int succes[4][8] ={
  {
    0,
    0b01111010,
    0b01000010,
    0b01000010,
    0b01111010,
    0b00001010,
    0b00001010,
    0b01111001
  },
  {
    0,
    0b01011110,
    0b01010010,
    0b01010000,
    0b01010000,
    0b01010000,
    0b01010010,
    0b10011110
  },
  {
    0,
    0b11110111,
    0b10010100,
    0b10000100,
    0b10000111,
    0b10000100,
    0b10010100,
    0b11110111
  },
  {
    0,
    0b10111100,
    0b00100000,
    0b00100000,
    0b10111100,
    0b00000100,
    0b00000100,
    0b10111100
  }
};

void MAX_setup() {
  pinMode(MAX_SS, OUTPUT);
  pinMode(MAX_SDA, OUTPUT);
  pinMode(MAX_CLK, OUTPUT);

  init_MAX();

  clear_MAX();
  delay(2000);
}

void display_night() {
  MAX_setRow(0,1,128);
  MAX_setRow(0,8,128);
  MAX_setRow(3,1,1);
  MAX_setRow(3,8,1);
}

void display_loading() {
  int loading[] = { 128,192,224,240,248,252,254,255 };

  clear_MAX();
  for (int i = 0; i < 4; i++) {
    for (int x = 0; x < 8; x++) {
      for (int r = 0; r < 9; r++) {
        MAX_setRow(i,r,loading[x]);
      }
      delay(100);
    }
  }
  display_succes();
}

void display_succes() {
  clear_MAX();
  for (int i = 0; i < 4; i++) {
    int index = 8;
    for (int r = 0; r < 9; r++) {
      MAX_setRow(i, r, succes[i][index]);
      index--;
    }
  }
  delay(2000);
  clear_MAX();
}

void clear_MAX() {
  for (int i = 1; i <= 8; i++) {
    digitalWrite(MAX_SS, LOW);
    writeOut(i, 0);
    writeOut(i, 0);
    writeOut(i, 0);
    writeOut(i, 0);
    digitalWrite(MAX_SS, HIGH);
  }
  
  if (MAX_nightmode) {
    display_night();
  }
}

void writeOut(byte reg, byte data) {
  shiftOut(MAX_SDA, MAX_CLK, MSBFIRST, reg);
  shiftOut(MAX_SDA, MAX_CLK, MSBFIRST, data);
}

void writeOutReverse(byte reg, byte data) {
  shiftOut(MAX_SDA, MAX_CLK, MSBFIRST, reg);
  shiftOut(MAX_SDA, MAX_CLK, LSBFIRST, data);
}

void writeOutSS(byte reg, byte data) {
  digitalWrite(MAX_SS, LOW);
  shiftOut(MAX_SDA, MAX_CLK, MSBFIRST, reg);
  shiftOut(MAX_SDA, MAX_CLK, MSBFIRST, data);
  digitalWrite(MAX_SS, HIGH);
}

void init_MAX() {
  for (int i = 0; i < 4; i++) {
    writeOutSS(0xB, 7);  // show 4 digits
    writeOutSS(0x9, 0);  // use digits (not bit patterns)
    writeOutSS(0xF, 0);  // no display test
    writeOutSS(0xA, 0);  // character intensity: range: 0 to 15
    writeOutSS(0xC, 1);  // not in shutdown mode (ie. start it up)
  }
}

void MAX_setIntensity(int intensity) {
  for (int i = 0; i < 4; i++) {
    writeOutSS(0xA, intensity);  // character intensity: range: 0 to 15
  }
  MAX_intensity = intensity;
}

void MAX_setRow(int addr, byte row, byte data) {
  digitalWrite(MAX_SS, LOW);
  for (int i = 3; i >= 0; i--) {
    if (i == addr) {
      writeOutReverse(row, data);
    }
    else {
      writeOut(0x0, 0);
    }
  }
  digitalWrite(MAX_SS, HIGH);
}
