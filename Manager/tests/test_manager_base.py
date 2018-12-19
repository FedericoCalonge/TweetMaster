'''
Created on Dec 12, 2018

@author: Gabriel Torrandella
'''
import unittest

from Campaign.Campaign import Campaign


class test_manager_base(unittest.TestCase):

    
    campaignCreationData = {'email':'hype@example.com', 
                                 'hashtags':['#JOKER','#SMASH'], 
                                 'mentions':['@Sora_Sakurai'],
                                 'startDate':"06 12 2018 23:20:00",
                                 'endDate':"07 12 2018 00:30:00"}
    
    campaignCreationDataError = {'hashtags':'#JOKER-#smash', 
                                 'mentions':'@Sora_Sakurai',
                                 'startDate':"06 12 2018 23:20:00",
                                 'endDate':"07 12 2018 00:30:00"}
    
    campaignDeleteByIDCData = {'idC':1}
    campaignDeleteByEmailData = {'email':"b@example.com"}
    campaignDeleteDataError = {'hype':"JOKER_IN_SMASH"}
    
    campaignPatchData = {'idC':3}


    initialCampaigns = [Campaign(1, "a@example.com", '#NothingBreaksLikeAHeart', "", "06 12 2018 23:20:00", "07 12 2018 00:30:00"),
                        Campaign(2, "b@example.com", "", '@POTUS', "06 12 2018 23:20:00", "07 12 2018 00:30:00"),
                        Campaign(3, "c@example.com", '#nintendo-#SMASH', '@Sora_Sakurai-@nintendo', "06 12 2018 23:20:00", "07 12 2018 00:30:00")]
    
    def setUp(self):
        pass
        
    def tearDown(self):
        pass

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()