import pytest
from flask import url_for

def test_cart_page_route(client):
    response = client.get(url_for('cart_page'))
    assert response.status_code == 200
    assert b'cart_page' in response.data

def test_cart_page_content(client):
    response = client.get(url_for('cart_page'))
    assert b'Manage shopping cart' in response.data

def test_{route_name}_constraints(client):
    response = client.get(url_for('{route_name}'))
    assert b'secure login' in response.data
    assert b'real-time updates' in response.data