#!/usr/bin/env python
# coding: utf-8
# Copyright 2013 Abram Hindle
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
# you may use urllib to encode data appropriately
import urllib

from urlparse import urlparse

def help():
    print "httpclient.py [GET/POST] [URL]\n"

class HTTPRequest(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    
        #initialize variables used
	HTTPHost = ""
	HTTPPath = ""
	HTTPPort = ""
        code = ""
        headers= ""
        body = ""

	def get_host_port(self,url):
            
            #call urlparse to seperate url
	    self.HTTPHost = urlparse(url).hostname 

            #get pathway
	    self.HTTPPath = urlparse(url).path

            #checkpathway if not a valid pathway set default path of /
            if (len(self.HTTPPath) <= 1):
                self.HTTPPath = "/"

	    # check for port
            self.HTTPPort = urlparse(url).port or None
            

	    #set port if there is no port is present
	    #HTTP usually run on port 80, or maybe 443 SSL ?
	    if self.HTTPPort == None:
		self.HTTPPort = 80

            #print("Host",self.HTTPHost)
            #print("Port",self.HTTPPort)
            #print("Path",self.HTTPPath)

        def connect(self, host, port):
            #initialize a socket using host and port 
            connect_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            connect_sock.connect((host, port))
            return connect_sock

        def get_code(self, data):
            #split the server response on spaces
            #second element will be the response code
	    self.code = int(data.split(' ')[1])
            #print("THIS IS CODE", self.code)
            return self.code

        def get_headers(self,data):
            #split the response on \r\n\r\n first element will be the headers
	    #print("this is the data", data.split("\n")
	    self.headers = data.split("\r\n\r\n")[0]
            return self.headers

        def get_body(self, data):
            #split response on \r\n\r\n second element will be the body
            self.body = data.split("\r\n\r\n",1)[1]
            return self.body

        # read everything from the socket
        def recvall(self, sock):
            buffer = bytearray()
            done = False
            while not done:
                part = sock.recv(1024)
                if (part):
                    buffer.extend(part)
                else:
                    done = not part
            return str(buffer)

        def GET(self, url, args=None):

            #need host and port for a socket connection
            self.get_host_port(url)

            #print("Creating socket to '" + self.HTTPHost + "' on port " + str(self.HTTPPort))
            #initialize socket for get request
            socket = self.connect(self.HTTPHost,self.HTTPPort)

            #minimum req for a HTTP get request
            requestHttp = "GET "+self.HTTPPath+" HTTP/1.1\r\n"+"Host:"+self.HTTPHost+"\r\n"+"Accept: */*\r\n"+"Connection: close\r\n\r\n"
	     
            #sending HTTP message through socket to server
            socket.sendall(requestHttp)
           
            #get response
            response = self.recvall(socket)
            #print("This is the response",response)

            #parse server response for code/body and store in HTTPRequest Object
            return HTTPRequest(self.get_code(response), self.get_body(response))

        def POST(self, url, args=None):
            requestpost = ""
            #need host and port for socket creation
            self.get_host_port(url)

            #print("Creating socket to '" + self.HTTPHost + "' on port " + str(self.HTTPPort))
            socket = self.connect(self.HTTPHost,self.HTTPPort)

            #post request formatting
            requestpost = "POST %s HTTP/1.1\r\nHost: %s\r\n Accept: */*\r\nContent-Type: application/x-www-form-urlencoded\r\n" % (self.HTTPPath, self.HTTPHost)

            #check if any args is anything
            if (args != None):
                
                #encode data using urllib
                adddata = urllib.urlencode(args)

                #find out the length of the encoded data
                contentlen = str(len(adddata))

                #add Content-Length to header containing datas length
                requestpost = requestpost + "Content-Length: %s\r\n\r\n" % contentlen
                
                #add the edcoded data after content-length
                requestpost = requestpost + adddata

            # if no args then set content-length to 0                      
            else:
                requestpost = requestpost + "Content-Length: 0\r\n\r\n"
                          
            #send request over socket
            socket.sendall(requestpost)

            #get response from server
            response = self.recvall(socket)
                                 
            #print("This is the post response", response)

            #parse response for code and body and store in HTTPRequest object
            return HTTPRequest(self.get_code(response), self.get_body(response))

        def command(self, url, command="GET", args=None):
            if (command == "POST"):
                return self.POST( url, args )
            else:
                return self.GET( url, args )
    
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print client.command( sys.argv[1], sys.argv[2] )
    else:
        print client.command( command, sys.argv[1] )    
