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
from urllib.parse import urlparse
import random

def help():
    # function to instruct user if format or request is wrong
    print("httpclient.py [GET/POST] [URL]\n")

class HTTPResponse(object):
    # class to make an object of an HTTP response
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    # class to drive
    
    def connect(self, host, port):
        # function to connect to a host:port
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((host, port)) 
        except (socket.error):
            print("Failed to create socket. Error code: {e}".format(e = socket.error))
            sys.exit()

 
    def get_code(self, data):
        # function to get status code from an HTTP response
        print(data)
        code = data.split('\n')[0]
        code = code.split(' ')[1]
        print("code: {c}".format(c = code))
        try:
            code = (int(code))
        except:
            code = 500
            
        return code #only likes integers
    

    def get_headers(self,data):
        # function to parse headers from a HTTP response
        headers = data.split('\r\n\r\n')[0]
        print("headers: {h}".format(h = headers))
        return headers

        
    def get_body(self, data):
        # function to parse body from a HTTP response
        body = ''
        body = data.split('\r\n\r\n')[1]
        print('body: {b}'.format(b = body))
        return body

    
    def sendall(self, data):
        # function to encode and send data
        self.socket.sendall(data.encode('utf-8'))

        
    def close(self):
        # function to close the socket
        self.socket.close()


    def recvall(self, sock):
        # function to read everything from the socket
        buffer = bytearray() #does conversion for you
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return buffer.decode('utf-8')


    def get_port(self,o):
        # function to get/set a port
        if o.port is None:
            if o.scheme == 'https':
                port = 443
            elif o.scheme == 'http':
                port = 80
            else:
                port = 27600 + random.randint(1,100)
        else:
            port = o.port
        return port


    def get_host(self,o):
        # function to get/set host
        # function assumes that host is parsable (ex: run https//... --> doesnt work)
        print('host {hn}'.format(hn = o.hostname))
        if o.hostname is not None:
            host = o.hostname
        else:
            host = self.get_url(o)
        return host

    def get_path(self,o):
        # function to get/set path
        print('path {p}'.format(p = o.path))
        if o.path != '' and o.path is not None:
            path = o.path
        else:
            path = "/"
        return path


    def format_get_request(self, path, host):
        # CITATION: https://developer.mozilla.org/en-US/docs/Web/HTTP/Messages
        #startline = method, path/url/(host:port)/*, HTTP version\r\n optional headers\r\n\r\n optional body

        request =  "GET {p} HTTP/1.1\r\n".format(p = path)
        request += "Host: {h}\r\nAccept: */*\r\n".format(h = host) #request headers
        request += "Connection: Closed\r\n\r\n" #general header
        return request
    
        
    def GET(self, url, args=None):
        # CITATION: https://docs.python.org/3/library/urllib.parse.html
        o = urlparse(url)
        
        host = self.get_host(o)
        port = self.get_port(o)
        path = self.get_path(o)

        self.connect(host,port)

        request = self.format_get_request(path,host)
        self.sendall(request)
        
        response = self.recvall(self.socket)
        self.close()
        
        code = self.get_code(response)
        body = self.get_body(response)
        #print("response: {r}".format(r = response))
        #print("code {c}".format(c = code))

        return HTTPResponse(code, body)


    def format_post_request(self, args, host, port, path):
        # CITATION: https://developer.mozilla.org/en-US/docs/Web/HTTP/Messages
        #startline = method, path/url/(host:port)/*, HTTP version\r\n optional headers\r\n\r\n optional body
        
        request = "POST {p} HTTP/1.1\r\n".format(p=path) #startline
        request += "Host: {h}\r\nAccept: */*\r\n".format(h=host) #request headers
        request += "Connection: Closed\r\n" #general headers
        
        if args is None:
            request += "Content-Length: 0\r\n"
            request += "Content-Type: application/x-www-form-urlencoded\r\n\r\n"
        else:
            # CITATION: https://docs.python.org/3/library/urllib.request.html#urllib-examples
            # convert such lists of pairs into query strings
            params = urllib.parse.urlencode(args,doseq=True)
            request += "Content-Length: "+str(len(params))+"\r\n"
            request += "Content-Type: application/x-www-form-urlencoded\r\n\r\n" #representation headers
            request += "{p}".format(p=params)

        return request
        


    def POST(self, url, args=None):
        # CITATION https://docs.python.org/3/library/urllib.parse.html
        o = urlparse(url)
        
        host = self.get_host(o)
        port = self.get_port(o)
        path = self.get_path(o)

        self.connect(host,port)

        request = self.format_post_request(args, host, port, path)
        self.sendall(request)

        response = self.recvall(self.socket)
        self.close()
        
        code = self.get_code(response)
        body = self.get_body(response)
        #print("response: {r}".format(r = response))
        #print("code {c}".format(c = code))

        return HTTPResponse(code, body)


    def command(self, url, command="GET", args=None):
        if (command == 'POST'):
            return self.POST( url, args )
        else:
            return self.GET( url, args )
        
    
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET" # assume GET if no method specified
    print(sys.argv)
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print(client.command( sys.argv[2], sys.argv[1] ))
    else:
        print(client.command( sys.argv[1] ))
