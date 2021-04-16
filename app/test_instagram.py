import tempfile
import unittest
import os
import pytest

from app import app as myapp
from app import like_post, unlike_post, follow, unfollow
from flask import url_for, request
import re


@pytest.fixture
def client():
    db_fd, myapp.config['DATABASE'] = tempfile.mkstemp()
    myapp.config['TESTING'] = True

    with myapp.test_client() as client:
        client.allow_subdomain_redirects = True
        yield client


def test_register_page(client):
    """Make sure login and logout works."""

    assert client.get('/register').status_code == 200

def test_login_page(client):

    assert client.get('/login').status_code == 200

def test_login(client):
    
    response = client.post('/login', data={"username": "gdbertucci", "password": "6969420"})
    assert response.status_code == 200

def test_timeline_page(client):

    assert client.get('/timeline').status_code == 200

def test_home_page(client):

    assert client.get('/').status_code == 200

def test_posting_page(client):

    assert client.get('/posting').status_code == 200

def test_post_not_logged_in(client):
    
    assert client.get('/posting').status_code == 200

def test_logout_page(client):
    # status code 302 signifies a redirect to timeline after logging out
    assert client.get('/logout').status_code == 302 

def test_like_post(client):
    
    like = like_post('test', 'dd31faa4-ccd8-4ff0-b616-dfc8d2bdfc74')
    
    assert like == True

def test_unlike_post(client):

    unlike = unlike_post('test', 'dd31faa4-ccd8-4ff0-b616-dfc8d2bdfc74')

    assert unlike == True

def test_follow_user(client):

    do_follow = follow('gdbertucci', 'test')

    assert do_follow == True

def test_unfollow_user(client):

    do_unfollow = unfollow('gdbertucci', 'test')

    assert do_unfollow == True



