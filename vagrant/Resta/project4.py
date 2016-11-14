from flask import Flask, render_template, url_for, request, redirect, flash, jsonify 
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Restaurant, Base, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

#>===============<
#JSON extraction
#>===============<

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

#>===============<
#Restaurant CRUD 
#>===============<

#Main page of restaurant website: 
@app.route('/')
@app.route('/restaurants')
def showRestaurants():
    restaurant = session.query(Restaurant).all()
    return render_template('homepage.html', restaurant = restaurant)

#New Restaurant page:
@app.route('/restaurants/new', methods =['GET', 'POST'])
def newRestaurant():
    if request.method == 'POST':
        newRestaurant = Restaurant(name = request.form['name'])
        session.add(newRestaurant)
        session.commit()
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('newRestaurant.html')

#Edit Restaurant page:
@app.route('/restaurants/<int:rest_id>/edit', methods = ['GET','POST'])
def editRestaurant(rest_id):
    Existing = session.query(Restaurant).filter_by(id = rest_id).one()
    if request.method == 'POST':
        if request.form['name']:
            Existing.name = request.form['name']
        session.add(Existing)
        session.commit()
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('editRestaurant.html', rest_id = rest_id, r = Existing)

#Delete Restaurant page:
@app.route('/restaurants/<int:rest_id>/delete', methods = ['GET','POST'])
def deleteRestaurant(rest_id):
    Existing = session.query(Restaurant).filter_by(id = rest_id).one()
    if request.method == 'POST':
        session.delete(Existing)
        session.commit()
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('deleteRestaurant.html', rest_id = rest_id, r = Existing)

#>===============<
#Individual Restaurant Menu Items CRUD 
#>===============<

#Individual Restaurant Code 
@app.route('/restaurants/<int:rest_id>/menu')
def showMenu(rest_id):
    restaurant = session.query(Restaurant).filter_by(id = rest_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = rest_id)
    return render_template('menu.html', restaurant = restaurant, items = items)
    
#New Menu Item code 
#@app.route('/')
@app.route('/restaurants/<int:rest_id>/new/',methods=['GET','POST'])
def newMenuItem(rest_id):
    if request.method == 'POST':
        newItem = MenuItem(name = request.form['name'], restaurant_id = rest_id)
        session.add(newItem)
        session.commit()
        flash("Menu item created!")        
        return redirect(url_for('showMenu',rest_id = rest_id))
    else: 
        return render_template('newmenuitem.html', rest_id = rest_id, r = Existing)


#    return "page to create a new item. Task 1 complete!"

#Edit menu items
@app.route('/restaurants/<int:rest_id>/<int:menu_id>/edit/', methods = ['GET','POST'])
def editMenuItem(rest_id, menu_id):
    Existing = session.query(MenuItem).filter_by(id = menu_id).one()
    if request.method == 'POST':
        if request.form['name']:
            Existing.name = request.form['name']
        session.add(Existing)
        session.commit()
        flash("Menu item editted!")
        return redirect(url_for('showMenu',rest_id = rest_id))
    else: 
        return render_template('editmenuitem.html', rest_id = rest_id, menu_id = menu_id, i = Existing)


#Delete Menu Items
@app.route('/restaurants/<int:rest_id>/<int:menu_id>/delete/',methods=['GET','POST'])
def deleteMenuItem(rest_id,menu_id):
    Existing = session.query(MenuItem).filter_by(id = menu_id).one()
    if request.method == 'POST':
        session.delete(Existing)
        session.commit()
        flash("Menu item deleted!")                
        return redirect(url_for('showMenu',rest_id = rest_id))
    else: 
        return render_template('deletemenuitem.html', rest_id = rest_id, menu_id = menu_id, i = Existing)

#>===============<
#Server run code
#>===============<

if __name__== '__main__':
    app.secret_key = 'super_secret_key'
    app.debug=True
    app.run(host = '0.0.0.0',port = 5000)
