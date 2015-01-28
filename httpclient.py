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

	HTTPHost = ""
	HTTPPath = ""
	HTTPPort = ""

	def get_host_port(self,url):
        #parse a url to get what info I need, Chunhanlee told me about this builtin python library function
        #https://docs.python.org/2/library/urlparse.html
        
	#http://stackoverflow.com/questions/20315010/python-urlparse-urlparseurl-hostname-return-none-value
        #call urlparse to seperate url
	    self.HTTPHost = urlparse.urlparse(url).hostname 
	    self.HTTPPath = urlparse.urlparse(url).path
	
	# if no path then set path to something
	#if (HTTPPath == ''):
	  #  HTTPPath = "\"
        
	# check for port
            self.HTTPport = urlparse.urlparse(url).port or None

	#https://msdn.microsoft.com/en-us/library/cc959833.aspx
	#HTTP usually run on port 80, or maybe 443 SSL ?
	    if self.HTTPport == None:
		self.HTTPport == "80"

        

        def connect(self, host, port):
            # use sockets!
            #http://stackoverflow.com/questions/68774/best-way-to-open-a-socket-in-python
            connect_sock = socket.socket()
            connect_sock.connect((host, port))
            return None

        def get_code(self, data):
            return None

        def get_headers(self,data):
            return None

        def get_body(self, data):
            return None

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
            code = 500
            body = ""
            return HTTPRequest(code, body)

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
