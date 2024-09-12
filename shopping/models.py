from datetime import datetime

from shopping import db

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    available = db.Column(db.Boolean, default=True)
    quantity = db.Column(db.Integer, default=0)
    image_filename = db.Column(db.String(100), nullable=False)  # Adicione esta linha

    order_items = db.relationship('OrderItem', back_populates='product')



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)  # Alterado para unique=True
    password = db.Column(db.String(100), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)  # Adicionado para diferenciar administradores

    orders = db.relationship('Order', back_populates='user')


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='pending')  # Ex: 'pending', 'paid', 'shipped', 'delivered'
    pix_code = db.Column(db.String(255), nullable=True)

    user = db.relationship('User', back_populates='orders')
    order_items = db.relationship('OrderItem', back_populates='order')


class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)  # Preço no momento da compra

    order = db.relationship('Order', back_populates='order_items')
    product = db.relationship('Product', back_populates='order_items')
