def test_index(client):
    response = client.get('/alumni/')
    assert response.status_code == 200
