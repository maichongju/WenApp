from sqlite3 import dbapi2 as sqlite3

def connect_db(db_loca):
    """
    Function will create a connection for the given name of database
    Precondition:
        db_loca: the location of the database file
    """
    try:
        rv = sqlite3.connect(db_loca)
        rv.row_factory = sqlite3.Row
        return rv
    except Exception:
        raise Exception
    
