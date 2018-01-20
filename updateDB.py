import requests
from time import sleep
from random import randint
def insertJobToDB(db, address, jobdate, cpnId, description):
    URL = "https://maps.googleapis.com/maps/api/geocode/json?key=AIzaSyD1egkppa_4el0N36w_DP7mOCTqlU4EDRI"
    cursor = db.cursor()
# Insert new address into db
    cursor.execute("SELECT numOfQuery, longitude, latitude FROM dispatch_db.address WHERE address = '" + address + "'")
    data = cursor.fetchone()   
    # addres not exist in DB
    if data is None:           
        PARAMS = {'address':address}
        sleep( randint(10,100)*0.01 )
        r = requests.get(url = URL, params = PARAMS)
        resp=r.json()
        if len(resp['results']) > 0: # request  Google  API successfully
            lattitude=resp['results'][0]['geometry']['location']['lat']
            longitude=resp['results'][0]['geometry']['location']['lng']
            sql = "INSERT INTO dispatch_db.address (jobId, address, longitude, latitude, numOfQuery) VALUES (%s,%s,%s, %s)"
            cursor.execute( sql, (address, longitude, lattitude, 0) )
            db.commit()
            outputmsg = 'Upload jobs successfully!!!'
        elif len(resp['results']) == 0: # request  Google  API fail
            outputmsg = 'Please try again!!!'
    # address already exist in DB
    else: 
        numOfQuery, longitude, lattitude = data[0], data[1], data[2]
        sql2 = "UPDATE dispatch_db.address SET numOfQuery = %s WHERE address = %s"
        cursor.execute(sql2, (numOfQuery+1, address))
        db.commit()
        outputmsg =  'Upload jobs successfully!!!'


# Insert NEW jobs in the database
    sql3 = "INSERT INTO dispatch_db.jobs (cpnId, plate, jobdate, address, latitude, longitude, description, Status) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
    cursor.execute(sql3, (cpnId , 'Unassigned', str(jobdate),  address, str(lattitude), str(longitude), description, 'Unassigned'))
    db.commit()
# Mark jobs as "Finished"
    return outputmsg


def insertFileToDB(db, addressList, jobdate, cpnId, descriptionList):
    URL = "https://maps.googleapis.com/maps/api/geocode/json?key=AIzaSyD1egkppa_4el0N36w_DP7mOCTqlU4EDRI"
    cursor = db.cursor()
# Insert new address into db
    for i in range(len(addressList)):
        cursor.execute("SELECT numOfQuery, longitude, latitude FROM dispatch_db.address WHERE address = '" + addressList[i] + "'")
        data = cursor.fetchone()   
        # addres not exist in DB
        if data is None:           
            PARAMS = {'address':addressList[i]}
            sleep( randint(10,100)*0.001 )
            r = requests.get(url = URL, params = PARAMS)
            resp=r.json()
            if len(resp['results']) > 0: # request  Google  API successfully
                lattitude=resp['results'][0]['geometry']['location']['lat']
                longitude=resp['results'][0]['geometry']['location']['lng']     
                sql = "INSERT INTO dispatch_db.address (address, longitude, latitude, numOfQuery) VALUES (%s,%s,%s, %s)"
                cursor.execute( sql, (addressList[i], longitude, lattitude, 0) )
                db.commit()
                outputmsg = 'Upload jobs successfully!!!'
            elif len(resp['results']) == 0: # request  Google  API fail
                outputmsg = 'Please try again!!!'
        # address already exist in DB
        else: 
            numOfQuery, longitude, lattitude = data[0], data[1], data[2]
            sql2 = "UPDATE dispatch_db.address SET numOfQuery = %s WHERE address = %s"
            cursor.execute(sql2, (numOfQuery+1, addressList[i]))
            db.commit()
            outputmsg =  'Upload jobs successfully!!!'

# Insert NEW jobs in the database
        sql3 = "INSERT INTO dispatch_db.jobs (cpnId, plate, jobdate, address, latitude, longitude, description, Status) VALUES ( %s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql3, ( cpnId , 'Unassigned', str(jobdate),  addressList[i], str(lattitude), str(longitude), descriptionList[i], 'Unassigned'))
        db.commit()
    return outputmsg

def getTodayUnassignedJobs(db, cpnId, startDt, endDt):
    cursor = db.cursor() 
    cursor.execute("SELECT ID FROM dispatch_db.jobs WHERE cpnId='"+cpnId+"' AND status!= 'Finished' AND jobdate BETWEEN '"+startDt+"' AND '"+endDt+"'")
    unassigned_jobs = cursor.fetchall()
    for i, ID in enumerate(unassigned_jobs):
        sql = "UPDATE dispatch_db.jobs SET jobId = %s WHERE ID = %s"
        cursor.execute(sql, (i, ID))
    cursor.execute("SELECT address, latitude, longitude, description FROM dispatch_db.jobs WHERE cpnId='"+cpnId+"' AND status!= 'Finished' AND jobdate BETWEEN '"+startDt+"' AND '"+endDt+"'")
    unassigned_jobs = cursor.fetchall()
    return unassigned_jobs

def getAllJobs(db, cpnId):
    from datetime import datetime

    jobdate = datetime.now().strftime( "%Y-%m-%d %I:%M:%S" ) 
    startDt, endDt = jobdate[:-8] + "00:00:00", jobdate[:-8] + "11:59:00"

    cursor = db.cursor()
    cursor.execute("SELECT * FROM dispatch_db.jobs WHERE cpnId='" + cpnId + "' AND status!= 'Finished' AND jobdate BETWEEN '"+startDt+"' AND '"+endDt+"'")    #result = cursor.fetchall()
    result = cursor.fetchall()
    return result
