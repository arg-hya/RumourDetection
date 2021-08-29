import matplotlib.pyplot as plt

import json

# import the module
import tweepy

# assign the values accordingly
from Twitter15 import readFile, makeGraphDB
from Twitterutils import makeGraph, convertTwitterTime, test

consumer_key = "xxxxx"
consumer_secret = "xxxx"
access_token = "xxxx"
access_token_secret = "xxxx"

# authorization of consumer key and consumer secret
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

# set access to user's access key and access secret
auth.set_access_token(access_token, access_token_secret)

# calling the api
print("Calling API...")
api = tweepy.API(auth, wait_on_rate_limit = True, wait_on_rate_limit_notify = True)

def getVertexs() :
    filePath = 'D:/Twitter/FakeNewsNet-master/FakeNewsNet-master/code/fakenewsnet_dataset/politifact/fake/politifact14745/retweets/929507659073687552.json'
    with open(filePath) as f:
        retweet_dict = json.load(f)

    print("Json loaded")

    count = 0
    list_id = []
    for retweet in retweet_dict['retweets'] :
        id = retweet['user']['id']
        count = count + 1
        list_id.append(id)

    print('Total IDs : ', count)
    # Creating an empty dictionary
    myDict = {}

    for id in list_id :

        print("Count = ", count, "ID = ", id)
        count = count - 1
        temp_list = []
        print("Calling friends API...")
        try:
            temp_list = api.friends_ids(id)
        except tweepy.TweepError:
            print("can't get records from this user, probably a protected account and it is safe to skip")
            pass
        #for frnd in friends :
        #    print("Friend = ", frnd.screen_name)
        #    temp_list.append(frnd.id)
        print(id , " has " , str(len(temp_list)) , " friends.")

        myDict[id] = temp_list

    print("Saving in json...")
    with open('Id2Followers.json', 'w') as fp:
        json.dump(myDict, fp)

# Defining main function
def main():
    #print("Program started...")
    #getVertexs()
    #print("Making graph...")
    #print(convertTwitterTime("Wed Nov 15 02:09:50 +0000 2017"))
    #test()
    makeGraphDB()
    #makeGraph()


# Using the special variable
# __name__
if __name__ == "__main__":
    main()