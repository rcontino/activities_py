from flask import Flask, render_template, json, request
from datetime import datetime, timedelta
from dateutil import parser
import connection as c

app = Flask(__name__)

@app.route("/")
def main():
    return render_template('index.html')

@app.route("/closecomments")
def closeComments():
    posts = c.getDataByParameter('ID', 'publish', 'post_status', 'wp_posts')
    for post in posts :
        postDate = c.getDataByParameter('post_date', str(post[0]), 'ID', 'wp_posts')
        pyDate = datetime.strptime(str(postDate[0][0]), '%Y-%m-%d %H:%M:%S')
        delta = datetime.now() - pyDate
        print(delta)

        if (delta > timedelta(days = 7)):
            c.updateCommentStatus(post[0])

    return render_template('commentsClosed.html')

@app.route("/tally")
def tallyVotes():
    print("In tally")
    posts = c.getDataByParameter('ID', 'publish', 'post_status', 'wp_posts')
    for post in posts :
        activityNames = c.getDataByParameter( 'name', str(post[0]), 'post_id', 'proposed_activities' )
        for activity in activityNames :
            activityVotes = 0
            comments = c.getDataByParameter('comment_content', str(post[0]), 'comment_post_ID', 'wp_comments')
            for comment in comments :
                if ((activity[0].lower() in comment[0].lower()) and ('yes' in comment[0].lower())) :        
                    activityVotes = activityVotes + 1

            c.updateVoteScore( activityVotes, post[0], activity )

    return render_template('tallied.html')

@app.route("/submit", methods=['POST'])
def submit():

    print("Before")

    # read the posted values from the UI
    _activityName = request.form['activityName']
    print("ActivityName: " + _activityName)
    _description = request.form['inputDescription']
    print("Description: " + _description)
    _postName = request.form['postName']
    print("PostName: " + _postName)

    # validate the received values
    if _activityName and _description and _postName:
        c.insert( _activityName, _description, _postName )
    else:
        print( "Invalid input")

@app.route('/getActivePosts')
def getActivePosts():
    print("getActivePosts was called successfully")
    query = "SELECT post_name FROM wp_posts WHERE post_status = 'publish' AND comment_status = 'open'"
    postJson = c.getDataByQuery( query )

    return postJson

if __name__ == "__main__":
    app.run()