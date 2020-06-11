from RPi import GPIO
import time

class LCD:
    def __init__(self, E, RS, DB, debugging=False):
        self._E = E
        self._RS = RS
        self._DB = DB
        self._debug = debugging
        self.__setup__()
        self.init_LCD()

    def __setup__(self):
        GPIO.setmode(GPIO.BCM)

        for datalijn in self.DB:
            GPIO.setup(datalijn, GPIO.OUT)
        
        GPIO.setup(self.RS, GPIO.OUT)
        GPIO.setup(self.E, GPIO.OUT)

    # ----------------------------------------------------------------------------------------------------------
    @property
    def E(self):
        """The E property."""
        return self._E

    @property
    def RS(self):
        """The RS property."""
        return self._RS

    @property
    def DB(self):
        """The DB property."""
        return self._DB

    @property
    def debug(self):
        """The debug property."""
        return self._debug

    # ----------------------------------------------------------------------------------------------------------
    def __send_instruction(self, value):
        GPIO.output(self.RS, 0) # 0 = instructie
        GPIO.output(self.E, 1) # E omhoog

        self.__set_data_bits(value)

        GPIO.output(self.E, 0)  # E omlaag (dalende flank)
        time.sleep(.01)

    def __send_character(self, value):
        GPIO.output(self.RS, 1) # 0 = instructie
        GPIO.output(self.E, 1) # E omhoog

        self.__set_data_bits(value)

        GPIO.output(self.E, 0)   # E omlaag (dalende flank)
        time.sleep(.01)

    def __set_data_bits(self, value):
        # Dit moet een routine worden die de bits uit de byte haalt, maar in plaats van deze serieel door te
        # sturen zetten we ze nu parallel klaar op de 8 GPIO pinnen van de databus
        mask = 1
        for i in range(8):
            GPIO.output(self.DB[i], value & mask)
            mask = mask << 1

    # ----------------------------------------------------------------------------------------------------------
    # INITIALISEER LCD: Function set, Display aan, Display clear + cursor home
    def init_LCD(self):
        # 1) Function set
        # 8 bit, 2 lines, 5x7
        if (self.debug):
            print("Function set")
        self.__send_instruction(0b00111000)

        self.display_on()
        self.clear()
    
    # CLEAR
    def clear(self):
        # 3) Clear display en cursor home
        if (self.debug):
            print("Clearing display...")
        self.__send_instruction(1)

    # DISPLAY ON
    def display_on(self):
        # 2) Display on
        if (self.debug):
            print("Display on")
        self.__send_instruction(0b00001111)

    def cursor_off(self):
        if (self.debug):
            print("Cursor off")
        self.__send_instruction(0b00001100)

    # CURSOR ADRES
    def set_cursor(self, adres):
        self.__send_instruction(128 | adres)

    def cursor_locatie(self, rij, positie):
        adres = positie -1
        if (rij == 2):
            adres = adres + 0x40
        self.set_cursor(adres)
        return adres

    # CURSOR OP 2E RIJ
    def second_row(self):
        self.set_cursor(0x40)

    # SEND MESSAGE
    def send_message(self, msg):
        if len(msg) <= 32:
            # Eerst 16 op lijn 1, daarna op lijn 2
            for i in range(0, len(msg)):
                self.__send_character(ord(msg[i]))

                # NEWLINE NA KARAKTER 16
                if (i == 15):
                    # 0b1000000 | DDRAM adres
                    self.second_row()
                # STOPPEN NA KARAKTER 32
                if (i == 31):
                    break
        else:
            # Tekst tonen en scrollen
            for c in msg:
                self.__send_character(ord(c))