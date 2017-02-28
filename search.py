import json
import string
import sys
from stemmer import PorterStemmer
from entry import Entry
reload(sys)
sys.setdefaultencoding('utf-8')

class Search:
    def __init__(self, path_index, path_corpus):
        self.path_index = path_index
        self.path_corpus = path_corpus

    def loadData(self):
        dic = {}
        with open(self.path_index, 'r') as f:
            dic = json.load(f)
            #print dic
        return dic

    def loadArticleData(self):
        dic = {}
        with open(self.path_corpus, 'r') as f:
            dic = json.load(f)
        #print dic
        return dic

    def getArticleList(self, listOfPostId):
        articleList = []
        dic = {}
        dic = self.loadArticleData()
        for id in listOfPostId:
            for k, v in dic.iteritems():
                if id == int(str(k)):
                    entry1 = Entry(k,v)
                    articleList.append(entry1)
                    # article = ""
                    # for key,value in v.iteritems():
                    #     keyStr = str(key)
                    #     valueStr = str(value)
                    #     if keyStr == 'title':
                    #         article = article + valueStr + "NEWLINE"
                    #     if keyStr == 'text':
                    #         article = article + valueStr
                    # articleList.append(article)
        return articleList

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
    # find posting list
    def findPostingList(self, term):
        dic = {}
        ls = []
        dic = self.loadData()
        ls = dic[term]
        ls.sort()
        return ls
    # check whether the element is in the dictionary.
    def checkEleInTheDic(self, term):
        dic = {}
        dic = self.loadData()
        if dic.has_key(term):
            return True
        else:
            return False

    # get the intersected list
    def intersection(self, list1, list2):
        output = []
        for v1 in list1:
            for v2 in list2:
                if v1 == v2 and v1 not in output:
                    output.append(v1)
        return output

    def dummy_search(self, query):
        res_list = []
        query_list = []
        query_list = query.split()
        i = 0
        j = 0
        ls = []
        warning = ""
        terms = ""
        ignore = "Ignoring term: "
        # the only one query
        if len(query_list) == 1:
            query1 = query_list[0]
            query1 = self.stemming(query1)
            if self.checkIgnoreStopWords(query1):
                warning = "Ignoring term: " + query1
                return None, warning

            else:
                if self.checkEleInTheDic(query1):
                    res_list = self.findPostingList(query1)
                    #res_list = self.getArticleList(res_list)
                    return res_list, None
                else:
                    warning = 'Unknown search term '+query1+' and return 0 results.'
                    return None, warning

        # more than one query
        else:
            for term in query_list:
                # pass the stopword
                j = j + 1
                if self.checkIgnoreStopWords(term):
                    terms = terms + " " + term

                else:
                    i = i + 1
                    #print i
                    #print "j:"+str(j)
                    afterStemTerm = self.stemming(term)
                    if self.checkEleInTheDic(afterStemTerm):
                        if i == 1:
                            ls = self.findPostingList(afterStemTerm)
                            #print "test1"
                        else:
                            ls = self.intersection(ls, self.findPostingList(afterStemTerm))
                            #print "test2"
                        if terms == "":
                            if len(ls) == 0:
                                warning = 'Unknown search term '+query+' and return 0 results.'
                                if j == len(query_list):
                                    return None, warning
                            else:
                                if j == len(query_list):
                                    return ls, None
                        else:
                            if len(ls) == 0:
                                warning = ignore + terms
                                warning = warning +  '. Unknown search term '+query+' and return 0 results.'
                                if j == len(query_list):
                                    return None, warning
                            else:
                                warning = ignore + terms
                                if j == len(query_list):
                                    return ls, warning
                    else:
                        warning = 'Unknown search term '+query+' and return 0 results.'
                        return None, warning

            return None, "Ignoring terms: " + terms
