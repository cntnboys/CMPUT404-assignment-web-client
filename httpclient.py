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
            #parse a url to get what info I need, Chunhanlee told me about this builtin python library function
            #https://docs.python.org/2/library/urlparse.html
        
            #http://stackoverflow.com/questions/20315010/python-urlparse-urlparseurl-hostname-return-none-value
            #call urlparse to seperate url
	    self.HTTPHost = urlparse(url).hostname 

            #get pathway
	    self.HTTPPath = urlparse(url).path or '/'
        
	    # check for port
            self.HTTPPort = urlparse(url).port or None

	    #https://msdn.microsoft.com/en-us/library/cc959833.aspx
	    #HTTP usually run on port 80, or maybe 443 SSL ?
	    if self.HTTPPort == None:
		self.HTTPPort = "80"

            print("Host",self.HTTPHost)
            print("Port",self.HTTPPort)
            print("Path",self.HTTPPath)

        def connect(self, host, port):
            # use sockets!
            #http://stackoverflow.com/questions/68774/best-way-to-open-a-socket-in-python
            connect_sock = socket.socket()
            connect_sock.connect((host, port))
            return connect_sock

        def get_code(self, data):
            print(data)
            code = int(data.split()[1])
            print(code)
            return code

        def get_headers(self,data):
            print (data)
            headers = data.split("/r/n/r/n")[0]
            print(headers)
            return headers

        def get_body(self, data):
            print(data)
            body = data.split("/r/n/r/n")[1]
            print(body)
            return body

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
            #code = 500
            #body = ""
            
            #need host and port for a socket connection
            self.get_host_port(url)
            #https://docs.python.org/2/library/socketserver.html
        
            #print("Creating socket to '" + self.HTTPHost + "' on port " + self.HTTPPort)
            socket = self.connect(self.HTTPHost,self.HTTPPort)
            #minimum req for a HTTP get/post
            #https://ellislab.com/forums/viewthread/74005/#367460
            #http://developer.nokia.com/community/discussion/showthread.php/180397-Sending-minimum-Headers-in-HTTP-request
            #class slides HTTP 2
            requestHttp = "GET"+self.HTTPPath+"HTTP/1.1/r/n"+"Host:"+self.HTTPHost+"/r/n"+"Accept: */*"+"/r/n"

            #sending message through socket
            #http://www.binarytides.com/python-socket-programming-tutorial/
            socket.sendall(requestHttp)

            #get response
            response = self.recvall(socket)

            print(response)

            return HTTPRequest(self.get_code(response), self.get_body(response))

        def POST(self, url, args=None):
            code = 500
            body = ""
            return HTTPRequest(code, body)

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
