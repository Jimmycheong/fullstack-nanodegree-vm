#>===============<
#Import dependancies 
#>===============<

from flask import Flask, render_template, url_for, redirect,request, jsonify
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Restaurant, Base, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


#>===============<
#JSON Extraction
#>===============<
@app.route('/restaurant/JSON')
def restaurantJSON():
    restaurant = session.query(Restaurant).all()
    return jsonify(Restaurant=[r.serialize for r in restaurant])

@app.route('/restaurant/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id)
    return jsonify(MenuItems=[i.serialize for i in items])

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def restaurantMenuItemJSON(restaurant_id, menu_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id, id=menu_id)
    return jsonify(MenuItems=[i.serialize for i in items])

 
#>===============<
#Routing
#>===============<

@app.route('/')
@app.route('/home')
def landingPage():
    Existing = session.query(Restaurant).all()    
    return render_template('landing.html', Existing = Existing)

@app.route('/restaurant')
def showRestaurants():
    Existing = session.query(Restaurant).all()    
    return render_template('restaurants.html', Existing = Existing)

@app.route('/restaurant/new/', methods = ["GET", "POST"])
def newRestaurant():
    if request.method == 'POST':
        if request.form['name']:
            newRestaurant = Restaurant(name = request.form['name'])
            session.add(newRestaurant)
            session.commit()
            return redirect(url_for('showRestaurants'))
    else: 
        return render_template('newRestaurant.html')

@app.route('/restaurant/<int:restaurant_id>/edit', methods = ["GET", "POST"])
def editRestaurant(restaurant_id):
    Existing = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':        
        if request.form['name']:
            Existing.name = request.form['name']
            session.add(Existing)
            session.commit()
            return redirect(url_for('showRestaurants'))
    else: 
        return render_template('editRestaurant.html', restaurant_id = restaurant_id, r = Existing)

@app.route('/restaurant/<int:restaurant_id>/delete', methods = ['GET', 'POST'])
def deleteRestaurant(restaurant_id):
    Existing = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        session.delete(Existing)
        session.commit()
        return redirect(url_for('showRestaurants'))
    else:     
        return render_template('deleteRestaurant.html', restaurant_id = restaurant_id, r = Existing)

@app.route('/restaurant/<int:restaurant_id>')
@app.route('/restaurant/<int:restaurant_id>/menu')
def showMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id)
    count = 0
    for item in items:
        count += 1
    if count > 0:
        return render_template('menu.html', restaurant = restaurant, items = items, restaurant_id = restaurant_id)
    else:
        return render_template('menu.html', restaurant = restaurant, restaurant_id = restaurant_id)

@app.route('/restaurant/<int:restaurant_id>/menu/new', methods = ['GET', 'POST'])
def newMenuItem(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id)
    if request.method == "POST":
        if request.form['name'] and request.form['description'] and request.form['price']:
            newItem = MenuItem(name = request.form['name'],
                               description = request.form['description'],
                               price = request.form['price'],
                               restaurant_id = restaurant_id,
                               course = request.form['course'],)
            session.add(newItem)
            session.commit()
        return redirect(url_for('showMenu',restaurant_id = restaurant_id))
    else:
        return render_template('newMenuItem.html', restaurant_id = restaurant_id)

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit', methods = ['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id, id = menu_id).one()
    if request.method == "POST":
        if request.form['name']:
            items.name = request.form['name']
            session.add(items)
            session.commit()
            return redirect(url_for('showMenu', restaurant_id = restaurant_id))
    else: 
        return render_template('editMenuItem.html', items=items,restaurant_id =restaurant_id, menu_id = menu_id)

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete', methods = ['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id, id = menu_id).one()
    if request.method == "POST":
        session.delete(items)
        session.commit()
        return redirect(url_for('showMenu', restaurant_id = restaurant_id))
    else:
        return render_template('deleteMenuItem.html', items=items, restaurant_id = restaurant_id, menu_id = menu_id)

#>===============<
#Server run code
#>===============<

if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
