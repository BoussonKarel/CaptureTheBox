void GPS_setup() {
  // ***** GPS *****
  pinMode(GPS_power, OUTPUT);
  digitalWrite(GPS_power, HIGH);
  GPSSerial.begin(9600);
  
  // nemaMsgDisable("GSV");
  // nemaMsgDisable("GSA");
  // nemaMsgDisable("VTG");
  // nemaMsgDisable("GGA");
}

/* ************** GPS ************** */
void process_GPS() {
  // Zit er iets in?
  if (GPS_msg == "")
    return;

  // Dit is onze process 'msg'
  String msg = GPS_msg;
  GPS_msg = "";

  // Heeft hij de header $GPRMC
  String header = msg.substring(0,6);
  if (!header.equals("$GPRMC"))
    return;

  // We tellen het aantal komma's vanaf index 18
  int commas = 0;
  int previous_comma = 0;

  for (int i = 18; i < msg.length(); i++) {
    String c = (String) msg[i];
    if (c.equals(",") and i != 0) {
      String raw_part = msg.substring(previous_comma, i);

      if (raw_part != "") {
        if (commas == 1) {
          latitude = convert_to_decimalDegrees(raw_part, 2);
        }
        if (commas == 2 or commas == 4) {
          if (raw_part == "S")
            latitude = 0 - latitude;
        }  
        if (commas == 3) {
          longitude = convert_to_decimalDegrees(raw_part, 3);
        }
        if (commas == 4) {
          if (raw_part == "W")
            longitude = 0 - longitude;
        }
      }
          
      commas += 1;
      previous_comma = i + 1;
    }
  }
  /*
  Serial.println("-RAW: " + msg);
  Serial.println("LAT: " + String(latitude, 6));
  Serial.println("LONG: " + String(longitude, 6));
  */
}

/* ************** Convert to decimal ° ************** */
float convert_to_decimalDegrees(String raw_gps, int degreeLength) {
  float degrees = raw_gps.substring(0,degreeLength).toFloat();
  float minutes = raw_gps.substring(degreeLength).toFloat();
  return degrees + minutes / 60.0;
}

/* ************** CONFIG GPS ************** */
inline int calculateChecksum (const char *msg) {
  int checksum = 0;
  for (int i = 0; msg[i] && i < 32; i++)
  checksum ^= (unsigned char)msg[i];
  return checksum;
}
inline int nemaMsgSend (const char *msg) {
  char checksum[8];
  snprintf(checksum, sizeof(checksum)-1, "*%.2X", calculateChecksum(msg));
  GPSSerial.print("$");
  GPSSerial.print(msg);
  GPSSerial.println(checksum);
}
inline int nemaMsgDisable (const char *nema) {
    if (strlen(nema) != 3) return 0;
    char tmp[32];
    snprintf(tmp, sizeof(tmp)-1, "PUBX,40,%s,0,0,0,0", nema);
    //snprintf(tmp, sizeof(tmp)-1, "PUBX,40,%s,0,0,0,0,0,0", nema);
    nemaMsgSend(tmp);
    return 1;
}

inline int nemaMsgEnable (const char *nema) {
    if (strlen(nema) != 3) return 0;
    char tmp[32];
    snprintf(tmp, sizeof(tmp)-1, "PUBX,40,%s,0,1,0,0", nema);
    //snprintf(tmp, sizeof(tmp)-1, "PUBX,40,%s,0,1,0,0,0,0", nema);
    nemaMsgSend(tmp);
    return 1;
}
