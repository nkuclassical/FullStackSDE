from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Restaurant, Base, MenuItem
from flask import Flask, render_template

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
    return render_template('menu.html',restaurant=restaurant,items=items)


@app.route('/restaurant/<int:restaurant_id>/new',methods=['GET','POST'])
def newMenuItem(restaurant_id):
    return "page to create a new menu item!"
@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/edit')
def editMenuItem(restaurant_id,menu_id):
    return "page to edit a new menu item for such restaurant"

@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/delete')
def deleteMenuItem(restaurant_id,menu_id):
    return "page to delete a new menu item for such restaurant"

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0',port=5000)
