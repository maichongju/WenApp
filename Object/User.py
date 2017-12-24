#from DataBase import connect_db
from sqlite3 import dbapi2 as sqlite3
LOGIN_TABLE = "Login"

class User:

    def __init__(self,database):
        """
        username (string) : Current user username
        login (boolean) : True if has login, otherwise false
        role (string) : if the user loggin then shwo the role for the current user
        database (string) : database location 
        """
        self._username = None
        self._login = False
        self._role = None
        self._database = database

    def login(self,username,password):
        """
        Function will compare the given username and password to the database, 
        if the database has a match for the password and the password then function 
        will return True, otherwise return false
        Precondition:
            username (string) : username need to be check
            password (string) : password need to be check
        """
        db_string = "SELECT * FROM {} WHERE Username='{}' and Password='{}'".format(LOGIN_TABLE,username,password)
        conn = self._connect_db(self._database)
        c = conn.cursor()
        c.execute(db_string)
        data = c.fetchall()
        conn.close()
        if len(data) == 1:
            self._login = True
            self._username = data[0][0]
            self._role = data[0][2]
        return self._login

    def logout(self):
        """
        Function will logout user which will reset all the information for User class
        """
        self._username = None
        self._login = False
        self._role = None
        return

    def getusername(self):
        """
        Function will return the current username 
        """
        if self._username == None:
            return "Guest"
        else:
            return self._username

    def islogin(self):
        """
        Function will return the login status for the current user
        """
        return self._login

    def getrole(self):
        """
        Function will return the current user role
        return:
            string : current user role
        """
        return self._role

    def _connect_db(self,db_loca):
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
            raise Exception("Can't not find the file")