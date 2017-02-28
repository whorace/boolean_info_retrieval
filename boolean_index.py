import os
import math
import urllib
from flask import *
from search import Search
from load_article import LoadArticle
from entry import Entry
from control import Control
app = Flask(__name__)

path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
data_path =  path + '/a3/json/films_corpus.json'
index_path = path + '/a3/json/index_films.json'

########## test data ##################
# data_path = path + '/a3/json/test_corpus.json'
# index_path = path + '/a3/index_test.json'
######################################
print "Loading data from corpus and create a new index..."
control1 = Control(data_path, index_path)
print "New index is created!!!"
loadArticle1 = LoadArticle(data_path)
search1 = Search(index_path, data_path)

@app.route("/")
@app.route("/index")
def search():
    print "test"
    return render_template('index.html')


@app.route("/results", methods=['GET'])
def results():
    try:
        text = str(request.args.get('query')).strip()
        current_page = int(request.args.get('page'))




        if text == "" or text == None:
            return render_template('index.html')

        search_results, warning = search1.dummy_search(str(text))

        if search_results == None:
            return render_template('serp.html', mode=0, results="", warning=warning, text=text,
                                    num_of_article=0, pages=0, current_page=current_page,
                                    query=urllib.quote_plus(text))

        else:

            num_of_article = len(search_results)
            #print num_of_article
            arc_per_page = 10
            start_arc = (current_page - 1) * arc_per_page
            end_arc = start_arc + arc_per_page

            res = search1.getArticleList(search_results[start_arc : end_arc])

            pages = int(math.ceil(num_of_article/float(arc_per_page)))
            #print pages
            if warning == None:
                return render_template('serp.html', mode=1, results=res, warning="None", text=text,
                                    num_of_article=num_of_article, pages=pages, current_page=current_page,
                                    query=urllib.quote_plus(text))
            else:
                return render_template('serp.html', mode=1, results=res, warning=warning, text=text,
                                    num_of_article=num_of_article, pages=pages, current_page=current_page,
                                    query=urllib.quote_plus(text))
    except KeyError:
        return "Problem"

@app.route('/<posting_id>')
def show_detail(posting_id):
    objOfArticle = loadArticle1.findArticle(posting_id)
    entry2 = Entry(posting_id, objOfArticle)
    return render_template('article.html', article=entry2)

if __name__ == "__main__":
    app.run()
    # app.run(debug = True)
