import mysql.connector as Connecter
from mysql.connector import pooling, Error
from dotenv import load_dotenv as Env
import os as System

Env()

try :
    Pool = Connecter.pooling.MySQLConnectionPool(
        pool_name = "Club",
        pool_size = 30,
        pool_reset_session = True,
        host = System.getenv("SQL_HOST", "localhost"),
        user = System.getenv("SQL_USER", "root"),
        password = System.getenv("SQL_PASSWORD", ""),
        database = System.getenv("SQL_NAME", "Club-Play")
    );
except Error as E :
    Pool = None;

def Executer( Query , Params ) :
    try :
        Connection = Pool.get_connection();
        Cursor = Connection.cursor(dictionary=True);
        Cursor.execute( Query , Params );
        Data = Cursor.fetchall();
        Connection.commit();
        Cursor.close();
        Connection.close();
        return {
            "Success" : True,
            "Message" : "Query Executed Successfully"
        };
    except Error as E :
        return {
            "Success": False,
            "Error": str(E)
        };
    
def Fetcher( Query , Params ) :
    try :
        Connection = Pool.get_connection();
        Cursor = Connection.cursor(dictionary=True);
        Cursor.execute( Query , Params );
        Data = Cursor.fetchall();
        Cursor.close();
        Connection.close();
        return {
            "Success" : True,
            "Data" : Data
        };
    except Error as E :
        return {
            "Success": False,
            "Error": str(E)
        };