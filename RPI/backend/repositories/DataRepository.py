from .Database import Database

class DataRepository:
    @staticmethod
    def json_or_formdata(request):
        if request.content_type == 'application/json':
            gegevens = request.get_json()
        else:
            gegevens = request.form.to_dict()
        return gegevens

    @staticmethod
    def meting_toevoegen(SensorID, Waarde):
        sql = "INSERT INTO meting (SpelID, Tijdstip, SensorID, Waarde) VALUES ((SELECT SpelID FROM spel WHERE NOW() > Begintijd AND NOW() < Eindtijd LIMIT 1), NOW(), %s, %s)"
        params = [SensorID, Waarde]
        return Database.execute_sql(sql, params)

    @staticmethod
    def laatste_meting(SensorID):
        sql = "SELECT Waarde FROM meting WHERE SensorID = %s ORDER BY MetingID DESC LIMIT 1"
        params = [SensorID]
        return Database.get_one_row(sql, params)

    @staticmethod
    def huidige_locatie():
        sql = "SELECT Waarde FROM meting WHERE SensorID = 1 ORDER BY MetingID DESC LIMIT 1"
        return Database.get_one_row(sql)

    @staticmethod
    def scorebord(SpelID):
        sql = "SELECT  Naam, SUM(TO_SECONDS(B.Eindtijd) - TO_SECONDS(B.Starttijd)) AS `Score` FROM bezit B JOIN speler S ON B.SpelerID = S.SpelerID WHERE SpelID = %s GROUP BY S.Naam ORDER BY `Score` DESC"
        params = [SpelID]
        return Database.get_rows(sql, params)

    @staticmethod
    def huidige_eigenaar(SpelID):
        sql = "SELECT B.SpelerID, Naam FROM bezit B JOIN speler SP ON SP.SpelerID = B.SpelerID WHERE SpelID = %s ORDER BY BezitID DESC LIMIT 1"
        params = [SpelID]
        return Database.get_one_row(sql, params)
