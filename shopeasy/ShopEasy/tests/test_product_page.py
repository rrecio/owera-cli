import pytest
from flask import url_for

def test_product_page_route(client):
    response = client.get(url_for('product_page'))
    assert response.status_code == 200
    assert b'product_page' in response.data

def test_product_page_content(client):
    response = client.get(url_for('product_page'))
    assert b'View product details' in response.data

def test_{route_name}_constraints(client):
    response = client.get(url_for('{route_name}'))
    assert b'responsive design' in response.data