from flask import Flask, render_template, request, redirect
from searchEngine import SearchEngine

app = Flask(__name__)
se = SearchEngine("index")


@app.route("/")
def redir():
    return render_template("index.html")


# POST REQUEST TO GET RESULTS
# CHECK IF USER ACTUALLY SUBMITS A QUERY LATER!
@app.route("/results", methods = ['POST', 'GET'])
def getResults():
    if request.method == "POST":
        query = request.form["query"]
        results = se.search(query, 5)
        return render_template("results.html", results = results)

@app.route("/back")
def goBack():
    return render_template("index.html")




# main function
if __name__ == "__main__":
    app.run()