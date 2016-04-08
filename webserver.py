# coding=utf-8

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Restaurant, Base, MenuItem
import urllib, sys
import cgi



engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

class WebServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
                output=""
                output+="<html><body>"
                output+="<h1>Create a New Restaurant</h1>"
                output+='''<form method='POST' enctype='multipart/form-data' action='/restaurants/new'>  Restaurant Name: <input name="newRestaurantName" type="text" placeholder="New Restaurant Name"><input type="submit" value="Create"></form></body></html>'''
                self.wfile.write(output)
                return

            elif self.path.endswith("/restaurants") or self.path.endswith("/restaurants/"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                restaurants=session.query(Restaurant).all()
                output = ""
                output += "<html><body>"
                output += '''<a href="/restaurants/new"<b>Create a New restaurant</b></a><p>'''
                for restaurant in restaurants:
                    output += "<h2>"+restaurant.name+"</h2><small><a href='#'>Edit</a> <a href='#'>Delete</a></small><hr>"
                # output += "<h1>Hello!</h1>"
                # output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        try:
            if self.path.endswith("/restaurants/new"):
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newRestaurantName')

                newRestaurant=Restaurant(name=messagecontent[0])
                session.add(newRestaurant)
                session.commit()

                output=""
                output+='''<html><head><meta http-equiv="refresh" content="2;url=/restaurants" ></head><body>'''
                output+="Add "+messagecontent[0]+" into database <b>Success!</b>"
                output+="</body></html>"
                self.wfile.write(output)
                return

        except:
            output=""
            output+='''<html><head><meta http-equiv="refresh" content="2;url=/restaurants" ></head><body>'''
            output+="Add "+messagecontent[0]+" into database <b>Fail!</b>"
            output+="</body></html>"
            self.wfile.write(output)
            return


def main():
    try:
        port = 8078
        server = HTTPServer(('', port), WebServerHandler)
        print "Web Server running on port %s" % port
        server.serve_forever()
    except KeyboardInterrupt:
        print " ^C entered, stopping web server...."
        server.socket.close()

if __name__ == '__main__':
    main()
