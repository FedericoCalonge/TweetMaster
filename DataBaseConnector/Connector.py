import flask_sqlalchemy
from datetime import datetime
import json
import sys
from DataBaseConnector import configTables
sys.path.append("..")
from Campaign import *

#Primerio insertar si o si una campaig así se ejecuta la linea configTables.BD.metadata.create_all(configTables.engine) que crea la BD.
#manager.insertCampaign('{"email":"donaldTrump@gmail.com","hashtags": ["#donaldTrump", "#G20"], "mentions": ["@donaldTrump", "@miauricioOK"], "sDate":"28-11-2018", "eDate":"02-12-2018"}')
def insertarCampaignBD(CampaignReceived):
	#Insertamos la campaña
	configTables.BD.metadata.create_all(configTables.engine) #Se crea la BD (o no, dependiendo si se ejecutó antes).
	#Insertamos fecha inicio, fecha fin, email dueño, hashtags y mentions en la tabla Campaign de la BD:
	new_campaignBD=configTables.Campaign(startDate=(datetime.strftime((CampaignReceived.startDate),"%d %m %Y %X")), finDate=(datetime.strftime((CampaignReceived.finDate),"%d %m %Y %X")), email=(CampaignReceived.emailDueño), hashtags=(CampaignReceived.hashtags), mentions=(CampaignReceived.mentions))
	configTables.session.add(new_campaignBD)

	#Y finalmente las agregamos a la BD con estas 3 lineas:
	configTables.session.new
	configTables.session.dirty
	configTables.session.commit() #Para que los cambios se efectivicen en la BD
	return new_campaignBD.id

#manager.deleteCampaignporuser("donaldTrump@gmail.com")
def eliminarCampaignBDxUser(email_user):
	#Pueden ser 1 o mas campañas asociadas a un usuario, elimina TODAS:
	configTables.session.query(configTables.Campaign).filter_by(email=email_user).delete()
	configTables.session.commit()

#manager.deleteCampaignporid(1)
def eliminarCampaignBDxID(idC):
	campaignespecifica = configTables.session.query(configTables.Campaign).get(idC) #Obtengo al camaña con id especifico idC.
	configTables.session.delete(campaignespecifica)
	configTables.session.commit()

#manager.returnCampaign(1)
def retornarCampaignBD(idC):
	print("Campaña retornada:")
	campaignespecifica = configTables.session.query(configTables.Campaign).get(idC)
	#return(campaignespecifica)
	#Que viaje en JSON, no como objeto:
	#campaignJSON=(campaignespecifica).to_json()
	objetoCampaign=Campaign(campaignespecifica.id, campaignespecifica.email, campaignespecifica.hashtags, campaignespecifica.mentions, campaignespecifica.startDate, campaignespecifica.finDate)
	#print(type(objetoCampaign))
	#print(objetoCampaign)
	c=objetoCampaign.to_dict()
	return(c)
	#print(campaignespecifica.id, campaignespecifica.email, campaignespecifica.hashtags, campaignespecifica.mentions, campaignespecifica.startDate, campaignespecifica.finDate) 
    #Devuelve esto: 2 donaldTrump@gmail.com #federicio-#federicio2 @hola-@hola2 2018-11-28 2018-12-02 --> con print envés de return se ve.

#manager.modifyCampaign(2, "email", "calonshi@gmail.com")
#Desde la Interfaz (en ModifCampaign) le llegaría al manager la columna a modificar, el campo para esa columna (inputUser) y el id de campaña.
def modificarCampaignBD(idC, inputColumn, inputUser):
	#Lenguaje MYSQL: UPDATE Campaign SET columna = "inputuser" WHERE id = "idC".
	campaignespecifica = configTables.session.query(configTables.Campaign).get(idC)
	#Hice esto de abajo porque no podía poner campaignespecifica.inputColumn = inputUser, no me toma inputColumn.
	if (inputColumn=="email"):
		campaignespecifica.email = inputUser
		configTables.session.commit()
	
	if (inputColumn=="startDate"):
		campaignespecifica.startDate = inputUser
		configTables.session.commit()
	
	if (inputColumn=="finDate"):
		campaignespecifica.finDate = inputUser
		configTables.session.commit()
	
	if (inputColumn=="hashtags"):
		campaignespecifica.hashtags = inputUser
		configTables.session.commit()
	
	if (inputColumn=="mentions"):
		campaignespecifica.mentions = inputUser
		configTables.session.commit()
	
	#print(campaignespecifica.id, campaignespecifica.email, campaignespecifica.hashtags, campaignespecifica.mentions, campaignespecifica.startDate, campaignespecifica.finDate) 

def insertTweet(TweetInput, idC):
	configTables.BD.metadata.create_all(configTables.engine) #Se crea la BD (o no, dependiendo si se ejecutó antes).
	#Insertamos fecha publicacion, autor, mensaje y macheo en la tabla Tweet de la BD:
	print ("TUIT")
	stringHashtag = listaAString(TweetInput.hashtags) # #donaldTrump-#G20
	stringMention = listaAString(TweetInput.mentions) # @donaldTrump-@miauricioOK
	#print(TweetInput.ID, TweetInput.userName, TweetInput.userID, TweetInput.hashtags ,TweetInput.mentions, TweetInput.date)
	new_TweetBD=configTables.Tweet(idCampaign=(idC), ID=(TweetInput.ID), userName=(TweetInput.userName), userid=(TweetInput.userID), hashtags=(stringHashtag),mentions=(stringMention), date=(TweetInput.date))
	configTables.session.add(new_TweetBD)

	#Y finalmente las agregamos a la BD con estas 3 lineas:
	configTables.session.new
	configTables.session.dirty
	configTables.session.commit()

def returnTweetByIDT(idT):
	print("Tweet retornado:")
	tweetEspecifico = configTables.session.query(configTables.Tweet).get(idT)
	return tweetEspecifico

def returnTweetsByIDC(IDC):
	tweetsBD = configTables.session.query(configTables.Tweet).filter_by(idCampaign=IDC).all()
	print(tweetsBD[1])

	#Nos tiró esto (lista de Tweets en el formato de SQL ALCHEMY): 
	#[<Tweets(ID='112112', userName='MiauricioOK',userid='451325',hashtags='#DonaldNoMeDejes',mentions='@donaldTrump-@G20',date='2018-03-20 21:08:01',idCampaign='3')>, 
	#<Tweets(ID='123456', userName='NASAOk',userid='789456',hashtags='#mars-#venus-#earth',mentions='@NASA-@planets',date='2018-03-20 15:11:01',idCampaign='3')>]
	#Tenemos que separar los tweets y crear objetos tweets. Y hacerles el to json. 
	#Y hacer una lista de esos to json. 
	
	"""
	tweetDict = {
        "id_str" : "123456",
        "user" : {"name" : "NASAOk", "id_str" : "789456"},
        "entities" : {"hashtags" : ["#mars","#venus","#earth"],"user_mentions" : ["@NASA", "@planets"]},
        "created_at" : "Sun Mar 20 15:11:01 +0000 2018",
    }
	

	for t in tweetsBD:
		tweets.append(Tweet(tweet).to_json())
	return tweets
	"""

	#return(campaignespecifica)
	#Que viaje en JSON, no como objeto:
	#campaignJSON=(campaignespecifica).to_json()
	return
	objetoCampaign=Campaign(campaignespecifica.id, campaignespecifica.email, campaignespecifica.hashtags, campaignespecifica.mentions, campaignespecifica.startDate, campaignespecifica.finDate)
	#print(type(objetoCampaign))
	#print(objetoCampaign)
	c=objetoCampaign.to_dict()
	return(c)

#def returnCampaignsInProgress(fecha en formato de fecha)
#HACER FUNCION PARA GABY QUE me da una fecha en formato de Campaña y cuya hora de inicio es menor y hora de fin mayor.
#Todas las campañas que comenzaron pero que no terminaron (todas las campañas en curso)
#DEvolver lista de campañas 

def listaAString(lista):
		string = "-".join(lista)
		return string