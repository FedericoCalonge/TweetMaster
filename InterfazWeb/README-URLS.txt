Urls que puede acceder el usuario:

/index: home de la app. 	-->index.html con enlaces a las URLs de abajo:

/Campaign:             -->Alta y Baja de Campa�a. 
	/Campaign/Alta -->Alta de Campa�a. AltaCampaign.html
	/Campaign/Baja -->Baja de Campa�a. BajaCampaign.html
	/Campaign/Modificacion -->Modificacion de Campa�a. ModifCampaign.html
	/GET/#CampaignID:  	-->Luego de hacer el alta. Hacer el html directamente con Flask que diga
	el status code correspondiente y el id de la campa�a creada. (Ver los Status codes disponibles en /doc). 
	Por ej. si se cre� satisfactoriamente --> "202 created. Campa�a #IdCampa�a creada."	
	/DELETE/#CampaignID:  	-->Luego de hacer la eliminaci�n. Hacer el html directamente con Flask que diga
	el status code correspondiente y el id de la campa�a eliminaci�n. (Ver los Status codes disponibles en /doc).
	/PUT/#CampaignID:       -->Luego de indicar los campos a cambiar.

/Reporter:             -->Obtenci�n del reporte.
	/GET/ReporterRaw  -->Obtenci�n del reporte Raw.
	/GET/ReporterJSON -->Obtenci�n del reporte JSON.
	[En estos 2 GET tambien se tendr�an que mostrar los status codes como en los GET y DELETE de Campaign de arriba
	 --> estos est�n en SWAGGER. Hay que implementarlos con FLASK].

/doc: Documentacion de la API con Swagger.  --> 