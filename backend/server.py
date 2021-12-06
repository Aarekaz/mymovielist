from flask import Flask,url_for,json,request,jsonify
import os


app = Flask(__name__)

@app.route("/json")
def json_example():
    path = os.path.realpath(os.path.dirname(__file__))
    # Join various path components
    json_url = os.path.join(path,"notebooks\\json_data", "data.json")
    data = json.load(open(json_url))
    return jsonify(data)

if __name__  == "__main__":
    app.run(debug=True)