import unittest
from Tweet.Tweet import Tweet 
from Campaign.Campaign import Campaign
from datetime import datetime
from DataBaseConnector import Connector
from DataBaseConnector import configTables
from Manager import manager
from datetime import datetime
import json

class test_manager(unittest.TestCase):
    #Testeamos que los tweets que llegan se agregen correctamente a la BD.
    def test_InsertTweets(self):
        #Precondición: deben haber 3 campañas creadas e insertadas en la BD.
        configTables.BD.metadata.create_all(configTables.engine) #Se crea la BD (en caso que ya está creada no hace nada)
        
        userInputs= '{"email":"test@gmail.com","hashtags": ["#test", "#mock"], "mentions": ["@testCampaign", "@mockOK"], "startDate":"28 11 2018 18:02:00", "endDate":"25 12 2018 19:26:22"}'
        fields = json.loads(userInputs) #Pasa de json a diccionario, esto lo hace flask por eso no hace falta hacerlo en el insertCampaign() del manager.
        #Insertamos 3 campañas en la BD:
        manager.Manager().insertCampaign(fields)
        manager.Manager().insertCampaign(fields)
        id3erCampaign=manager.Manager().insertCampaign(fields)
    
        #Ejemplo de los lista de diccionario de tweets en formato JSON que el Fetcher le manda a Manager (tweetsJson).
        self.tweet1 = {
            "id_str" : "12366",
            "user" : {"name" : "NASAOk", "id_str" : "789456"},
            "entities" : {"hashtags" : ["#mars","#venus","#earth"],"user_mentions" : ["@NASA", "@planets"]},
            "created_at" : "Sun Mar 20 15:11:01 +0000 2018"
        }
        self.tweet2 = {
            "id_str" : "12477",
            "user" : {"name" : "MiauricioOK", "id_str" : "451325"},
            "entities" : {"hashtags" : ["#DonaldNoMeDejes"], "user_mentions" : ["@donaldTrump", "@G20"]},
            "created_at" : "Sun Mar 20 21:08:01 +0000 2018"
        }
        tweetsJson = [json.dumps(self.tweet1),json.dumps(self.tweet2)]
        #Insertamos 2 tweets en la 3er campaign.
        manager.Manager().insertTweets(tweetsJson, id3erCampaign)
        #Obtengo el 2do Tweet:
        tweetRetornado = Connector.returnTweetByIDT("12477")
        #Asserto los datos del 2do Tweet:
        print(tweetRetornado.ID)
        self.assertEqual(tweetRetornado.ID,"12477")
        self.assertEqual(tweetRetornado.userName, "MiauricioOK")
        self.assertEqual(tweetRetornado.userid, "451325")
        self.assertEqual(tweetRetornado.hashtags, "#DonaldNoMeDejes")
        self.assertEqual(tweetRetornado.mentions, "@donaldTrump-@G20")
        self.assertEqual(tweetRetornado.date, "Sun Mar 20 21:08:01 +0000 2018")

    #Testeamos que se cree la campaña correctamente en la BD y que sea retornada sin modificaciones.
    def test_InsertCampaign(self):
        configTables.BD.metadata.create_all(configTables.engine) #Se crea la BD (en caso que ya está creada no hace nada)
        
        #Entrada de ejemplo, lo que el usuario ingresa en la Interfaz Web en Alta Campaña (en formato JSON llegaria):
        userInputs= '{"email":"test@gmail.com","hashtags": ["#test", "#mock"], "mentions": ["@testCampaign", "@mockOK"], "startDate":"28 11 2018 18:02:00", "endDate":"25 12 2018 19:26:22"}'
        fields = json.loads(userInputs) #Pasa de json a diccionario, esto lo hace flask por eso no hace falta hacerlo en el insertCampaign() del manager.
        idCampaign=manager.Manager().insertCampaign(fields)
        campaignRetornada = Connector.retornarCampaignBD(idCampaign)

        #Asserto todos los atributos del objeto Campaign:
        self.assertEqual(campaignRetornada.emailDueño, "test@gmail.com")
        self.assertEqual(campaignRetornada.hashtags, "#test-#mock")
        self.assertEqual(campaignRetornada.mentions, "@testCampaign-@mockOK")
        self.assertEqual(campaignRetornada.startDate , datetime(2018, 11, 28, 18, 2))
        self.assertEqual(campaignRetornada.finDate , datetime(2018, 12, 25, 19, 26, 22))

    #Testeamos que se pueda modificar una campaña (siempre y cuando la campaña NO haya iniciado: 
    #la fecha de inicio de campaign start_date debe ser MENOR a la fecha actual) 
    #y que la columna a modificar se haya sobreescrito satisfactoriamente.
    def test_ModifyCampaign(self):
        #Precondicion: tener 2 campaigns en la BD.
        userInputs= '{"email":"test@gmail.com","hashtags": ["#test", "#mock"], "mentions": ["@testCampaign", "@mockOK"], "startDate":"18 12 2018 18:02:00", "endDate":"02 12 2018 19:26:22"}'
        fields = json.loads(userInputs) #Pasa de json a diccionario, esto lo hace flask por eso no hace falta hacerlo en el insertCampaign() del manager.
        #Creamos e insertamos 2 campaign:
        manager.Manager().insertCampaign(fields)
        id2daCampaign=manager.Manager().insertCampaign(fields)
        
        #Datos que ingresara el usuario (además de la id2daCampaign):
        columna="email"
        inputUser="pepito@gmail.com"
        
        manager.Manager().modifyCampaign(id2daCampaign, columna, inputUser)
        campaignRetornada = Connector.retornarCampaignBD(id2daCampaign)
        #Si imprimo (campaignRetornada.startDate) me imprime: 2018-11-28 18:02:00.
        #Pero si lo retorno es este tipo de dato--> datetime.datetime(2018, 11, 28, 18, 2)
        self.assertEqual(campaignRetornada.emailDueño, "pepito@gmail.com")
 
    #Pruebas en los metodos de manager:
    def test_ReturnCampaignBD(self):
        #Le pasamos la ID de Campaign 2
        objetoCampaign = Connector.retornarCampaignBD(2)
        print (objetoCampaign)
        #Imprime esto:
        # <idC:2 emailDueño:test@gmail.com hashtags:#test-#mock mentions:@testCampaign-@mockOK startDate:2018-11-28 18:02:00 finDate:2018-12-02 19:26:22> 

    def test_ReturnTweetsByIDC(self):
        #Retornamos los tuits con IDC 3 (de la 3ra campaña)
        tweets = Connector.returnTweetsByIDC(3)
        print(tweets)
        #Esto me devuelve, una lista de tweets en formato diccionario con sus atributos.
        #[{'id_str': 112112, 'user': {'name': 'MauricioOK', 'id_str': '451325'}, 'entities': {'hashtags': '#DonaldNoMeDejes', 'user_mentions': '@donaldTrump-@G20'}, 'created_at': '2018-03-20 21:08:01'},
        # {'id_str': 123456, 'user': {'name': 'NASAOk', 'id_str': '789456'}, 'entities': {'hashtags': '#mars-#venus-#earth', 'user_mentions': '@NASA-@planets'}, 'created_at': '2018-03-20 15:11:01'}]

    def test_FechaMayor(self):
        fecha1 = datetime(2018, 12, 19, 19, 49)
        print (fecha1)
        fecha_actual = datetime.now()
        if (fecha_actual > fecha1):
            print ("Mayor")
        else:
            print("Menor")

    def test_DeleteCampaignPorUser(self):
        email="test@gmail.com"
        manager.Manager().deleteCampaignporuser(email)

    def test_ReturnCampaignsInProgress(self):
        manager.Manager().returnCampaignsInProgress()

  