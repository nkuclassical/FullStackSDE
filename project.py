from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Restaurant, Base, MenuItem
from flask import Flask

import urllib, sys
import cgi

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

app = Flask(__name__)

@app.route('/')
@app.route('/hello')
def HelloWorld():

    menuItems=session.query(MenuItem).all()

    output =  '<h1>Our Menu List</h1>'
    for menuItem in menuItems:
        output += '<big>'+menuItem.name+'</big></br>'
        output += '<small>'+str(menuItem.price)+'</br>'
        output += menuItem.description+'</small>'
        output += '<hr>'
    return output

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0',port=5000)
