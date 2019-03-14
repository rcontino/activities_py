from flask import Flask, render_template, json, request
app = Flask(__name__)

@app.route("/")
def main():
    return render_template('index.html')

@app.route("/submit", methods=['POST'])
def submit():

    # read the posted values from the UI
    _activityName = request.form['activityName']
    _description = request.form['description']

    # validate the received values
    if _activityName and _description:
        return json.dumps({'html':'<span>All fields good !!</span>'})
    else:
        return json.dumps({'html':'<span>Enter the required fields</span>'})

if __name__ == "__main__":
    app.run()