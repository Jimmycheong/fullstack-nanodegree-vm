#>===============<
#Import dependancies 
#>===============<

from flask import Flask, render_template, url_for, redirect,request, jsonify
app = Flask(__name__)


#>===============<
#Fake dictionary  
#>===============<

#Fake Restaurants
restaurant = {'name': 'The CRUDdy Crab', 'id': '1'}
restaurants = [{'name': 'The CRUDdy Crab', 'id': '1'}, {'name':'Blue Burgers', 'id':'2'},{'name':'Taco Hut', 'id':'3'}]

#Fake Menu Items
items = [ {'name':'Cheese Pizza', 'description':'made with fresh cheese', 'price':'$5.99','course' :'Entree', 'id':'1'}, {'name':'Chocolate Cake','description':'made with Dutch Chocolate', 'price':'$3.99', 'course':'Dessert','id':'2'},{'name':'Caesar Salad', 'description':'with fresh organic vegetables','price':'$5.99', 'course':'Entree','id':'3'},{'name':'Iced Tea', 'description':'with lemon','price':'$.99', 'course':'Beverage','id':'4'},{'name':'Spinach Dip', 'description':'creamy dip with fresh spinach','price':'$1.99', 'course':'Appetizer','id':'5'} ]

item =  {'name':'Cheese Pizza','description':'made with fresh cheese','price':'$5.99','course' :'Entree'}
#items = [] #empty items debug

#>===============<
#JSON Extraction
#>===============<

@app.route('/restaurant/JSON')
def restaurantJSON():
    rests = restaurants
    return jsonify(Restaurant=[r.serialize for r in rests])

#@app.route('/restaurant/<int:restaurant_id>/JSON')

#@app.route('/restaurant/<int:restaurant_id>/<menu_id>/JSON')

 
#>===============<
#Routing
#>===============<

@app.route('/')
@app.route('/restaurant')
def showRestaurants():
    return render_template('restaurants.html', restaurants = restaurants)

@app.route('/restaurant/new/', methods = ["GET", "POST"])
def newRestaurant():
    if request.method == 'POST':
        if request.form['name']:
            latestid = len(restaurants)
            restaurants.append({
                "name":request.form['name'],
                "id":latestid})            
            return redirect(url_for('showRestaurants'))
    else: 
        return render_template('newRestaurant.html')

@app.route('/restaurant/<int:restaurant_id>/edit', methods = ["GET", "POST"])
def editRestaurant(restaurant_id):
    if request.method == 'POST':
        if request.form['name']:
            restaurants[restaurant_id-1]['name'] = request.form['name']
            return redirect(url_for('showRestaurants'))
    else: 
        Existing = restaurants[restaurant_id -1]
        return render_template('editRestaurant.html', restaurant_id = restaurant_id, r = Existing)

@app.route('/restaurant/<int:restaurant_id>/delete', methods = ['GET', 'POST'])
def deleteRestaurant(restaurant_id):
    if request.method == 'POST':
        restaurants.pop(restaurant_id -1)
        return redirect(url_for('showRestaurants'))
    else:     
        Existing = restaurants[restaurant_id - 1]
        return render_template('deleteRestaurant.html', restaurant_id = restaurant_id, r = Existing)

@app.route('/restaurant/<int:restaurant_id>')
@app.route('/restaurant/<int:restaurant_id>/menu')
def showMenu(restaurant_id):
    Existingr = restaurants[restaurant_id - 1]
    Entrees = []
    Appes = []
    Desserts = []
    Bevs = []
    for i in items:
        if i['course'] == 'Entree':
            Entrees.append(i)
        if i['course'] == 'Appetizer':
            Appes.append(i)
        if i['course'] == 'Beverage':
            Bevs.append(i)
        if i['course'] == 'Dessert':
            Desserts.append(i)            
    return render_template('menu.html', restaurant_id = restaurant_id, r = Existingr, Entrees = Entrees, Appes = Appes, Desserts = Desserts, Bevs = Bevs, items=items)

@app.route('/restaurant/<int:restaurant_id>/menu/new', methods = ['GET', 'POST'])
def newMenuItem(restaurant_id):
    if request.method == "POST":
        if request.form['name'] and request.form['description'] and request.form['price']:
            latestid = len(items)
            items.append({
                "name":request.form['name'],
                "course":request.form['course'],
                "id": str(latestid),
                "price": request.form['price'],
                "description":request.form['description'],
                          })
            return redirect(url_for('showMenu',restaurant_id = restaurant_id))
    else:
        return render_template('newMenuItem.html', restaurant_id = restaurant_id)

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit', methods = ['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    if request.method == "POST":
        if request.form['name']:
            items[menu_id - 1]['name'] = request.form['name']
            return redirect(url_for('showMenu', restaurant_id = restaurant_id))
    else: 
        Existing = items[menu_id-1]
        return render_template('editMenuItem.html', restaurant_id =restaurant_id, menu_id = menu_id, i = Existing)

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete', methods = ['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    if request.method == "POST":
        items.pop(menu_id - 1)
        return redirect(url_for('showMenu', restaurant_id = restaurant_id))
    existingmi = items[menu_id - 1]
    return render_template('deleteMenuItem.html', restaurant_id = restaurant_id, menu_id = menu_id, i = existingmi)

#>===============<
#Server run code
#>===============<

if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
