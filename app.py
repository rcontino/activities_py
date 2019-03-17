from flask import Flask, render_template, json, request
from datetime import datetime, timedelta
from dateutil import parser
import connection as c

app = Flask(__name__)

@app.route("/")
def main():
    tallyVotes()
    expirePosts()
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
        
def tallyVotes():
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

def expirePosts():
    print("Expiring posts")
    posts = c.getDataByParameter('ID', 'publish', 'post_status', 'wp_posts')
    for post in posts :
        postDate = c.getDataByParameter('post_date', str(post[0]), 'ID', 'wp_posts')
        pyDate = datetime.strptime(str(postDate[0][0]), '%Y-%m-%d %H:%M:%S')
        delta = datetime.now() - pyDate
        print(delta)

        if (delta > timedelta(days = 7)):
            c.updateCommentStatus(post[0])

if __name__ == "__main__":
    app.run()