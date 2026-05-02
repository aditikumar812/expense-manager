from flask import Flask
app=Flask(__name__)

@app.route("/")#The important thing is the @app.route("/") above it  tells Flask "when someone visits the homepage, run whatever function is below me.
def home():
    return ('Hello World')

if __name__=="__main__":
    app.run(debug=True)

