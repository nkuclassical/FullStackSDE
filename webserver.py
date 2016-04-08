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
            if self.path.endswith("/hello"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                restaurants=session.query(Restaurant).all()
                output = ""
                output += "<html><body>"
                for restaurant in restaurants:
                    output += "<h2>"+restaurant.name+"</h2><small><a href='#'>Edit</a> <a href='#'>Delete</a></small><hr>"
                # output += "<h1>Hello!</h1>"
                # output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return


            elif self.path.endswith(urllib.quote('你好'.decode(sys.stdin.encoding).encode('utf8'))):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"
                output += "<h1>你好!</h1>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/你好'><h2>你想说些什么?</h2><input name="messageCN" type="text" ><input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return
        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        try:
            self.send_response(301)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            ctype, pdict = cgi.parse_header(
                self.headers.getheader('content-type'))
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                if fields.get('message'):
                    messagecontent = fields.get('message')
                elif fields.get('messageCN'):
                    messagecontent = fields.get('messageCN')
            output = ""
            output += "<html><body>"
            output += " <h2> Okay, how about this: </h2>"
            output += "<h1> %s </h1>" % messagecontent[0]
            output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
            output += "</body></html>"
            self.wfile.write(output)
            print output
        except:
            pass


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
