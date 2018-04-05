#export PYTHONPATH="${PYTHONPATH}:/home/jtk0/.local/lib/python2.7/site-packages"
import gzip
import glob, os
import json
currentFullTweet = ""#TODO delete

def tweetGenerator(tweetFolderPath= "./data/tweets"):
    files = glob.glob(tweetFolderPath +"/*.gz")
    for currentFile in files:
        with gzip.open(currentFile,"rb") as file:
            for line in file:
                jsonTweet = json.loads(line)
                global currentFullTweet#TODO delete
                currentFullTweet = jsonTweet#TODO delete

                if tweetFilter(jsonTweet)  == False:
                    continue
                tweet = wordFilter(jsonTweet)
                yield tweet


#determine if this is a valid/useful tweet
def tweetFilter(jsonTweet):
    if 'delete' in jsonTweet:
        return False
    if jsonTweet['lang'] != 'en':
        return False
    if len(jsonTweet['entities']['urls']) != 0:
        return False
    return True

#given a valid tweet, transform json into a useful tweet line
#including things such as stop words
def wordFilter(jsonTweet):
    #Something like a stop list would go here
    hashtags = " ".join([a['text'] for a in jsonTweet['entities']['hashtags']])
    return jsonTweet['text']+" " + hashtags



if __name__ == '__main__':
    tweets=tweetGenerator()
    for tweet in tweets:
        print tweet
