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
        conn = self._connect_db()
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
        if self._username is None:
            return "Guest"
        else:
            return self._username

    def islogin(self):
        """
        Function will return the login status for the current user
        """
        return self._login

    def setrole(self,role):
        """
        Function will update the user role 
        """
        self._updaterole(role)
        return

    def _updaterole(self,role):
        """
        Private helper function for set role, function will update the database data
        """
        UPDATE_STRING = "UPDATE {} SET Role = '{}' WHERE Username = '{}'".format(LOGIN_TABLE,role,self._username)
        coon = self._connect_db()
        c = coon.cursor()
        c.execute(UPDATE_STRING)
        coon.commit()
        coon.close()
        return

    def getrole(self):
        """
        Function will return the current user role
        return:
            string : current user role
        """
        return self._role

    def _connect_db(self):
        """
        Function will create a connection for the given name of database
        Precondition:
            db_loca: the location of the database file
        """
        try:
            rv = sqlite3.connect(self._database)
            rv.row_factory = sqlite3.Row
            return rv
        except Exception:
            raise Exception("Can't not find the database file")

    def signup(self,username,password):
        """
        Function will create a new user into database, will check if user is exist
        if it is exist function will return False, success create then it will return True
        Precondition:
            username (string) : username need to create
            password (string) : password for the user
        return :
            True success create, False fail to create
        """
        GET_STRING = "SELECT * FROM {} WHERE Username='{}'".format(LOGIN_TABLE,username)
        PUT_STRING = "INSERT INTO {} VALUES ('{}', '{}', 'USER')".format(LOGIN_TABLE,username,password)
        coon = self._connect_db()
        c = coon.cursor()
        c.execute(GET_STRING)
        data = c.fetchall()

        # Username taken
        if len(data)!=0:
            coon.close()
            return False

        c.execute(PUT_STRING)
        coon.commit()
        coon.close()

        self._username = username
        self._login = True
        self._role = "USER"

        return True
