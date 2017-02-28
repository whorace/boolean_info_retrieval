class Entry:
    def __init__(self, posting_id, article):
        self.posting_id = posting_id
        self.title = article["title"]
        self.text = article["text"]
        self.abstractOfText = article["text"][:500]
