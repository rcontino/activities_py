import pymysql, json

def connect () :
    connection = pymysql.connect( host="", user="", passwd="", db="" )
    cursor = connection.cursor()
    return connection, cursor

def executeInsert ( cursor, _activityName, _description ) :
    insert = "INSERT INTO `proposed_activities` (timestamp, name, description, score, post_id) VALUES (CURRENT_TIMESTAMP, '" + _activityName + "', '" + _description + "' , '0', '54');"
    connection, cursor = connect()
    cursor.execute( insert )
    connection.commit()

    for name, score in cursor.fetchall() :
        print ( name, score )

    connection.close()

def insert ( _activityName, _description ) :
    connection, cursor = connect()
    executeInsert ( cursor, _activityName, _description )
    print("Proposed Activity Inserted")
    connection.close()

def updateVoteScore (  newScore, postId, activity ) :
    connection, cursor = connect()
    query = "UPDATE proposed_activities SET score = " + str(newScore) + " WHERE post_id = " + str(postId) + " AND name = '" + activity[0] + "';"
    print (query)
    cursor.execute( query )
    connection.commit()
    print("Score updated")
    connection.close()

def updateCommentStatus ( postId ) :
    connection, cursor = connect()
    query = "UPDATE wp_posts SET comment_status = 'closed' WHERE ID = " + str(postId) + ";"
    print (query)
    cursor.execute( query )
    connection.commit()
    print("Comment Status updated")
    connection.close()    

def getDataByParameter ( column, specifier, specifierColumn, table ) :
    connection, cursor = connect()
    query = "SELECT " + column + " FROM " + table + " WHERE " + specifierColumn + " = '" + specifier + "';"
    print(query)
    cursor.execute( query )

    results = []
    for column in cursor.fetchall():
        results.append( column )

    connection.close()

    return results

def getDataByQuery ( query ) :
    connection, cursor = connect()
    cursor.execute( query )

    posts_dict = []
    for post in cursor.fetchall():
        post_dict = {
                'name': post[0]
        }
        posts_dict.append(post_dict)

    connection.close()    

    print(json.dumps(posts_dict))
    return json.dumps(posts_dict)
     