from sqlite3 import dbapi2 as sqlite3
LOGIN_TABLE = "Login"

SERVER_UNVALIABLE = "Server Out of Server"
PASSWORD_NOT_MATCH = "User name or Password are not match to our record"

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
        self._id = None
        self._database = database



    def login(self,username,password):
        """
        Function will compare the given username and password to the database,
        if the database has a match for the password and the password then function
        will return True, otherwise return false
        Precondition:
            username (string) : username need to be check
            password (string) : password need to be check
        return:
            True if successed login, false otherwise
        """
        # ('UserId','Username','Password','Role')
        data,error = self._check_password(username,password)
        if data is False:
            return self._login,error
        else:
            self._login = True
            self._id = data[0]
            self._username = data[1]
            self._role = data[3]
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
        self._role = role
        return

    def _updaterole(self,role):
        """
        Private helper function for set role, function will update the database data
        Precondition:
            role (string) : role for the database
        """
        UPDATE_STRING = "UPDATE {} SET Role = '{}' WHERE Username = '{}'".format(LOGIN_TABLE,role,self._username)
        self._database.setdata(UPDATE_STRING)
        return

    def getrole(self):
        """
        Function will return the current user role
        return:
            string : current user role
        """
        return self._role

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
        PUT_STRING = "INSERT INTO {} VALUES ('{}', '{}', 1)".format(LOGIN_TABLE,username,password)
        if self._has_user(username):
            return False

        self._database.setdata(PUT_STRING)

        self._username = username
        self._login = True
        self._role = 1

        return True

    def delete_account(self):
        """
        Function will delete the current account
        """
        DELETE_STRING = "DELETE FROM {} WHERE Username = '{}'".format(LOGIN_TABLE,self._username)
        self._database.setdata(DELETE_STRING)
        self.logout()
        return

    def update_password(self,old,new):
        """
        Function will update the password for the user, function will check
        if the old password is match, if match then will update the password
        Precondition:
            old (string) : old password
            new (string) : new password
        """
        result = self._check_password(self._username,old)
        if result is False:
            return False
        else:
            self._update_password(new)

        return True

    def _update_password(self,password):
        """
        Function will update the password in the databse for the current user
        """
        UPDATE_STRING = "UPDATE {} SET Password = '{}' WHERE Username = '{}'".format(LOGIN_TABLE,password,self._username)
        self._database(UPDATE_STRING)
        return

    def _check_password(self,username,password):
        """
        Function will check if the password match the data,
        if match function will return the data for the user
        Precondition:
            username (string) : username for the user
            password (string) : password for the user
        """
        GET_STRING = "SELECT * FROM {} WHERE Username='{}' and Password='{}'".format(LOGIN_TABLE,username,password)
        data = self._database.getdata(GET_STRING)
        if data is None:
            return False,SERVER_UNVALIABLE
        if len(data) == 0:
            return False, PASSWORD_NOT_MATCH
        return data[0]

    def _has_user(self,username):
        """
        Function will check if the the given username is in the database
        if user in the database, then return true, otherwiase false
        Precondition:
            username (string) : username for check in the database
        """
        GET_STRING = "SELECT * FROM {} WHERE Username='{}'".format(LOGIN_TABLE,username)
        data = self._database.getdata(GET_STRING)
        if len(data)!=0:
            return True
        else:
            return False
