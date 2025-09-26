from http import HTTPStatus


def test_root_returns_hello_world(client):
    response = client.get('/')

    assert response.json() == {'message': 'hello world'}
    assert response.status_code == HTTPStatus.OK


def test_create_user(client):
    payload = {'username': 'jonh', 'email': 'jonh@gmail.com', 'password': '123'}
    response = client.post('/users/', json=payload)

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {'id': 1, 'email': 'jonh@gmail.com', 'username': 'jonh'}


def test_read_users(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [{'id': 1, 'email': 'jonh@gmail.com', 'username': 'jonh'}]}


def test_update_user(client):
    payload = {'username': 'alice', 'email': 'alice@gmail.com', 'password': 'secret'}
    response = client.put('/users/1', json=payload)

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'username': 'alice',
        'email': 'alice@gmail.com',
    }


def test_update_not_found_user(client):
    payload = {'username': 'alice', 'email': 'alice@gmail.com', 'password': 'secret'}
    response = client.put('/users/2', json=payload)

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_delete_user(client):
    response = client.delete('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'username': 'alice',
        'email': 'alice@gmail.com',
    }


def test_delete_not_found_user(client):
    payload = {'username': 'alice', 'email': 'alice@gmail.com', 'password': 'secret'}
    response = client.put('/users/2', json=payload)

    assert response.status_code == HTTPStatus.NOT_FOUND
