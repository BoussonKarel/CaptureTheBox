class Speler:
    def __init__(self, spelerid, rfiduid, naam, mod):
        self._valueErrors = {}
        self.id = spelerid
        self.RFIDUID = rfiduid
        self.naam = naam
        self.moderator = mod

    # METHODS -------------------------------------------------------------
    def __str__(self):
        return f"(Speler {self.id}) {self.naam} - {self.RFIDUID}"

    def __repr__(self):
        return self.__str__()

    def jsonInfo(self):
        dict_speler = {"SpelerID": self.id, "RFIDUID": self.RFIDUID, "Naam": self.naam, "Moderator": self.moderator}
        return dict_speler

    # -------------------- VALIDATION --------------------
    @property
    def valueErrors(self):
        """The valueErrors property."""
        return self._valueErrors
        
    @property
    def IsValid(self):
        """The IsValid property."""
        return (len(self._valueErrors) == 0)

    # -------------------- PROPERTIES --------------------
    @property
    def id(self):
        """The id property."""
        return self._id
    @id.setter
    def id(self, value):
        if type(value) is int:
            self._id = value
        else:
            self._valueErrors["id"] = ValueError("Geen geldig id")

    @property
    def RFIDUID(self):
        """The RFIDUID property."""
        return self._RFIDUID
    @RFIDUID.setter
    def RFIDUID(self, value):
        if (type(value) is str):
            if (len(value) <= 64):
                self._RFIDUID = value
            else:
                self._valueErrors["RFIDUID"] = ValueError("Maximaal 64 karakters")
        elif (value == None):
            self._RFIDUID = None
        else:
            self._valueErrors["RFIDUID"] = ValueError("Geen geldig RFID UID")

    @property
    def naam(self):
        """The naam property."""
        return self._naam
    @naam.setter
    def naam(self, value):
        if (type(value) is str):
            if (len(value) <= 45):
                self._naam = value
            else:
                self._valueErrors["naam"] = ValueError("Maximaal 45 karakters")
        else:
            self._valueErrors["naam"] = ValueError("Geen geldige naam")

    @property
    def moderator(self):
        """The moderator property."""
        return self._moderator
    @moderator.setter
    def moderator(self, value):
        if (type(value) is int) and ((value == 0) or (value == 1)):
            self._moderator = value
        elif (value == None):
            self._moderator = 0
        else:
            self._valueErrors["moderator"] = ValueError("Geen geldige moderator waarde (0 of 1)")