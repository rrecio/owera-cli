from flask import render_template, redirect, url_for, flash, request
from .models import db

def register_routes(app):
    @app.route('/')
    def index():
        return render_template('index.html')
    
    @app.route('/health')
    def health():
        return {'status': 'ok'}

    @app.route('/product_list')
    def product_list():
        return render_template('product_list.html')

    @app.route('/product_page')
    def product_page():
        return render_template('product_page.html')

    @app.route('/cart_page')
    def cart_page():
        return render_template('cart_page.html')

    @app.route('/checkout_page')
    def checkout_page():
        return render_template('checkout_page.html')