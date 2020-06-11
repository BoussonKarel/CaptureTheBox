from .Database import Database
from model.Spel import Spel

class SpelRepository:
    @staticmethod
    def json_or_formdata(request):
        if request.content_type == 'application/json':
            gegevens = request.get_json()
        else:
            gegevens = request.form.to_dict()
        return gegevens

    @staticmethod
    def spel_aanmaken(begintijd, eindtijd):
        sql = "INSERT INTO spel (begintijd, eindtijd) values (%s, %s)"
        params = [begintijd, eindtijd]
        return Database.execute_sql(sql, params)

    @staticmethod
    def eindtijd_aanpassen(SpelID, eindtijd):
        sql = "UPDATE spel SET eindtijd = %s WHERE SpelID = %s"
        params = [eindtijd, SpelID]
        return Database.execute_sql(sql, params)

    @staticmethod
    def actief_spel_ophalen():
        print("Zoeken naar spel...")
        sql = "SELECT * FROM spel WHERE Begintijd <= NOW() AND NOW() <= Eindtijd"
        result = Database.get_one_row(sql)
        if type(result) is dict:
            # mapping naar Categorie object
            result = SpelRepository.map_to_object(result)
            print("Spel gevonden!")
            return result
        return None

    @staticmethod
    def einde_bezit(SpelID, eindtijd):
        sql = "UPDATE bezit SET Eindtijd = %s WHERE BezitID = (SELECT BezitID FROM bezit WHERE SpelID = %s ORDER BY BezitID DESC LIMIT 1)"
        params = [eindtijd, SpelID]
        Database.execute_sql(sql, params)

    @staticmethod
    def start_bezit(SpelID, UID, starttijd):
        subquery = "SELECT SpelerID FROM spel_has_speler JOIN speler ON Speler_SpelerID = SpelerID WHERE Spel_SpelID = %s AND RFIDUID = %s"
        sql = f"INSERT INTO bezit (SpelID, SpelerID, Starttijd) VALUES (%s, ({subquery}), %s);"
        params = [SpelID, SpelID, UID, starttijd]
        Database.execute_sql(sql, params)

# helpers -----------------------------------------------
    @staticmethod
    def map_to_object(row):
        if (row is not None) and (type(row) is dict):
            id = SpelRepository.checkColumn(row, "SpelID")
            begintijd = SpelRepository.checkColumn(row, "Begintijd")
            eindtijd = SpelRepository.checkColumn(row, "Eindtijd")
        return Spel(id, begintijd, eindtijd)

    @staticmethod
    def checkColumn(row, columnName):
        result=""
        if (columnName in row.keys() and row[columnName] is not None): # controle op Null
            result = row[columnName]
        return result