import pyodbc as sql

class DataBase:
    """
    This class is using pyodbc as connection to Azure 
    """
    def __init__(self,config):
        self._connstr = self._get_connection(config)

        return 

    def _get_connection(self,config):
        """
        Function will get the database connection string 
        form the config, and return as a full connection 
        string
        Precondition:
            config (Database) : all the connection info for the string
        return :
            (String) full connetion string for SQL Server
        """
        driver = config['driver']
        server = config['server']
        database = config['database']
        username = config['username']
        password = config['password']
        cs = "DRIVER={};SERVER={};DATABASE={};UID={};PWD={}".format( \
                driver,server,database,username,password)
        return cs

    def _create_conn(self):
        """
        Function will return database connection
        return :
            databse connection
        """ 
        return sql.connect(self._connstr)

    def getdata(self,command):
        """
        Function is for get any information from the database
        it will return the data get from database
        Precondition:
           command (String) : string need to excutive
        return :
            data retrive from databse
        """
        conn = self._create_conn()
        c = conn.cursor()
        c.execute(command)
        data = c.fetchall()
        conn.close()
        return data

    def setdata(self,command):
        """
        Function will updata the database for the given command
        Precondition:
            command (String) : string need to excutive
        """
        conn = self._create_conn()
        c = conn.cursor()
        c.execute(command)
        conn.commit()
        conn.close()
        return

