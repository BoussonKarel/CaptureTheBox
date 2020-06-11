import datetime
from .Speler import Speler
from repositories.SpelerRepository import SpelerRepository

class Spel:
    def __init__(self, spelid, begintijd, eindtijd):
        self._valueErrors = {}
        self.id = spelid
        self.begintijd = begintijd
        self.eindtijd = eindtijd
        self.spelers = SpelerRepository.spelers_ophalen(spelid)

    # METHODS -------------------------------------------------------------
    def __str__(self):
        str = f"Spel {self.id}: {self.begintijd} - {self.eindtijd}"
        return str

    def __repr__(self):
        return self.__str__()

    def jsonInfo(self):
        dict_spel = {"SpelID": self.id, "Begintijd": str(self.begintijd), "Eindtijd": str(self.eindtijd)}
        lst_spelers = []
        for speler in self.spelers:
            lst_spelers.append(speler.jsonInfo())
        return {"Spel": dict_spel, "Spelers": lst_spelers}

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
    def begintijd(self):
        """The begintijd property."""
        return self._begintijd
    @begintijd.setter
    def begintijd(self, value):
        if (isinstance(value, datetime.datetime)):
            self._begintijd = value
        else:
            self._valueErrors["begintijd"] = ValueError("Geen geldige begintijd")

    @property
    def eindtijd(self):
        """The eindtijd property."""
        return self._eindtijd
    @eindtijd.setter
    def eindtijd(self, value):
        if (isinstance(value, datetime.datetime)):
            self._eindtijd = value
        else:
            self._valueErrors["eindtijd"] = ValueError("Geen geldige eindtijd")
        
    @property
    def spelers(self):
        """The spelers property."""
        return self._spelers
    @spelers.setter
    def spelers(self, value):
        if (isinstance(value, list)):
            e = 0
            for speler in value:
                if (not isinstance(speler, Speler)):
                    e += 1
            if (e < 1):
                self._spelers = value
            else:
                self._valueErrors["spelers"] = ValueError("Lijst bevat ongeldige speler")
        else:
            self._valueErrors["spelers"] = ValueError("Spelers is geen lijst")
