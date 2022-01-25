#!/usr/bin/env python
import SimpleHTTPServer
import SocketServer

import sqlite3
from sqlite3 import Error

def select_all_user(conn, wfile ):
    cur = conn.cursor()
    cur.execute("SELECT * FROM user")
    rows = cur.fetchall()
    for row in rows:
        print(row)
        wfile.write( str(row) + "<br>" )

def select_user(conn, wfile, username, password):
    cur = conn.cursor()
    # SAFE
    # sql = """SELECT uid FROM user WHERE `uid` = '%s' and `pwd` = '%s'""" % (username, password)
    # cur.execute(sql)
    
    # UNSAFE
    cur.execute("SELECT uid FROM user WHERE uid = '{}'".format(username)) 
    rows = cur.fetchone()
    print rows
    if bool(rows) :
        wfile.write("Login Success")
    else :
        wfile.write("Username or password is invalid")

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn

class MyRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/web.html'
            return SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)
        else :
            print( self.path )
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            print(self.wfile)
            self.wfile.write("<body><p>This is a test.</p>")
            self.wfile.write("<p>You accessed path: %s</p>" % self.path)

            # get uid & pwd
            path = self.path
            username = path[path.find('api1?uid=')+len('api1?uid='):path.rfind('&')]
            password = path[path.find('&pwd=')+len('&pwd='):path.rfind('')]

            # call database
            conn = create_connection( "/Users/akhmads/Downloads/simple-webserv-python/web.db")
            #select_all_user( conn, self.wfile )
            select_user( conn, self.wfile, username, password)
            self.wfile.close()

Handler = MyRequestHandler
PORT = 8088
server = SocketServer.TCPServer(('0.0.0.0', PORT), Handler)
print( "Server listening on port: ", PORT )
server.serve_forever()
