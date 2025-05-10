import pytest
from flask import url_for

def test_checkout_page_route(client):
    response = client.get(url_for('checkout_page'))
    assert response.status_code == 200
    assert b'checkout_page' in response.data

def test_checkout_page_content(client):
    response = client.get(url_for('checkout_page'))
    assert b'Complete purchases' in response.data

def test_{route_name}_constraints(client):
    response = client.get(url_for('{route_name}'))
    assert b'secure login' in response.data
    assert b'use a database' in response.data