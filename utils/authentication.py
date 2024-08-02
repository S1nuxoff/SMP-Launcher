import os
import json
from utils.firebase_init import db, smpl_configs_dir, auth as firebase_auth, firebase_client
import firebase_admin
from firebase_admin import auth

firebase_client_auth = firebase_client.auth()

def register_user(email, password, username):
    try:
        if username_exists(username):
            raise ValueError('Username already exists.')

        user = auth.create_user(
            email=email,
            password=password
        )
        print('Successfully created new user:', user.uid)

        user_data = {
            'name': username,
            'email': email,
            'skin': '',
            'online': False,
            'friends': {}
        }
        db.collection('users').document(user.uid).set(user_data)
        print(f"User {username} added to Firestore with UID: {user.uid}")
        return user.uid
    except firebase_admin._auth_utils.EmailAlreadyExistsError:
        print('Email already exists.')
        raise
    except Exception as e:
        print('Error creating new user:', str(e))
        raise

def username_exists(username):
    users_ref = db.collection('users')
    query = users_ref.where('name', '==', username).get()
    return bool(query)

def authenticate_user(email, password):
    try:
        user = firebase_client_auth.sign_in_with_email_and_password(email, password)
        print('Successfully authenticated user:', user['localId'])
        user_data = get_user_data(user['localId'])
        
        if user_data:
            username = user_data.get('name', 'unknown')
            update_config_file(username, user['localId'])
        else:
            print(f"No user data found in Firestore for UID: {user['localId']}")
        return user['localId']
    except Exception as e:
        print('Error authenticating user:', str(e))
        raise

def get_user_data(user_id):
    user_doc = db.collection('users').document(user_id).get()
    return user_doc.to_dict() if user_doc.exists else None

def update_config_file(username, user_id):
    config_path = smpl_configs_dir
    try:
        with open(config_path, 'r') as file:
            config_data = json.load(file)

        if 'accounts' not in config_data:
            config_data['accounts'] = []

        new_account = {
            'username': username,
            'uid': user_id
        }
        config_data['accounts'].append(new_account)

        with open(config_path, 'w') as file:
            json.dump(config_data, file, indent=4)
        print(f"User {username} added to config file with UID: {user_id}")
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error updating config file: {e}")
