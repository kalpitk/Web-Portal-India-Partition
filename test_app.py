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
    for line in open('schema.sql'):
        cursor.execute(line)
    app.config['TESTING'] = True
    client = app.test_client()
    return client

def login(client, username, password):
    return client.post('/login', data=dict(
        username=username,
        password=password
    ), follow_redirects=True)


def logout(client):
    return client.get('/logout', follow_redirects=True)

def test_pages(client):
    res = client.get('/home')
    assert res.status == '200 OK'