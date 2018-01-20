import requests
import xml.etree.ElementTree as ET

class soapproxy:
      url="http://52.220.157.99/Services/Directory.asmx?wsdl"
      headers = {'content-type': 'text/xml'}
      appid='0'
      sid=''
      def __init__(self,username,password,appid):
           body = """<?xml version="1.0" encoding="utf-8"?>
                <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                xmlns:xsd="http://www.w3.org/2001/XMLSchema"
                xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
                <soap:Body>
                <Login xmlns="http://gpsgate.com/services/">
                <strUsername>%s</strUsername>
                <strPassword>%s</strPassword>
                <iApplicationID>%s</iApplicationID>
                </Login>
                </soap:Body>
                </soap:Envelope>"""%(username,password,appid)
           self.appid=appid
           response = requests.post(self.url,data=body,headers=self.headers)
           tree = ET.fromstring(response.content)
           self.sid=tree[0][0][0][0].text
      def getUsersInUserTag(self,usertag):
           device= [];
           body = """<?xml version="1.0" encoding="utf-8"?>
           <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
           xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
           <soap:Body>
           <GetUsersInUserTag xmlns="http://gpsgate.com/services/">
           <strSessionID>%s</strSessionID>
           <iApplicationID>%s</iApplicationID>
           <strTagName>%s</strTagName>
           </GetUsersInUserTag>
           </soap:Body>
           </soap:Envelope>"""%(self.sid,self.appid,usertag)
           response = requests.post(self.url,data=body,headers=self.headers)
           tree = ET.fromstring(response.content)
           for i in range(0,len(tree[0][0][0][0])):
               device.append([tree[0][0][0][0][i][2].text,tree[0][0][0][0][i][9][0][0].text,\
                              tree[0][0][0][0][i][9][0][1].text,tree[0][0][0][0][i][9][1][0].text,\
                              tree[0][0][0][0][i][9][1][1].text])
           return (device)
