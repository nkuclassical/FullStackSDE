from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Restaurant, Base, MenuItem
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify

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


@app.route('/restaurants/<int:restaurant_id>/new',methods=['GET','POST'])
def newMenuItem(restaurant_id):
    if request.method == 'POST':
        newItem=MenuItem(name=request.form['name'],restaurant_id=restaurant_id, description=request.form['description'],price=request.form['price'])
        session.add(newItem)
        session.commit()
        flash("New menu item created!")
        return redirect(url_for('restaurantMenu',restaurant_id=restaurant_id))
    else:
        return render_template('newMenuItem.html',restaurant_id=restaurant_id)


@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit',methods=['GET','POST'])
def editMenuItem(restaurant_id,menu_id):
    editedItem=session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method=='POST':
        if request.form['name']:
            editedItem.name=request.form['name']
        session.add(editedItem)
        session.commit()
        flash("Menu item edited!")
        return redirect(url_for('restaurantMenu',restaurant_id=restaurant_id))
    else:
        return render_template('editMenuItem.html',restaurant_id=restaurant_id,menu_id=menu_id,item=editedItem)

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete',methods=['GET','POST'])
def deleteMenuItem(restaurant_id,menu_id):
    deleteItem=session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method=='POST':
        session.delete(deleteItem)
        session.commit()
        flash("Menu item deleted!")
        return redirect(url_for('restaurantMenu',restaurant_id=restaurant_id))
    else:
        return render_template('deletemenuitem.html',restaurant_id=restaurant_id,item=deleteItem)

@app.route('/restaurants/<int:restaurant_id>/menu/json')
def restaurantMenuJSON(restaurant_id):
    items=session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
    return jsonify(MenuItems=[i.serialize for i in items])

@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/json')
def menuJSON(restaurant_id,menu_id):
    items=session.query(MenuItem).filter_by(id=menu_id).one()
    return jsonify(items.serialize)

if __name__ == '__main__':
    app.debug = True
    app.secret_key = 'super_secret_key'
    app.run(host='0.0.0.0',port=5000)
