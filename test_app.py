from app import app
import pytest
import os
import mysql.connector
from flask import (Flask, g, redirect, render_template, request, session,
                   url_for)

mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database = 'PROJECT'
)
cursor = mydb.cursor(buffered=True)

@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()
    return client

def login(client, username, password):
    return client.post('/login', data = dict(
        username = username,
        password = password
    ), follow_redirects = True)

def signup(client, username, name, email, password):
    return client.post('/sign_up', data = dict(
        username = username,
        name = name,
        email = email,
        password = password
    ), follow_redirects = True)

def logout(client):
    return client.get('/logout', follow_redirects=True)

def test_pages(client):
    res = client.get('/home')
    assert res.status_code == 200

def test_login(client):
    # test correct password
    res = login(client, 'admin', 'admin')
    assert res.status_code == 200
    res = login(client, 'collab', 'collab')
    assert res.status_code == 200
    res = login(client, 'mod', 'mod')
    assert res.status_code == 200

    # test incorrect password
    res = login(client, 'admin', 'incorrect_pass')
    assert res.status_code == 401

def test_signup(client):
    res = signup(client, 'user1', 'abc@example.com', 'User', 'password')
    res = login(client, 'user1', 'password')
    assert res.status_code == 200

def test_profile(client):
    res = client.get('/profile/collab')
    print res.data
    assert res.data.find('Collab') != -1
    assert res.data.find('collab@example.com') != -1
    assert res.data.find('d5029374377771fd628239fd1f4e9d02') == -1
    assert res.data.find('Moderator') == -1
    assert res.data.find('Admin') == -1
    assert res.data.find('/post/1') != -1
    res = client.get('/profile/admin')
    assert res.data.find('Moderator') != -1
    assert res.data.find('Admin') != -1
    res = client.get('/profile/mod')
    assert res.data.find('Moderator') != -1
    assert res.data.find('Admin') == -1