from .Database import Database
from model.Speler import Speler

class SpelerRepository:
    @staticmethod
    def json_or_formdata(request):
        if request.content_type == 'application/json':
            gegevens = request.get_json()
        else:
            gegevens = request.form.to_dict()
        return gegevens

    @staticmethod
    def spelers_ophalen(SpelID):
        spelers = []
        sql = "SELECT SpelerID, RFIDUID, Naam, Moderator FROM spel_has_speler JOIN speler on Speler_SpelerID = SpelerID WHERE Spel_SpelID = %s"
        params = [SpelID]
        rows = Database.get_rows(sql, params)

        if rows is not None:
            for row in rows:
                # mapping naar object
                spelers.append(SpelerRepository.map_to_object(row))
        return spelers

    @staticmethod
    def nieuwe_speler(rfid, speler):
        sql = "INSERT INTO speler (RFIDUID, naam) VALUES (%s, %s)"
        params = [rfid, speler]
        return Database.execute_sql(sql, params)

    @staticmethod
    def speler_toevoegen(SpelID, SpelerID):
        sql = "INSERT INTO spel_has_speler (Spel_SpelID, Speler_SpelerID) VALUES (%s, %s)"
        params = [SpelID, SpelerID]
        return Database.execute_sql(sql, params)

# helpers -----------------------------------------------
    @staticmethod
    def map_to_object(row):
        if (row is not None) and (type(row) is dict):
            id = SpelerRepository.checkColumn(row, "SpelerID")
            rfiduid = SpelerRepository.checkColumn(row, "RFIDUID")
            naam = SpelerRepository.checkColumn(row, "Naam")
            mod = SpelerRepository.checkColumn(row, "Moderator")
        return Speler(id, rfiduid, naam, mod)

    @staticmethod
    def checkColumn(row, columnName):
        result=""
        if (columnName in row.keys() and row[columnName] is not None): # controle op Null
            result = row[columnName]
        return result