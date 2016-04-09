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

@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
    output = ''
    for i in items:
        output += i.name
        output += '</br>'
        output += i.price
        output += '</br>'
        output += i.description
        output += '</br>'
        output += '</br>'
    return output


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0',port=5000)
