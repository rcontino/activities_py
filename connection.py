import pymysql

def doQuery( myConnection, _activityName, _description ) :
    cur = myConnection.cursor()
    insert = "INSERT INTO `proposed_activities` (timestamp, name, description, score, post_id) VALUES (CURRENT_TIMESTAMP, '" + _activityName + "', '" + _description + "' , '0', '10');"
    cur.execute( insert )
    myConnection.commit()

    for name, score in cur.fetchall() :
        print ( name, score )

def insert( _activityName, _description ) :
    myConnection = pymysql.connect( host="", user="", passwd="", db="" )
    doQuery( myConnection, _activityName, _description )
    myConnection.close()