from repositories.SpelRepository import SpelRepository
from repositories.SpelerRepository import SpelerRepository
from model.Spel import Spel

import time, threading

import datetime

class SpelBeheer:
    huidigSpel = None
    RFIDtags = [ "66 c0 54 73", "52 ae 43 73", "6a 08 15 a3", "29 bf fd a3", "7a 63 50 73", "2a 1f 56 73"]

    @staticmethod
    def spel_maken(begintijd, eindtijd, spelers):
        # Nodig om een spel te maken:
        # - Lijst met spelernamen
        # - Begintijd, Eindtijd
        SpelID = SpelRepository.spel_aanmaken(begintijd, eindtijd)
        if (SpelID != None):
            print(SpelID)
            index = 0
            for speler in spelers:
                try:
                    RFID = SpelBeheer.RFIDtags[index]
                    index += 1
                except IndexError:
                    RFID = None
                SpelerID = SpelerRepository.nieuwe_speler(RFID, speler)
                SpelerRepository.speler_toevoegen(SpelID, SpelerID)
            return SpelID
        else:
            return None

    @staticmethod
    def spel_updaten():
        while True:
            # Geen spel bezig: zoeken
            if (SpelBeheer.huidigSpel == None):
                SpelBeheer.huidigSpel = SpelRepository.actief_spel_ophalen()
            # Spel bezig
            else:
                # CHECK OP STOP
                eindtijd = SpelBeheer.huidigSpel.eindtijd
                now = datetime.datetime.now()
                if (eindtijd < now):
                    SpelBeheer.stop_spel(eindtijd)
            time.sleep(10)

    @staticmethod
    def RFID_actie(UID, timestamp):
        if (SpelBeheer.huidigSpel):
            SpelID = SpelBeheer.huidigSpel.id
            print(f"Speler {UID} probeert de box te stelen...")
            # Eindtijd toevoegen bij vorige eigenaar (als die er is)
            SpelRepository.einde_bezit(SpelID, timestamp)
            # Nieuwe entry met starttijd
            SpelRepository.start_bezit(SpelID, UID, timestamp)

    # Het spel stoppen
    @staticmethod
    def stop_spel(tijdstip):
        temp_spel = SpelBeheer.huidigSpel
        SpelBeheer.huidigSpel = None
        # Laatste bezit een de eindtijd geven
        SpelRepository.einde_bezit(temp_spel.id, tijdstip)
        if (tijdstip < temp_spel.eindtijd): # Als het om een vroegtijdige stop gaat
            SpelRepository.eindtijd_aanpassen(temp_spel.id, tijdstip)
        print("Spel is gestopt")

    @staticmethod
    def spel_info():
        if (SpelBeheer.huidigSpel):
            dict_spel = SpelBeheer.huidigSpel.jsonInfo()
            return dict_spel
        else:
            return {"spel": None, "spelers": None}

thread_spel_update = threading.Thread(target=SpelBeheer.spel_updaten)
thread_spel_update.start()