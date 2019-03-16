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

    tallyVotes()

def tallyVotes():
    # Get comments by post ID
    id = "47"
    activityNames = c.getActivityNames( id )
    comments = c.getComments( id )

    for activity in activityNames :
        # check to see if the comment contains one of the activity names and 'yes'
        # if yes, update the proposed activity with the same name and post_id
        for comment in comments :
            if ((activity[0] in comment[0]) and ('yes' in comment[0])) :        
                priorScore = c.getActivityScore( activity )
                newScore = priorScore[0] + 1
                print (activity, comment, newScore)
                c.updateVoteScore( newScore, id, activity )







if __name__ == "__main__":
    app.run()