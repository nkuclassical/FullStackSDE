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
            elif self.path.endswith("/edit"):
                restaurantIDPath=self.path.split('/')[2]
                myRestaurantQuery=session.query(Restaurant).filter_by(id=restaurantIDPath).one()
                if myRestaurantQuery:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    output = "<html><body>"
                    output += "<h1>"
                    output += myRestaurantQuery.name
                    output += "</h1>"
                    output += "<form method='POST' enctype='multipart/form-data' action = '/restaurants/%s/edit' >" % restaurantIDPath
                    output += "<input name = 'newRestaurantName' type='text' placeholder = '%s' >" % myRestaurantQuery.name
                    output += "<input type = 'submit' value = 'Rename'>"
                    output += "</form>"
                    output += "</body></html>"

                    self.wfile.write(output)

            elif self.path.endswith("/delete"):
                restaurantIDPath=self.path.split('/')[2]
                myRestaurantQuery=session.query(Restaurant).filter_by(id=restaurantIDPath).one()
                if myRestaurantQuery:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    output = "<html><body>"
                    output += "<h1>"
                    output += myRestaurantQuery.name
                    output += "</h1>"
                    output += "<form method='POST' enctype='multipart/form-data' action = '/restaurants/%s/delete' >" % restaurantIDPath
                    output += "Confirm to Delete "+myRestaurantQuery.name+" ?"
                    output += "<input type = 'submit' value = 'Delete'>"
                    output += "</form>"
                    output += "</body></html>"

                    self.wfile.write(output)

            elif self.path.endswith("/restaurants") or self.path.endswith("/restaurants/"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                restaurants=session.query(Restaurant).all()
                output = ""
                output += "<html><body>"
                output += '''<a href="/restaurants/new"<b>Create a New restaurant</b></a><p>'''
                for restaurant in restaurants:
                    output += "<h2>"+restaurant.name+"</h2><big><b>ID: </b>"+str(restaurant.id)+"</big><br /><small><a href='/restaurants/"+str(restaurant.id)+"/edit'>Edit</a> <a href='/restaurants/"+str(restaurant.id)+"/delete'>Delete</a></small><hr>"
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

            elif self.path.endswith("/edit"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newRestaurantName')
                    restaurantIDPath = self.path.split("/")[2]

                    myRestaurantQuery = session.query(Restaurant).filter_by(
                        id=restaurantIDPath).one()
                    if myRestaurantQuery != []:
                        myRestaurantQuery.name = messagecontent[0]
                        session.add(myRestaurantQuery)
                        session.commit()
                        self.send_response(301)
                        self.send_header('Content-type', 'text/html')
                        self.send_header('Location', '/restaurants')
                        self.end_headers()

            elif self.path.endswith("/delete"):
                restaurantIDPath = self.path.split("/")[2]
                myRestaurantQuery = session.query(Restaurant).filter_by(id=restaurantIDPath).one()
                if myRestaurantQuery != []:
                    session.delete(myRestaurantQuery)
                    session.commit()
                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()



        except:
            output=""
            output+='''<html><body>500 Internal Server Error</body></html>'''
            self.wfile.write(output)
            return


def main():
    try:
        port = 8003
        server = HTTPServer(('', port), WebServerHandler)
        print "Web Server running on port %s" % port
        server.serve_forever()
    except KeyboardInterrupt:
        print " ^C entered, stopping web server...."
        server.socket.close()

if __name__ == '__main__':
    main()
