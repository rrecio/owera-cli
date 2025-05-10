import pytest
from flask import url_for

def test_product_list_route(client):
    response = client.get(url_for('product_list'))
    assert response.status_code == 200
    assert b'product_list' in response.data

def test_product_list_content(client):
    response = client.get(url_for('product_list'))
    assert b'Browse products with filters' in response.data

def test_{route_name}_constraints(client):
    response = client.get(url_for('{route_name}'))
    assert b'responsive design' in response.data
    assert b'filtering' in response.data
    assert b'sorting' in response.data
    assert b'pagination' in response.data