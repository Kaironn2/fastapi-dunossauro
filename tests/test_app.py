from http import HTTPStatus

from src.schemas import UserPublic


def test_root_returns_hello_world(client):
    response = client.get('/')

    assert response.json() == {'message': 'hello world'}
    assert response.status_code == HTTPStatus.OK


def test_create_user(client):
    payload = {'username': 'jonh', 'email': 'jonh@gmail.com', 'password': '123'}
    response = client.post('/users/', json=payload)

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {'id': 1, 'email': 'jonh@gmail.com', 'username': 'jonh'}


def test_create_user_username_already_exists(client, user):
    payload = {'username': 'jonh', 'email': 'jonh@gmail.com', 'password': '123'}
    response = client.post('/users/', json=payload)

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Username already exists.'}


def test_create_user_email_already_exists(client, user):
    payload = {'username': 'jonathas', 'email': 'jonh@gmail.com', 'password': '123'}
    response = client.post('/users/', json=payload)

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Email already exists.'}


def test_read_users(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_read_user_by_id(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == user_schema


def test_read_user_by_id_not_found(client):
    response = client.get('/users/2')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'This user does not exists'}


def test_read_users_with_users(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_update_user(client, user):
    payload = {'username': 'jonh', 'email': 'jonh@gmail.com', 'password': 'secret'}
    response = client.put('/users/1', json=payload)

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'username': 'jonh',
        'email': 'jonh@gmail.com',
    }


def test_update_not_found_user(client):
    payload = {'username': 'alice', 'email': 'alice@gmail.com', 'password': 'secret'}
    response = client.put('/users/2', json=payload)

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'This user does not exists'}


def test_delete_user(client, user):
    response = client.delete('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_delete_not_found_user(client):
    response = client.delete('/users/1')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'This user does not exists'}
