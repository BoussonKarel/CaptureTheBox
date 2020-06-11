void RFID_setup() {
  // ***** RFID *****
  SPI.begin(); // Init SPI bus
  rfid.PCD_Init(); // Init MFRC522 
}

/* ************** RFID ************** */
void check_RFID() {
  if (rfid.PICC_IsNewCardPresent()) { // (true, if RFID tag/card is present ) PICC = Proximity Integrated Circuit Card
    if(rfid.PICC_ReadCardSerial()) { // true, if RFID tag/card was read
      for (byte i = 0; i < 4; ++i) { // read id (in parts)
        RFID_lastUID[i] = rfid.uid.uidByte[i];
      }
      display_loading();
    }
  }
}

void resetRFID() {
  RFID_lastUID[0] = 0;
  RFID_lastUID[1] = 0;
  RFID_lastUID[2] = 0;
  RFID_lastUID[3] = 0;
}
