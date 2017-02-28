import json
class LoadArticle:

    def __init__(self,path):
        self.path = path
        with open(self.path, 'r') as f:
            self.dic = json.load(f)

    def findArticle(self,posting_id):
        return self.dic[posting_id]
