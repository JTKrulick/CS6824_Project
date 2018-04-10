#export PYTHONPATH="${PYTHONPATH}:/home/jtk0/.local/lib/python2.7/site-packages"
import gzip
import glob, os
import json
import re
import gensim
from gensim.corpora import Dictionary

def forumGeneratorRawString(dataPath= "./data/sample-patients-info.tsv"):
    with open(dataPath, 'r') as data:
        data.next()#skip the column names
        #forum_id\tdiscussion_id\tdiscussion_title\tpost_id\tpost_content\tdatetime\n
            
        for post in data:
            splitFoward = post.strip().split("\t",4)
            splitReverse = splitFoward[4].rsplit("\t",1)#post have tabs
            forum_id = splitFoward[0]
            discussion_id =splitFoward[1]
            discussion_title = splitFoward[2]
            try:
                post_id = int(splitFoward[3])
            except ValueError:
                continue
            post_content = splitReverse[0]
            datetime = splitReverse[1]

            if post_id==0:
                yield discussion_title+" " +post_content
            else:
                yield post_content

def forumGenerator(dictionary=None ,dataPath= "./data/sample-patients-info.tsv", stopWordFile="./data/stopWords.txt"):
    stopWordList=[]
    with open(stopWordFile, 'r') as stopWords:
        for stopWord in stopWords:
          stopWordList.append(stopWord.strip())

    for forumString in forumGeneratorRawString(dataPath):
       removedSC = re.sub('[^A-Za-z 0-9]+', '', forumString)
       wordList = [word for word in removedSC.lower().split() if word not in stopWordList]
       yield dictionary.doc2bow(wordList)


def createDictionary(dictLoc="./data/generated/forumDictionary",useCache=False):
    if (useCache==True and os.path.isfile(dictLoc)):
        dictionary = Dictionary.load_from_text(dictLoc)
    else:
        def wordList(dataPath= "./data/sample-patients-info.tsv"):
            for forumString in forumGeneratorRawString(dataPath):
                removedSC = re.sub('[^A-Za-z 0-9]+', '', forumString)
                yield removedSC.lower().split()
        words = wordList()
        dictionary = Dictionary(words)
        dictionary.save_as_text(dictLoc)
    return dictionary

def lda(topics = 10):
    dic =createDictionary(dictLoc="./data/generated/forumDictionary",useCache=True)
    tg = forumGenerator(dic)
    corpus = []
    for val in tg:
        corpus.append(val)
    lda = gensim.models.ldamodel.LdaModel(corpus,topics,dic)
    return lda


if __name__ == '__main__':
    ldaResult = lda(topics = 10)
    for a in ldaResult.print_topics(10):
        print a
