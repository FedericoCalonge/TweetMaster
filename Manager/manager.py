import json
from Tweet.Tweet import Tweet as Tweet
from Campaign.Campaign import Campaign as Campaign
from DataBaseConnector import configTables 
from datetime import datetime
from DataBaseConnector import Connector as Connector
import requests

class Manager():
	def insertCampaign(self, userInputs):
		#Con los nombres de los campos correspondientes a los del json que nos llegan armamos un objeto campaña.
		#Pero antes de esto como fields["hashtags"] y fields["mentions"] son LISTAS, tenemos que pasarlas a un string para poder añadirlo a la BD como un varchar: 
		stringHashtag = self.listaAString(userInputs["hashtags"]) # #donaldTrump-#G20
		stringMention = self.listaAString(userInputs["mentions"]) # @donaldTrump-@miauricioOK
	
		ObjetoCampaign = Campaign(1, userInputs["email"], stringHashtag, stringMention, userInputs["startDate"], userInputs["endDate"])
		#Llamamos a un metodo de Connector para agregar la campaña a la BD junto con las mentions y los hashtags:
		return Connector.insertarCampaignBD(ObjetoCampaign)

	def listaAString(self, lista):
		string = "-".join(lista)
		return string
	
	def deleteCampaignporuser(self, email_user):
		#Se puede eliminar la campaña sólo si esta NO está iniciada (esta logica la aplicamos en 
		#eliminarCampaignBDxUser)
		Connector.eliminarCampaignBDxUser(email_user)

	def deleteCampaignporid(self, idCampaign):
		#Se puede eliminar la campaña sólo si esta NO está iniciada:
		campaignRetornada = Connector.retornarCampaignBD(idCampaign)
		fecha_inicio_campaign = campaignRetornada.startDate
		fecha_actual = datetime.now()
		#La campaña inició (fecha de inicio de campaign es MENOR a fecha actual), no hacemos nada:
		if not (fecha_inicio_campaign < fecha_actual):
		#La campaña NO inició, eliminamos la campaña:
			Connector.eliminarCampaignBDxID(idCampaign)
			return True
		else:
			return False
			
	def returnCampaign(self, idCampaign):
		return Connector.retornarCampaignBD(idCampaign)
	
	def modifyCampaign(self, idCampaign, columna, inputUser):
		#Se puede modificar la campaña sólo si esta NO está iniciada:
		campaignRetornada = Connector.retornarCampaignBD(idCampaign)
		if campaignRetornada == []:
			return False
		fecha_inicio_campaign = campaignRetornada.startDate
		fecha_actual = datetime.now()
		#La campaña inició (fecha de inicio de campaign es MENOR a fecha actual), no hacemos nada:
		if not (fecha_inicio_campaign < fecha_actual):
		#La campaña NO inició, modificamos la campaña:
			Connector.modificarCampaignBD(idCampaign, columna, inputUser)
		return True
		
	def returnCampaignsInProgress(self):
		#Obtenemos TODAS las Campañas y vemos una por una si la fecha de inicio de campaign es MENOR a
		#la fecha actual y la fecha de fin de la campaña es MAYOR a la fecha actual. Y si sucede esto la agregamos a una nueva lista.
		listaCampaigns = configTables.session.query(configTables.Campaign).all()
		print (listaCampaigns)
		listaNuevaCampaigns=[]
		for c in listaCampaigns:
			#Cada c es un: <Campaign(idC='1', startDate='28 11 2018 18:02:00', finDate='02 12 2018 19:26:22', email='test@gmail.com', hashtags='#test-#mock', mentions='@testCampaign-@mockOK')>
			#Y accedo a los atributos con c.atributo (el atributo está en la tabla Campaign dentro de configTables), osea asi: print (c.id)
			idCampaign = c.id
			print (idCampaign)
			campaignRetornada = Connector.retornarCampaignBD(idCampaign)
			fecha_inicio_campaign = campaignRetornada.startDate
			fecha_fin_campaign = campaignRetornada.finDate
			fecha_actual=datetime.now()
			if ((fecha_inicio_campaign < fecha_actual) and (fecha_fin_campaign > fecha_actual)):  #La campaña está en curso. Agrego la campaña a la nueva lista a devolver.
				listaNuevaCampaigns.append(c)
			#Si la campaña no inició no hago nada. 
			

		return (listaNuevaCampaigns) #Devolvemos la lista de campañas en curso (que todavía no finalizaron)
		#[<Campaign(idC='15', startDate='28 11 2018 18:02:00', finDate='25 12 2018 19:26:22', email='test@gmail.com', hashtags='#test-#mock', mentions='@testCampaign-@mockOK')>, 
		#<Campaign(idC='16', startDate='28 11 2018 18:02:00', finDate='25 12 2018 19:26:22', email='test@gmail.com', hashtags='#test-#mock', mentions='@testCampaign-@mockOK')>]

	#Fijarse en test_manager que sería este tweetsJson que recibe.
	def insertTweets(self, tweetsJson, idC):
		tweets = json.loads(tweetsJson)
		#Los separamos en tweets separados y llamamos a insertTweet para agregarlo uno por uno:
		for i in range(len(tweets)):
			t = Tweet(tweets[i])
			self.insertTweet(t,idC) #Le pasamos el objeto Tweet instanciado.

	def insertTweet(self, TweetInput, idC):
		Connector.insertTweet(TweetInput, idC)
	
	#Arregla el desastre de #-# y @-@
	def _campaignStringToList(self, c):
		c.hashtags = c.hashtags.split("-")
		c.mentions = c.mentions.split("-")
		return c
	
	#POR QUË NO LO HACE EL CONECTOR
	def _dbCampaignToCampaig(self, dbC):
		return Campaign(dbC.id, dbC.email, dbC.hashtags, dbC.mentions, dbC.startDate, dbC.finDate)
		
	#Comunicacion entre Fetcher y Manager. Cada campaña se codifica a json:
	def fetchCampaings(self):
		campaignsToFetch = self.returnCampaignsInProgress()
		for idC in campaignsToFetch:
			c = self._campaignStringToList(self._dbCampaignToCampaig(idC))
			jsonCampaign = c.to_json()
			url = "http://127.0.0.1:5001/fetcher"
			headers = {"Content-Type":"application/json"}			
			response = requests.get(url, json=jsonCampaign, headers=headers)
			self.insertTweets(response.json()["Tweets"],idC)
			
			
			
			
			
			
			
			
			
			
			
		