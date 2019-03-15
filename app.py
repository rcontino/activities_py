from flask import Flask, render_template, json, request
import connection as c

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
        c.insert( _activityName, _description )
    else:
        print( "Invalid input")

if __name__ == "__main__":
    app.run()