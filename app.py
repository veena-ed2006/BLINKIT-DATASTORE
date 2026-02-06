from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# MODEL
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    price = db.Column(db.Integer)

# LOGIN PAGE
@app.route('/')
def index():
    return render_template('index.html')

# PRODUCTS PAGE
@app.route('/products')
def products():
    items = Product.query.all()
    return render_template('products.html', items=items)

# CREATE
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        db.session.add(Product(name=name, price=price))
        db.session.commit()
        return redirect('/products')
    return render_template('add.html')

# UPDATE
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    item = Product.query.get(id)
    if request.method == 'POST':
        item.name = request.form['name']
        item.price = request.form['price']
        db.session.commit()
        return redirect('/products')
    return render_template('edit.html', item=item)

# DELETE
@app.route('/delete/<int:id>')
def delete(id):
    item = Product.query.get(id)
    db.session.delete(item)
    db.session.commit()
    return redirect('/products')

# API
@app.route('/api/products')
def api():
    data = Product.query.all()
    return jsonify([
        {"id": p.id, "name": p.name, "price": p.price}
        for p in data
    ])

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
