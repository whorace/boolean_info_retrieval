from index import Index
import time

class Control:
    def __init__(self, load_path, output_path):
        startTime = time.time()
        print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(startTime))

        # self.load_path = 'json/films_corpus.json'
        # self.output_path = 'json/index_films.json'
        self.load_path = load_path
        self.output_path = output_path

        ##########
        # load_path = 'json/test_corpus.json'
        # output_path = 'json/index_test.json'
        ##########

        index1 = Index(self.load_path, self.output_path)
        index1.run()



        endTime = time.time()
        print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(endTime))
        seconds = endTime - startTime
        print seconds
