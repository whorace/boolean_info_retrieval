import json
import string
import sys
from stemmer import PorterStemmer
reload(sys)
sys.setdefaultencoding('utf-8')
class Index:
    def __init__(self, loadpath, outputpath):
        self.load_path = loadpath
        self.output_path = outputpath

    def loadData(self):
        dic = {}
        with open(self.load_path, 'r') as f:
            dic = json.load(f)
        #print dic
        return dic
    def run(self):
        self.indexDic = {}
        dic = {}
        dic = self.loadData()
        self.tokenize(dic)
        self.outputToFile(self.indexDic)
    def tokenize(self,dic):
        i = 0
        for k, v in dic.iteritems():
            #page
            page = int(str(k))
            listOfTitleAndText = []
            titleAndText = ""
            # print page
            # print type(page)
            # i = i+1
            # print i
            for key, value in v.iteritems():
                keyStr = str(key)
                valueStr = str(value)
                #print type(keyStr)

                if keyStr == 'title':
                    keyStr = self.offpunctuation(keyStr)
                    #print 'test: title   ' + valueStr
                    titleAndText = titleAndText + " " + valueStr

                if keyStr == 'text':
                    valueStr = self.offpunctuation(valueStr)
                    #print 'test: text   ' + valueStr
                    titleAndText = titleAndText + " " + valueStr
            # lowercase
            titleAndText = titleAndText.lower()
            # split into list
            listOfTitleAndText = titleAndText.split()
            # addToIndexDic
            for element in listOfTitleAndText:
                # ignore the stop words
                if self.checkIgnoreStopWords(element):
                    pass
                else:
                    #stemming the element
                    element = self.stemming(element)
                    self.addToIndexDic(element, page)



    # clear all punctuations in string
    def offpunctuation(self, string):
        string = str.translate(string, None,'~`!@#$%^&*()_+=-[]\|}{;:/><,.?\"\'')
        return string
    # check whether it is a stop word
    def checkIgnoreStopWords(self, term):
        list = ['a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from', 'has', 'he', 'in', 'is', 'it', 'its', 'of', 'on', 'that', 'the', 'this', 'to', 'was', 'were', 'will', 'with']
        for element in list:
            if term == element:
                return True
        return False
    # using PorterStemmer to do stemming
    def stemming(self, term):
        output = ""
        stem1 = PorterStemmer()
        output = stem1.stem(term)
        return output



    # testFile
    def testFile(self, string):
        text_file = open("testFile.txt", "w")
        text_file.write(string)
        text_file.close()
    # add the posting list with term
    def addToIndexDic(self, term, page):
        #postingList = []
        if self.indexDic.has_key(term):

            # postingList = self.indexDic[term]
            # print postingList
            if(self.checkEleHelper(self.indexDic[term], page)):
                #do nothing
                pass
            else:
                value = self.indexDic[term]
                # print "test"
                # print value
                # print type(value)
                value.append(page)
                self.indexDic[term] = value
        else:
            list = []
            list.append(page)
            self.indexDic[term] = list

    # check whethter the element is in the list
    def checkEleHelper(self, ls, element):
        for ele in ls:
            if ele == element:
                return True
        return False
    # output the index to index.json
    def outputToFile(self, dic):
        with open(self.output_path,'w') as f:
            f.write(json.dumps(dic))
            print "done"
