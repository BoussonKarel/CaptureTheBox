# pylint: skip-file
from RPi import GPIO
import time, threading, json, datetime, os, base64
from subprocess import check_output # IP on display
from ttn import MQTTClient # LoRa
import paho.mqtt.client as mqtt # LoRa

from repositories.DataRepository import DataRepository
from flask import Flask, jsonify, request
from flask_socketio import SocketIO
from flask_cors import CORS

import secrets # Secret keys
from helpers.LCD import LCD
from helpers.ArduinoSerial import ArduinoSerial
from helpers.SpelBeheer import SpelBeheer

# ------- INSTELLINGEN -------
mode = "LoRa" # Data komt binnen via LoRa (MQTT)
# mode = "Serial" # Data komt binnen via Seriële communicatie
polling_delay = 5*60 # Delay (in seconden) tussen elke Arduino ondervraging

# ------- GPIO -------
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# ------- FLASK -------
app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.Flask["secret_key"]

socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app)

# ------- ARDUINO -------
# Met deze code wordt elke {opvraging_delay} de Arduino ondervraagt voor de laatste sensorwaarden
# De uitvoer van de arduino komt in arduino_callback, die geeft het door aan update_value()
# update_value() steekt alles in de database en doet eventuele emits
def arduino_polling():
    while True:
        if (mode == "Serial"):
            Arduino.tx("LDR;")
            Arduino.tx("GPS;")
            time.sleep(polling_delay)

def arduino_callback(msg):
    print("[RX ARDUINO]")
    jsonObject = json.loads(msg)

    for item in jsonObject.items():
        key = item[0]
        value = item[1]
        
        if (value == "" or value is None):
            print("Ongeldige waarde")
            break
        if (key == "LDR"):
            update_value(key, value)
        elif (key == "RFID"):
            update_value(key, value)
        elif (key == "latitude"):
            gps_data = f"{jsonObject['latitude']};{jsonObject['longitude']}"
            update_value("GPS", gps_data)

if (mode == "Serial"):
    Arduino = ArduinoSerial(arduino_callback)
    thread_arduino_polling = threading.Thread(target=arduino_polling)
    thread_arduino_polling.start()

# ------- LORA -------
# Hier zit alle code om via MQTT de binnengekomen LoRa messages te ontvangen
# De binnenkomende data wordt als base64 meegegeven met lora_decode
# lora_decode() zet het om naar iets bruikbaars voor update_value()
# update_value() steekt alles in de database en doet eventuele emits
def lora_connect():
    lora_connected = False
    while not lora_connected:
        try:
            print("[TTN] Attempting to connect...")
            ttn_client.connect()
            ttn_client.set_uplink_callback(ttn_message)
            lora_connected = True
            print("[TTN] Connected")
        except Exception as e:
            print("[TTN] Error", e)
            print("[LoRa] Trying again in 10 seconds")
            time.sleep(10)

def ttn_message(msg, client):
    print("[TTN] Receiving...")
    lora_decode(msg.payload_raw)

def lora_decode(payload):
    data = base64.b64decode(payload).hex()
    print(data)
    bytes = bytearray.fromhex(data)

    data_ldr = round(bytes[0] / 255 * 100.0, 2)
    update_value("LDR", data_ldr)

    data_rfid = ""
    i = 0
    for byte in [ bytes[9], bytes[10], bytes[11], bytes[12]]:
        byteHex = hex(byte)[2:]
        if len(byteHex) == 1:
            byteHex = "0" + byteHex
        data_rfid += f"{byteHex}"
        if (i < 3):
            data_rfid += " "
        i += 1
    update_value("RFID", data_rfid)

    data_lat = 0
    # Bij negatieve lat/long is er 0x80 toegevoegd aan de MSB
    if ((bytes[1] << 24) & 0x80):
        data_lat |= ((bytes[1] << 24) & (0x80 << 24))
    else:
        data_lat |= (bytes[1] << 24)
    data_lat |= (bytes[2] << 16) | (bytes[3] << 8) | bytes [4]
    data_lat /= 1000000

    data_long = 0
    if ((bytes[5] << 24) & 0x80):
        data_long |= ((bytes[5] << 24) & (0x80 << 24))
    else:
        data_long |= (bytes[5] << 24)
    data_long |= (bytes[6] << 16) | (bytes[7] << 8) | bytes [8]
    data_long /= 1000000

    gps_data = f"{data_lat};{data_long}"
    update_value("GPS", gps_data)

ttn_client = MQTTClient(secrets.LoRa["game"], secrets.LoRa["access_key"], mqtt_address="", discovery_address="discovery.thethings.network:1900", reconnect=True)


if (mode == "LoRa"):
    thread_lora_connect = threading.Thread(target=lora_connect)
    thread_lora_connect.start()

# ------- UPDATE_VALUE -------
# update_value() steekt alles in de database en doet eventuele emits
# Deze code is apart van de Arduino en LoRa code, zodat ik makkelijk kan switchen tussen Serieel <> LoRa
vorig_lichtp = None
vorige_GPS = None
vorige_RFID = None

def update_value(type, value):
    global vorig_lichtp
    global vorige_GPS
    global vorige_RFID
    timestamp = datetime.datetime.now()

    if (type == "LDR"):
        if (value != vorig_lichtp):
            vorig_lichtp = value
            # LDR waarde toevoegen in database
            DataRepository.meting_toevoegen(2, value)
            # socketio.emit('B2F_MVP1_LDR', {"Waarde": value}, broadcast=True)
        else:
            print("LDR waarde niet veranderd. Niet updaten.")
    elif (type == "GPS"):
        if (value != vorige_GPS):
            vorige_GPS = value
            # GPS waarden toevoegen in database
            DataRepository.meting_toevoegen(1, value)
            # Emit naar frontend die open staat
            socketio.emit('B2F_GPS_locatie', {"Waarde": value}, broadcast=True)
        else:
            print("GPS waarde niet veranderd. Niet updaten.")
    elif (type == "RFID"):
        SpelBeheer.RFID_actie(value, timestamp)
        # socketio.emit("B2F_MVP1_RFID", {"UID": value})
    elif (sensor == "Error"):
        print(f"Arduino kon niet antwoorden op verzoek: {value}")

# ------- LCD DISPLAY -------
def show_ip():
    DB = [ 26,19,13,6,5,21,20,16 ]
    E = 22
    RS = 27
    display = LCD(E, RS, DB)

    while True:
        display.clear()
        ips = str(check_output(['hostname', '--all-ip-addresses']))
        # Haal b' en \\n eruit en splits in een array op een spatie
        ips = ips.strip("b'").strip(" \\n").split(" ")
        # Wifi IP = index 1 bij mij
        ip = ips[1]

        display.send_message(f"IP:")
        display.second_row()
        display.send_message(ip)
        display.cursor_off()
        time.sleep(30)

# ------- API ENDPOINTS -------
@app.route('/')
def hallo():
    return "Server is running."

# GPS Locatie
@app.route('/MVP1/LDR')
def get_LDR():
    # Laatste meting van sensor 2 (LDR)
    laatste_meting = DataRepository.laatste_meting(2)
    return jsonify(laatste_meting), 200

# Spel informatie
@app.route('/CTB/Spel', methods=["GET", "POST"])
def spel_info():
    if request.method == "GET":
        if (SpelBeheer.huidigSpel):
            return jsonify(SpelBeheer.spel_info()), 200
        else:
            return jsonify(Spel=None), 200
    elif request.method == "POST":
        gegevens = DataRepository.json_or_formdata(request)
        begintijd = datetime.datetime.strptime(gegevens["begintijd"], '%Y-%m-%d %H:%M')
        eindtijd = datetime.datetime.strptime(gegevens["eindtijd"], '%Y-%m-%d %H:%M')
        spelers = gegevens["spelers"]
        SpelID = SpelBeheer.spel_maken(begintijd, eindtijd, spelers)
        if (SpelID != None):
            return jsonify(SpelID=SpelID), 200
        else:
            return jsonify(Error="Kon spel niet aanmaken"), 500
        # print(gegevens)

# Een spel vroegtijdig stoppen
@app.route('/CTB/Spel/Stop', methods=["POST"])
def stop_spel():
    SpelBeheer.stop_spel(datetime.datetime.now())
    return jsonify(succes=1), 200
    
# Scorebord
@app.route('/CTB/Scorebord', methods=["GET"])
def scorebord():
    if (SpelBeheer.huidigSpel):
        scorebord = DataRepository.scorebord(SpelBeheer.huidigSpel.id)
        return jsonify(scorebord), 200
    else:
        return jsonify(error="NO_GAME"), 200

# Huidige koffer eigenaar ophalen
@app.route('/CTB/Bezit', methods=["GET"])
def bezit():
    if (SpelBeheer.huidigSpel):
        owner = DataRepository.huidige_eigenaar(SpelBeheer.huidigSpel.id)
        return jsonify(owner), 200
    else:
        return jsonify(Naam=None), 200

# ------- SOCKETIO -------
@socketio.on('connect')
def initial_connection():
    LDR_waarde = DataRepository.laatste_meting(2)
    socketio.emit('B2F_MVP1_LDR', LDR_waarde)
    # Stuur live (laatste) GPS locatie
    gps_loc = DataRepository.huidige_locatie()
    socketio.emit('B2F_GPS_locatie', gps_loc)

# Veilig afsluiten? Stuur dit commando.
@socketio.on('F2B_shutdown')
def shutdown(msg):
    os.system('sudo shutdown -h now')

# ------- LOOP -------
try:
    thread_show_ip = threading.Thread(target=show_ip)
    thread_show_ip.start()

    if __name__ == '__main__':
        socketio.run(app, debug=False, host='0.0.0.0')
except KeyboardInterrupt as e:
    print(e)
finally:
    GPIO.cleanup()
    if (mode == "Serial"):
        Arduino.Serial.close() # close port
    elif (mode == "LoRa"):
        ttn_client.close()
    print("Capture The Box: \"Goodbye\"")