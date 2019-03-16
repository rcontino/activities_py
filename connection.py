import pymysql

def connect () :
    myConnection = pymysql.connect( host="", user="", passwd="", db="" )
    return myConnection

def executeInsert ( myConnection, _activityName, _description ) :
    cur = myConnection.cursor()
    insert = "INSERT INTO `proposed_activities` (timestamp, name, description, score, post_id) VALUES (CURRENT_TIMESTAMP, '" + _activityName + "', '" + _description + "' , '0', '47');"
    cur.execute( insert )
    myConnection.commit()

    for name, score in cur.fetchall() :
        print ( name, score )

def insert ( _activityName, _description ) :
    myConnection = connect()
    executeInsert ( myConnection, _activityName, _description )
    myConnection.close()

def getComments ( postId ) :
    myConnection = connect ()
    cur = myConnection.cursor()
    query = "SELECT comment_content FROM wp_comments WHERE comment_post_ID = '" + postId + "';"
    cur.execute( query )

    comments = []
    for comment_content in cur.fetchall() :
        comments.append ( comment_content )

    return comments

def getActivityNames ( postId ) :
    myConnection = connect ()
    cur = myConnection.cursor()
    query = "SELECT name FROM proposed_activities WHERE post_id = '" + postId + "';"
    cur.execute( query )

    activityNames = []
    for name in cur.fetchall() :
        activityNames.append ( name )

    return activityNames

def getActivityScore ( name ) :
    myConnection = connect ()
    cur = myConnection.cursor()
    query = "SELECT score FROM proposed_activities WHERE name = '" + name[0] + "';"
    cur.execute( query )

    score = cur.fetchone()

    return score    

def updateVoteScore (  newScore, postId, activity ) :
    myConnection = connect ()
    cur = myConnection.cursor()
    query = "UPDATE proposed_activities SET score = " + str(newScore) + " WHERE post_id = " + postId + " AND name = '" + activity[0] + "';"
    print (query)
    cur.execute( query )
    myConnection.commit()