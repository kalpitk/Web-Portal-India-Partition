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

def test_home(client):
    assert client.get('/home').status_code == 200

def test_login(client):
    # test correct password
    assert login(client, 'admin', 'admin').status_code == 200 
    assert login(client, 'collab', 'collab').status_code == 200
    assert login(client, 'mod', 'mod').status_code == 200

    # test incorrect password
    assert login(client, 'admin', 'incorrect_pass').status_code == 401

def test_signup(client):
    signup(client, 'user1', 'abc@example.com', 'User', 'password')
    res = login(client, 'user1', 'password')
    assert res.status_code == 200

def test_profile(client):
    res = client.get('/profile/collab')
    assert res.data.find('Collab') != -1
    assert res.data.find('collab@example.com') != -1
    assert res.data.find('d5029374377771fd628239fd1f4e9d02') == -1
    assert res.data.find('Moderator') == -1
    assert res.data.find('Admin') == -1
    assert res.data.find('/post/1') != -1
    assert res.data.find('/post/2') == -1
    res = client.get('/profile/admin')
    assert res.data.find('Moderator') != -1
    assert res.data.find('Admin') != -1
    res = client.get('/profile/mod')
    assert res.data.find('Moderator') != -1
    assert res.data.find('Admin') == -1

    assert client.get('/profile/some_invalid_username').status_code != 200

def test_posts(client):
    assert client.get('/post/1').status_code == 200
    assert client.get('/post/2').status_code == 302

    login(client, 'mod', 'mod') 
    assert client.get('/post/2').status_code == 200

    login(client, 'collab', 'collab')
    assert client.get('/post/2').status_code == 200
    assert client.get('/post/4').status_code == 200

def test_dashboard(client):
    assert client.get('/dashboard').status_code != 200
    
    login(client, 'collab', 'collab')
    res = client.get('/dashboard')
    assert res.status_code == 200
    assert res.data.find('/post/1') != -1
    assert res.data.find('/post/2') != -1

def test_post_list(client):
    res = client.get('/post_list').data
    assert res.find('/post/1') != -1
    assert res.find('/post/3') != -1

    res = client.get('/post_list?src_lat=-34.9&src_lng=150.7').data
    assert res.find('/post/1') != -1
    assert res.find('/post/3') != -1

