Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 22:45:29) [MSC v.1916 32 bit (Intel)] on win32
Type "help", "copyright", "credits" or "license()" for more information.
>>> 
import MySQLdb
import time
MySQLdb.paramstyle
from datetime import datetime
import time
import sys
import fcntl


def connect(ip_address, port1, username, password, database, values, identifier_type):
    port1 = int(port1)
    connMRS = MySQLdb.connect (host = ip_address,
        port=port1,
        user=username,
        passwd = password,
        db=database)

    caseno = values['number']
    gender = values['gender']
    if gender == 'Male':
        gender = 'Male'
    elif gender == 'Female':
        gender = 'Female'
    else:
        gender = 'Female'

    birthdate = values['birthdate']
    todaydate = datetime.today().strftime('%Y-%m-%d')
    street = values['street']
    city = values['city']
    state = values['state']
    country = values['country']
    firstname = values['firstname']
    middlename = values['middlename']
    lastname = values['lastname']
    for item in values:
        if (values[item] is None) or (values[item] is False):
            values[item] = "_"

    #insert person on person table
    cursoromrs1 = connMRS.cursor()
    inspersonstmnt = """INSERT INTO person(firstname,middlename,lastname,street,city,state,country,gender,birthdate,birthdate_estimated,dead,\
                  creator,date_created,voided,\
                  uuid) \
                  VALUES(%s, %s,'0','0', '1',%s,'0', uuid())"""
    cursoromrs1.execute(inspersonstmnt, (gender, birthdate, todaydate))
    patientid = int(cursoromrs1.lastrowid)
    cursoromrs1.execute("commit")
    cursoromrs1.close()


    #insert patient into patient table
    cursoromrs2 = connMRS.cursor()
    insertpatient = """INSERT INTO patient (patient_id,creator,date_created) \
    VALUES(%s,1,%s)"""
    cursoromrs2.execute(insertpatient, (patientid, todaydate))
    cursoromrs2.execute("commit")
    cursoromrs2.close()


    #insert patient into patient_identifier table
    cursoromrs3 = connMRS.cursor()
    insertcase = """INSERT INTO patient_identifier (patient_id, \
    identifier,identifier_type,preferred , location_id, creator, date_created,uuid) \
    VALUES( %s, %s , %s, 1, 1, 1, %s , uuid())"""
    cursoromrs3.execute(insertcase, (patientid, caseno, identifier_type, crdate))
    cursoromrs3.execute("commit")
    cursoromrs3.close()

    return patientid

def connect_write(ip_address, port1, username, password, database, patientid, values, identifier_type):
    port1 = int(port1)
    connMRS = MySQLdb.connect (host = ip_address,
        port=port1,
        user=username,
        passwd = password,
        db=database)
