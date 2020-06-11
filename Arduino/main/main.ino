/*******************************************************************************
 * Copyright (c) 2015 Thomas Telkamp and Matthijs Kooijman
 *
 * Permission is hereby granted, free of charge, to anyone
 * obtaining a copy of this document and accompanying files,
 * to do whatever they want with them without any restriction,
 * including, but not limited to, copying, modification and redistribution.
 * NO WARRANTY OF ANY KIND IS PROVIDED.
 *
 * This example sends a valid LoRaWAN packet with payload "Hello,
 * world!", using frequency and encryption settings matching those of
 * the The Things Network.
 *
 * This uses OTAA (Over-the-air activation), where where a DevEUI and
 * application key is configured, which are used in an over-the-air
 * activation procedure where a DevAddr and session keys are
 * assigned/generated for use with all further communication.
 *
 * Note: LoRaWAN per sub-band duty-cycle limitation is enforced (1% in
 * g1, 0.1% in g2), but not the TTN fair usage policy (which is probably
 * violated by this sketch when left running for longer)!

 * To use this sketch, first register your application and device with
 * the things network, to set or generate an AppEUI, DevEUI and AppKey.
 * Multiple devices can use the same AppEUI, but each device has its own
 * DevEUI and AppKey.
 *
 * Do not forget to define the radio type correctly in config.h.
 *
 *******************************************************************************/

#include <lmic.h>
#include <hal/hal.h>
#include <SPI.h>

// This EUI must be in little-endian format, so least-significant-byte
// first. When copying an EUI from ttnctl output, this means to reverse
// the bytes. For TTN issued EUIs the last bytes should be 0xD5, 0xB3,
// 0x70.
static const u1_t PROGMEM APPEUI[8]= { 0x00, 0x11, 0x22, 0x33, 0x44, 0x55, 0x66, 0x77 };
void os_getArtEui (u1_t* buf) { memcpy_P(buf, APPEUI, 8);}

// This should also be in little endian format, see above.
static const u1_t PROGMEM DEVEUI[8]={ 0x00, 0x11, 0x22, 0x33, 0x44, 0x55, 0x66, 0x77 };
void os_getDevEui (u1_t* buf) { memcpy_P(buf, DEVEUI, 8);}

// This key should be in big endian format (or, since it is not really a
// number but a block of memory, endianness does not really apply). In
// practice, a key taken from ttnctl can be copied as-is.
// The key shown here is the semtech default key.
static const u1_t PROGMEM APPKEY[16] = { 0x00, 0x11, 0x22, 0x33, 0x44, 0x55, 0x66, 0x77, 0x77, 0x66, 0x55, 0x44, 0x33, 0x22, 0x11, 0x00 };
void os_getDevKey (u1_t* buf) {  memcpy_P(buf, APPKEY, 16);}

static uint8_t mydata[] = "Hello, world!";
static osjob_t sendjob;

// Schedule TX every this many seconds (might become longer due to duty
// cycle limitations).
const unsigned TX_INTERVAL = 60;

// Pin mapping
const lmic_pinmap lmic_pins = {
    .nss = 10,
    .rxtx = LMIC_UNUSED_PIN,
    .rst = 5,
    .dio = {2, 3, 4},
};

/* ************** RFID ************** */
#include <SPI.h>
#include <MFRC522.h>

#define RFID_SS 53
#define RFID_RST 49
// MOSI 51
// MISO 50
// SCK 52
MFRC522 rfid(RFID_SS, RFID_RST); // Instance of the class

byte RFID_lastUID[4] = {0,0,0,0};

unsigned long millisCheckpoint;

/* ************** GPS ************** */
int GPS_power = 7;
bool GPS_status = false;
#define GPSSerial Serial1

int gpsByte = -1;
int dollarSigns;
String GPS_msg = "";

float latitude, longitude;

/* ************** LDR ************** */
int LDR = A0;

/* ************** DOTM ************** */
#define MAX_SS 24
#define MAX_SDA 22
#define MAX_CLK 26

int MAX_intensity = 0;

bool MAX_nightmode = false;

/* ************** SETUP ************** */
void setup() {
  setData();
  LoRa_setup();
  
  // ***** RFID *****
  //RFID_setup();
  // ***** GPS *****
  GPS_setup();
  // ***** Dot Matrix *****
  MAX_setup();

  millisCheckpoint = millis();
}

/* ************** LOOP ************** */
bool rfid_allowed = false;

void loop() {
  LoRa_loop();
  
  // Check GPS messages
  while (GPSSerial.available()) {
    gpsByte = GPSSerial.read();
    if (gpsByte != -1) {
      char gpsChar = (char) gpsByte;
      
      if (gpsChar == '$') {
        dollarSigns++;
        if (dollarSigns == 1) {
          process_GPS();
          dollarSigns = 0;
        }
      }

      GPS_msg += (String) gpsChar;
    }
  }

  // Check for RFID cards
  if (rfid_allowed) {
    check_RFID();
  }

  check_nightmode();
}

void check_nightmode() {
    // Toggle night mode (4 dots)
  float LDR = get_LDR();
  if (MAX_nightmode == false) {
    if (LDR < 20) {
      // Toggle nightmode ON
      MAX_nightmode = true;
      display_night();
    }
  }
  else {
    if (LDR >= 20) {
      MAX_nightmode = false;
      clear_MAX();
    }
  }

  // Set intensity
  if (LDR > 0 && LDR <= 40) {
    if (MAX_intensity != 0) {
      MAX_setIntensity(0);
    }
  }
  if (LDR > 40 && LDR <= 70) {
    if (MAX_intensity != 1) {
      MAX_setIntensity(1);
    }
  }
  if (LDR > 70 && LDR <= 100) {
    if (MAX_intensity != 2) {
      MAX_setIntensity(2);
    }
  }
}
