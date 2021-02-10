#!/usr/bin/env python3
# coding: utf-8
# Copyright 2016 Abram Hindle, https://github.com/tywtyw2002, and https://github.com/treedust
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
import urllib.parse

def help():
    print("httpclient.py [GET/POST] [URL]\n")

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):

    def connect(self, host, port):
        print('Creating TCP socket')
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print("host: {h}".format(h = host))
            print("port: {p}".format(p = port))
            self.socket.connect((host, port)) 
        except (socket.error):
            #how new is this formatting (what version python?)
            print("Failed to create socket. Error code: {e}".format(e = socket.error))
            sys.exit()
        print('Socket created successfully')
        return self.socket

    def get_code(self, data):
        code = "nothing here yet"
        print("code: {c}".format(c = code))
        #return code
        return None

    def get_headers(self,data):
        headers = "nothing here yet"
        print("headers: {h}".format(h = headers))
        #return headers
        return None

    def get_body(self, data):
        headers = "nothing here yet"
        print("body: {b}".format(b = body))
        #return body
        return None
    
    def sendall(self, data):
        # all good
        self.socket.sendall(data.encode('utf-8'))
        
    def close(self):
        # all good
        self.socket.close()

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray() #does conversion for you
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return buffer.decode('utf-8')


    def GET(self, url, args=None):
        #get host and port --> check urlib if it will do this for you
        #connect
        code = 500
        body = ""

        #self.close()
        return HTTPResponse(code, body)


    def POST(self, url, args=None):
        code = 500
        body = ""
        
        #self.close()
        return HTTPResponse(code, body)


    def command(self, url, command="GET", args=None):
        print("commmand function")
        if (command == "POST"):
            return self.POST( url, args )
        else:
            # GET also assumed if user puts in something other than POST or GET
            return self.GET( url, args ) 
    
if __name__ == "__main__":
    # takes care of client command line args
    # no more checking required? ("httpclient.py [GET/POST] [URL]\n")
    client = HTTPClient()
    command = "GET" # assume GET if no method specified 
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print(client.command( sys.argv[2], sys.argv[1] ))
    else:
        print(client.command( sys.argv[1] ))
