# PDI-TweetMaster

>Thanks thanking your time in finding TweetMaster!
>
>This RESTful API is a college's project, so expect mediocre code and a lot of to-do's.
>
>Autors: Federico Calonge, Juan David, Gabriel Torrandella
>Professor: Juan Lagostena

## Setting Up TweetMaster

### Requirements

Install the packages in here. The easiest way is using **pip3**, as the API is made in Python 3.5.

>pip3 install -r requirements.txt

### Setting up the database

TweetMaster uses a MySQL database during operations.  
Fortunately, the necesary set-up is controlled by the app during it's first execution.  
Worry no more!

### Setting up the scheduler

The Scheduler is a small Python module accessed once every 5 minutes.  
To do that, it is necesary to create a _cron job_ that executes the module every 5 minutes.

First, look up the Python 3 path using **which**. If you are using a virtual enviroment, executute this command while working on it.  
>which python3

This will return your Python 3 path.

Now add a the next cron job. (To add a cron job, use **crontab -e**):  
>*/5 * * * * PYTHONPATH {path to scheduler.py}/scheduler.py
