import tempfile
import unittest
import os
import pytest

from app import app as myapp
from applib.app_lib import get_posts, get_accounts, follow, unfollow, like_post, unlike_post
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
    
    post_uuid = 'dd31faa4-ccd8-4ff0-b616-dfc8d2bdfc74'
    username = 'test'
    
    like_post(username, post_uuid)

    posts = get_posts()
    is_liked = False
    for post in posts:
        if post['uuid'] == post_uuid:
            if username in post['likers']:
                is_liked = True
            break
    
    assert is_liked == True

def test_unlike_post(client):

    post_uuid = 'dd31faa4-ccd8-4ff0-b616-dfc8d2bdfc74'
    username = 'test'
    
    unlike_post(username, post_uuid)

    posts = get_posts()
    is_liked = True
    for post in posts:
        if post['uuid'] == post_uuid:
            if username not in post['likers']:
                is_liked = False
            break
    
    assert is_liked == False

def test_follow_user(client):

    username = 'gdbertucci'
    person_to_follow = 'test'
    follow(username, person_to_follow)

    accounts = get_accounts()
    is_following = False
    for account in accounts:
        if username == account['username']:
            if 'test' in account['following']:
                is_following = True
            break
    assert is_following == True

def test_unfollow_user(client):

    username = 'gdbertucci'
    person_to_unfollow = 'test'
    unfollow(username, person_to_unfollow)

    accounts = get_accounts()
    is_following = True
    for account in accounts:
        if username == account['username']:
            if 'test' not in account['followers']:
                is_following = False
            break
    assert is_following == False

