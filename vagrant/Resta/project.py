from flask import Flask, render_template, url_for, request, redirect, flash, jsonify 
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Restaurant, Base, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

#JSON data transfers code
@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id).all()
    return jsonify(MenuItems=[i.serialize for i in items])

@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def oneItemJSON(restaurant_id,menu_id):
    menuItems = session.query(MenuItem).filter_by(id = menu_id).one()
    return jsonify(menuItems.serialize)


#Normal HTML website code 
@app.route('/')
@app.route('/restaurants/<int:rest_id>/menu')
def restaurantMenu(rest_id):
    restaurant = session.query(Restaurant).filter_by(id = rest_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = rest_id)
    return render_template('menu.html', restaurant = restaurant, items = items)
    
#Task 1: Create route for newMenuItem function here
#@app.route('/')
@app.route('/restaurants/<int:rest_id>/new/',methods=['GET','POST'])
def newMenuItem(rest_id):
    if request.method == 'POST':
        newItem = MenuItem(name = request.form['name'], restaurant_id = rest_id)
        session.add(newItem)
        session.commit()
        flash("Menu item created!")        
        return redirect(url_for('restaurantMenu',rest_id = rest_id))
    else: 
        return render_template('newmenuitem.html', rest_id = rest_id)


#    return "page to create a new item. Task 1 complete!"

#Task 2: Create route for newMenuItem function here
@app.route('/restaurants/<int:rest_id>/<int:menu_id>/edit/', methods = ['GET','POST'])
def editMenuItem(rest_id, menu_id):
    Existing = session.query(MenuItem).filter_by(id = menu_id).one()
    if request.method == 'POST':
        updateItem = MenuItem(name = request.form['name'], restaurant_id = rest_id)
        if request.form['name']:
            Existing.name = request.form['name']
        session.add(Existing)
        session.commit()
        flash("Menu item editted!")
        return redirect(url_for('restaurantMenu',rest_id = rest_id))
    else: 
        return render_template('editmenuitem.html', rest_id = rest_id, menu_id = menu_id, i = Existing)


#Task 3: Create route for newMenuItem function here
@app.route('/restaurants/<int:rest_id>/<int:menu_id>/delete/',methods=['GET','POST'])
def deleteMenuItem(rest_id,menu_id):
    Existing = session.query(MenuItem).filter_by(id = menu_id).one()
    if request.method == 'POST':
        session.delete(Existing)
        session.commit()
        flash("Menu item deleted!")                
        return redirect(url_for('restaurantMenu',rest_id = rest_id))
    else: 
        return render_template('deletemenuitem.html', rest_id = rest_id, menu_id = menu_id, i = Existing)


if __name__== '__main__':
    app.secret_key = 'super_secret_key'
    app.debug=True
    app.run(host = '0.0.0.0',port = 5000)
