#Script populating solar data from pvwatts web service
#Mike Tafel 
#2010/07/26
import urllib, urllib2, pg, simplejson as json, time, sys,  hashlib, hmac, base64, urlparse
#DB connection properties
db = pg.connect(dbname = 'database_name', host= 'host', port= 5432, user = 'user',passwd= 'password')

#db query sql CHANGE TO TABLE NAME
selectallSql = "select * FROM sem_qcew_geocode WHERE latitude < 0 OR latitude IS NULL"

#db queries
sel = db.query(selectallSql) 
result = sel.getresult()
#fields = sel.listfields()
rows = len(result)
#beggining to build url

base_url = "http://maps.google.com/maps/api/geocode/json?"



print rows
x = 0
while x < rows:
    
    #Setting up the variables for the query string.
    row = result[x]
    add = row[1]          #This is the field number of your address field
    zip = str(row[3])
##    zip= row[3]             #This is the field number of your zip code field
    objectid = row[0]       #This is the field number of your id field
    values = { 'sensor' : 'false','address' :add+' , '+zip}

    data = urllib.urlencode(values)
    
    
    #build request url
    request_url = base_url+data
    print request_url
    
    #send request
    start = time.time()
    print values
    response = urllib2.urlopen(request_url)
   
    output = response.read()
    elapsed = (time.time() - start)
    #Read and parse json output.
  
    data = json.loads(output)
    status = data["status"]
    print status    
    if status == "OVER_QUERY_LIMIT":
        x = rows
        print "over the query limit"
    elif status == "OK":
        long = data["results"][0]["geometry"]["location"]["lng"]
        lat = data["results"][0]["geometry"]["location"]["lat"]
        precision = data["results"][0]["geometry"]["location_type"]
        #If the geocode result is outside of the region, don't use it. 
        if long < -106 or long > -104 or lat > 41 or lat < 38:
           update_query = "UPDATE sem_qcew_geocode SET latitude = -2, precision = '%(prec)s' WHERE objectid = '%(objectid)s'" % {'objectid' : objectid, 'prec': precision}
          db.query(update_query)
           print "out of region"
        else:
        values = {'long' : long, 'lat' : lat, 'prec': precision, 'objectid' : objectid}
        update_query = "UPDATE sem_qcew_geocode SET longitude = '%(long)s', latitude = '%(lat)s', precision = '%(prec)s' WHERE objectid = '%(objectid)s'" % values
        db.query(update_query)
    elif status != "OK":
        #update the data
        update_query = "UPDATE sem_qcew_geocode SET latitude = -1 WHERE objectid = '%(objectid)s'" % {'objectid' : objectid}
        
        db.query(update_query)
     
    else:
        pass
    x = x+1
    #the amount of time each geocde takes. 
    print elapsed







