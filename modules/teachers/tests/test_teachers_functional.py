def test_index(client):
    response = client.get('/teachers/')
    assert response.status_code == 200
