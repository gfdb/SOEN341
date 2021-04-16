from json import load, dump
from flask import redirect, url_for, session


def auth_login(username, password):
    accounts = get_accounts()
    for account in accounts:
        if username == account['username'] and password == account['password']:    
            return True
    return False

def create_account(new_account):
    accounts = get_accounts()
    accounts.append(new_account)
    with open('app/static/accounts.json', 'w') as all_accounts:
        dump(accounts, all_accounts, indent=4, sort_keys=True)

def get_posts():
    with open('app/static/posts.json', 'r') as read_file:
        posts = load(read_file)
        read_file.close()
    return posts

def post_comment(post_uuid, comment):
    posts = get_posts()
    for post in posts:
        if post['uuid'] == post_uuid:
            post['comments'].append(comment)
    with open('app/static/posts.json', 'w') as write_file:
        dump(posts, write_file, indent=4, sort_keys=True)
        write_file.close()

def get_accounts():
    with open('app/static/accounts.json', 'r') as read_accounts:
        accounts = load(read_accounts)
        read_accounts.close()
    return accounts

def swap_theme(page):
    if session.get('color_theme'):
        if session.get('color_theme') == 'dark':
            session['color_theme'] = 'light'
            return redirect(url_for(page))
        if session.get('color_theme') == 'light':
            session['color_theme'] = 'dark'
            return redirect(url_for(page))
    session['color_theme'] = 'light'
    return redirect(url_for(page))

def post_a_picture(new_post):
    posts = get_posts()
    with open('app/static/posts.json', 'w') as all_posts:
        posts.insert(0, new_post)
        dump(posts, all_posts, indent=4, sort_keys=True)
        all_posts.close()

def follow(username, person_to_follow):
    accounts = get_accounts()
    for account in accounts:
        if account['username'] == username:
            account['following'].append(person_to_follow)
            break
    with open('app/static/accounts.json', 'w') as all_accounts:
        dump(accounts, all_accounts, indent=4, sort_keys=True)


def unfollow(username, person_to_unfollow):
    accounts = get_accounts()
    for account in accounts:
        if account['username'] == username:
            account['following'].remove(person_to_unfollow)
            break
    with open('app/static/accounts.json', 'w') as all_accounts:
        dump(accounts, all_accounts, indent=4, sort_keys=True)


def like_post(person_liking, post_uuid):
    posts = get_posts()
    for post in posts:
        if post['uuid'] == post_uuid:
            if person_liking not in post['likers']:
                post['likers'].append(person_liking)
                break
            else:
                break
    with open('app/static/posts.json', 'w') as all_posts:
        dump(posts, all_posts, indent=4, sort_keys=True)


def unlike_post(person_unliking, post_uuid):
    posts = get_posts()
    for post in posts:
        if post['uuid'] == post_uuid:
            if person_unliking in post['likers']:
                post['likers'].remove(person_unliking)
                break
            else:
                break
    with open('app/static/posts.json', 'w') as all_posts:
        dump(posts, all_posts, indent=4, sort_keys=True)


def get_num_followers(username):
    accounts = get_accounts()
    for account in accounts:
        if account['username'] == username:
            return len(account['followers'])

def get_num_following(username):
    accounts = get_accounts()
    for account in accounts:
        if account['username'] == username:
            return len(account['following'])

def get_profile_pic(username):
    accounts = get_accounts() 
    for account in accounts:
        if account['username'] == username:
            return account['profile_pic']

def set_profile_pic(username, profile_pic):
    accounts = get_accounts()
    for account in accounts:
        if account['username'] == username:
            account['profile_pic'] = profile_pic
    with open('app/static/accounts.json', 'w') as acc:
        dump(accounts, acc, indent=4, sort_keys=True)