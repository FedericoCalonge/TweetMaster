# PDI-TweetMaster
>This RESTful API is a college's project, so expect mediocre code and a lot of to-do's.
>
>Autores: Federico Calonge, Juan David, Gabriel Torrandella.
>
>Profesor: Juan Lagostena.

## Setting Up TweetMaster

### Requirements

Python 3.5.2+

Instalar los paquetes que hay en el proyecto; la manera más facil es utilizando **pip3**:
```
pip3 install -r requirements.txt
```

### Setting up the database

TweetMaster usa una base de datos MySQL durante sus operaciones. El set-up y creación de la BD es controlada por la app durante la 1ra ejecucion (por esto NO es necesario crear la BD previamente). 

Lo que si se debe hacer es **modificar** la linea 9 del archivo _configtables.py_ ubicado en la carpeta _DataBaseConnector_ dependiendo de la conexión con la BD en MySQL. En nuestro caso, utilizamos la conexión a nuestra BD en MySQL desde nuestro localhost (en el puerto 3306) mediante el usuario root y la password 4236. De acuerdo a esto, la linea 9 la completamos así:
```
Linea 9 → engine = create_engine("mysql+pymysql://root: 4236@localhost :3306/BDTweetMaster?charset=utf8",echo=True)
```

### Setting up the servers

Ejecutar en diferentes terminales: _start_manager_, _start_fetcher_ y _start_reporter_, del directorio root de TweetMaster. El órden es indistinto.
Los servers vivirán en:  
 * Manger:   127.0.0.1/5000
 * Fetcher:  127.0.0.1/5001
 * Reporter: 127.0.0.1/5002
 
### Setting up the scheduler

El Scheduler es un pequeño módulo de Python que es accedido cada 5 minutos. Para hacer esto, es necesario crear un _cron job_ que ejecutará el módulo cada 5 minutos. 

Para añadir el _cron job_ se debe ejecutar **crontab -e**. Esto abrirá un editor de texto; y se deberá añadir esto al final de las lineas: 
```
*/5 * * * * cd {path to TweetMaster root} && PYTHONPATH Scheduler/scheduler.py
```
Donde:
 * "path to TweetMaster root" es el path desde el root al directorio root de TweetMaster. 
   * /dir1/dir2/dir3/TweetMaster
 * "PYTHONPATH" es el path del interprete de Python3.
   * Si _NO_ estamos usando un entorno virtual, se debe reemplazar esto con _python3_
   * _SI_ estamos utilizando un entorno virtual, se debe obtener el path ejecutando **which python3** cuando estemos trabajando dentro del entorno virtual. 

### Opcional: Setting up the Swagger tool

Hay documentación en Swagger para la API TweetMaster.  Es un servidor incluído con la aplicación. 
Para correr el servidor, se debe ejecutar lo siguiente (desde el directorio root): 
```
python3 -m swagger_server
```
Y luego abrir el navegador en...:
```
http://localhost:8080/FedericoCalonge/TweetMaster/1.0.0/ui/
```

### Para mayor información ver el archivo "Escenarios de prueba API y Mejoras" donde se realizaron pruebas mediante POSTMAN y se especifican las mejoras en la API. 
