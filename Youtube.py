import os as System;
from dotenv import load_dotenv as Env;
from Source.Source import Source;

Env()

if __name__ == "__main__":
    Source( int( System.getenv( "PORT" ) ) );