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

        return False

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