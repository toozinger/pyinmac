"""
IN-MaC Database utilities

Copyright (c) 2021 IN-MaC, Purdue University
Author: Benjamin P. Haley

LICENSE
"""

from mysql.connector import connect
from datetime import datetime
from .servers import servers
import traceback
import mysql

def connect_inmac_db(server_name, user_name, password, db_name='IMT_machines'):
    """Return a connection to an IN-MaC MySQL database"""
    # Select server and check if valid
    try:
        s = servers[server_name]
    except KeyError:
        raise Exception("UnknownServer") from None
    except: raise
    
    # Connect to host, catching common errors
    try:
        db = connect(host=s['host'], user=user_name, password=password, 
                     database=db_name, port=s['ports']['mysql'])
        db.get_warnings = True
        return db
    except mysql.connector.errors.ProgrammingError as error:
        if error.errno == 1045:
              raise Exception("AccessDeniedForUser") from None
        elif error.errno == 1044:
            raise Exception("NoAccessToThisDatabase") from None
        else:
            raise
    except:
        raise

# Columns:
# id      (int, primary)
# Time    (datetime(6) - largest range, no UTC conversion, includes microsecs)
# Value   (varchar255  - store numbers, strings, etc.)
# Metric  (varchar255)

# TODO cf Kepware/Token_Line table?

create_table_sql = \
    'CREATE TABLE IF NOT EXISTS {0} (id INT AUTO_INCREMENT NOT NULL PRIMARY KEY, Time DATETIME(6) NOT NULL, Value VARCHAR(255) NOT NULL, Metric VARCHAR(255) NOT NULL)'

def check_machine_table(db, machine_name):
    """
    Check that a table exists for machine_name; create the table if it does not
    exist.  Return True/False to indicate if the table was created.
    """
    ret = False
    c = db.cursor()
    s = 'SELECT COUNT(*) FROM information_schema.tables WHERE table_name = "%s"'
    c.execute(s, (machine_name,))
    r = c.fetchone()
    if r[0] == 0:  #r is None
        c.execute(create_table_sql.format(machine_name))
        db.commit()
        ret = True
    c.close()
    return ret
    
def get_time():
    """Return the current time value for inclusion in a DB"""
    return str(datetime.now())

def add_data(db, machine_name, time, value, metric): 
    """Insert new data into the specified machine table"""
    c = db.cursor()
    s = 'INSERT INTO {0} (Time, Value, Metric) VALUES (%s, %s, %s)'
    
    # Checks for common errors
    try:
        c.execute(s.format(machine_name), (time, str(value), metric))
        c.close()
        db.commit()
    except mysql.connector.errors.ProgrammingError as error:
        if error.errno == 1146:
            raise Exception("TableDoesNotExist") from None
        else:
            raise
    except:
        raise

def get_data(db, machine_name, metric, where=None):
    """
    Return time, value lists for selected metric with optional where clause
    """
    c = db.cursor()
    s = 'SELECT Time, Value FROM {0} WHERE Metric = "{1}"'
    if where is not None:
        s += ' AND '+where
    # Catch common errors
    try:
        c.execute(s.format(machine_name, metric))
    except mysql.connector.errors.ProgrammingError as error:
        if error.errno == 1146:
            raise Exception("TableDoesNotExist") from None
        else:
            raise
    t = []
    x = []
    for r in c.fetchall():
        t.append(r[0])  # datetime object
        x.append(r[1])
    c.close()
    return t, x

# XXX This fails - why?
#s = 'SELECT Time, Value FROM {0} WHERE Metric = "%s"'
#c.execute(s.format(machine_name), (metric,))

