import psycopg2
import psycopg2.extras
from config import config

def connect():
  connection = None
  params = config()
  connection = psycopg2.connect(**params)
  connection.autocommit = True
  return connection

if __name__ == '__main__':
  connect()