'''
Created on Dec 10, 2018

@author: Gabriel Torrandella
'''
import sys
from os import path

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from Manager.manager import Manager


class Scheduler():
    
    def keepSchedule(self):
        Manager().fetchCampaings()
        
Scheduler().keepSchedule()


