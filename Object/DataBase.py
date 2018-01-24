import pyodbc as sql
from configparser import ConfigParser
from mysql.connector import connect
from mysql.connector.errors import ProgrammingError

class DataBase:
    """
    This class is using pyodbc as connection to Azure
    """
    def __init__(self,option_file,type = None):
        self._type_list = ["MySQL","SQLServer"]
        self._file = option_file
        self._connection = Connect(option_file)
        self._type = type
        return

    def getdata(self,command):
        """
        Function is for get any information from the database
        it will return the data get from database
        Precondition:
           command (String) : string need to excutive
        return :
            data retrive from databse
        """
        data = None
        if self._connection.connect():
            self._connection.get_cursor().execute(command)
            data = self._connection.get_cursor().fetchall()
            self._connection.close()
        return data

    def setdata(self,command):
        """
        Function will updata the database for the given command
        Precondition:
            command (String) : string need to excutive
        """
        if self._connection.connect():
            self._connection.get_cursor().execute(command)
            self._connection.commit()
            self._connection.close()
            return True
        return False


class Connect:
    def __init__(self,option_file,type = None):
        """
        Initialize a MySQL database connection object.
        Preconditions:
            option_file - name of option file (str)
        Postconditions:
            Initializes a database connection object.
        """
        self._connection = None
        self._type = type
        self._config = ConfigParser()
        try:
            self._config.read_file(open(option_file))
        except FileNotFoundError:
            raise Exception(
                "Option file '{}' not found.".format(option_file))
        return

    def connect(self):
        """
        make the connection connect, if connect return true otherwise return False
        """
        result= self._connect_mysql()
        if result == False:
            result = self._connect_sqlserver()
        return result

    def _connect_mysql(self):
        """
        Function will try to initialize a MySQL database connection object.
        Precondition:
            config (str): name of config file
        return:
            False if initialize fail, otherwise return the connect object
        """
        try:
            # Extract the client section
            info = self._config['MySQL']
            # Connect to the database
            self._connection = connect(
                user=info['user'], password=info['password'], host=info['host'],
                database=info['database'])
        except Exception:
            self._connection = None
            print("MySQL Ddatabase cannot connect")
            return False
        return True


    def _connect_sqlserver(self):
        """
        Function will get the database connection string
        form the config, and return as a full connection
        string
        Precondition:
            config (Database) : all the connection info for the string
        return :
            (String) full connetion string for SQL Server
        """
        try:
            info = self._config['SQLServer']
            driver = info['driver']
            server = info['server']
            database = info['database']
            username = info['username']
            password = info['password']
            connectstring = "DRIVER={};SERVER={};DATABASE={};UID={};PWD={}".format( \
                    driver,server,database,username,password)
            self._connection = sql.connect(connectstring)
        except Exception as p:
            print("SQLServer cannot connect")
            self._connection = None
            return False
        return True

    def get_cursor(self):
        """
        Returns a database cursor.
        """
        try:
            return self._connection.cursor()
        except AttributeError:
            raise Exception("Database connection is closed.")

    def close(self):
        """
        Closes the database connection.
        """
        try:
            self._connection.close()
            self._connection = None
            return
        except AttributeError:
            raise Exception("Database connection is already closed.")


    def commit(self):
        try:
            self._connection.commit()
        except AttributeError:
            raise Exception("Database connection is already closed.")
