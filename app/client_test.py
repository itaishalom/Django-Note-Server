import requests

# Base URL of the Django server hosting the REST API
BASE_URL = 'http://127.0.0.1:8000/'
username = 'new_user'
password = 'password123'


def login():
    # Create a dictionary containing the user's credentials
    credentials = {
        'username': username,
        'password': password
    }

    # Send a POST request to the login endpoint with the user's credentials
    response = requests.post(BASE_URL + 'users/login/', data=credentials)

    # Check if the request was successful (HTTP status code 200)
    if response.status_code == 200:
        # Extract the token from the response JSON
        token = response.json().get('token')

        # Print the token
        print('Token:', token)
        return token
        # Store the token securely for subsequent requests
        # Example: save it in a variable or file, or set it in a session
    else:
        # Print an error message if the request failed
        print('Login failed. Status code:', response.status_code)


def list_notes(token, tag='', query=''):
    headers = {'Authorization': f'Token {token}'}
    params = {'tag': tag, 'query': query}

    response = requests.get(BASE_URL + 'notes/', headers=headers, params=params)
    print('List of Notes:')
    print(response.json())
    return response.json()


def fetch_all_notes(token, tag='', query=''):
    headers = {'Authorization': f'Token {token}'}
    params = {'tag': tag, 'query': query}
    return iterate_over_notes_result([], params, path='notes/', headers=headers)


def fetch_all_notes_public(tag='', query=''):
    params = {'tag': tag, 'query': query}
    return iterate_over_notes_result([], params, path='notes/public', headers={})


def iterate_over_notes_result(notes, params, path, headers):
    page = 1
    while True:
        # Make a GET request to the API endpoint with pagination parameters
        response = requests.get(BASE_URL + f'{path}?page={page}', params=params, headers=headers)
        status_code = response.status_code
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()

            # Extract notes from the current page
            results = data['results']
            notes.extend(results)

            # Check if there are more pages
            if data['next']:
                # Move to the next page
                page += 1
            else:
                # No more pages, break out of the loop
                break
        else:
            print('Failed to fetch notes:', response.status_code)
            break
    # Process and display all fetched notes
    display_notes(notes)
    print(f'Total notes: {len(notes)}')
    return notes, status_code


# Function to display notes
def display_notes(notes):
    # Display notes
    for note in notes:
        print(f'Note ID: {note["id"]}, Title: {note["title"]}, Body: {note["body"]}')


def delete(token, messages):
    if len(messages) == 0:
        return
    headers = {'Authorization': f'Token {token}'}
    for message in messages:
        note_id = message['id']
        response = requests.delete(BASE_URL + f'notes/{note_id}', headers=headers)

        # Processing the response
        if response.status_code == 204:
            print("Note deleted successfully.")
        elif response.status_code == 404:
            print("Note not found.")
        else:
            print("Failed to delete note:", response.text)


def add_note(token):
    headers = {'Authorization': f'Token {token}'}
    note_data = {
        'title': 'New Note Title2',
        'body': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
        'tags': ['tag1']
    }
    response = requests.post(BASE_URL + 'notes/', json=note_data, headers=headers)
    print('Response from server:')
    print(response.json())


def update(token, note_id):
    headers = {'Authorization': f'Token {token}'}
    note_data = {
        'title': 'updated',
        'body': 'Lorem.',
        'tags': ['tag2']
    }
    response = requests.put(BASE_URL + f'notes/{note_id}', json=note_data, headers=headers)
    print('Response from server:')
    print(response.json())


def create_user():
    user_data = {
        'username': username,
        'password': password,
        'email': 'new_user@example.com'
    }

    response = requests.post(BASE_URL + 'users/add/', data=user_data)

    if response.status_code == 201:  # 201 Created
        print('User created successfully:', response.json())
    else:
        print('Error creating user:', response.text)


def main():
    create_user()
    [result, status] = fetch_all_notes_public('')
    assert len(result) == 0
    assert status == 200
    token = login()
    [result, status] = fetch_all_notes(token)
    delete(token, result)

    add_note(token)
    [result, status] = fetch_all_notes(token)
    assert len(result) == 1
    assert status == 200

    update(token, result[0]['id'])

    # List notes again to see the newly added note

    [result, status] = fetch_all_notes(token, tag='tag2')
    assert len(result) == 1
    assert status == 200

    [result, status] = fetch_all_notes(token, tag='tag4')
    assert len(result) == 0
    assert status == 200

    [result, status] = fetch_all_notes(token, query='Lorem')
    assert len(result) == 1
    assert status == 200

    delete(token, result)
    [result, status] = fetch_all_notes(token)
    assert len(result) == 0
    assert status == 200



if __name__ == "__main__":
    main()
