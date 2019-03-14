from flask import Flask, render_template, json, request
import connection

app = Flask(__name__)

@app.route("/")
def main():
    return render_template('index.html')

@app.route("/submit", methods=['POST'])
def submit():

    # read the posted values from the UI

    _activityName = request.form['activityName']
    _description = request.form['inputDescription']

    # validate the received values
    if _activityName and _description:

        print("More to come here")
    else:
        return json.dumps({'html':'<span>Enter the required fields</span>'})


if __name__ == "__main__":
    app.run()