def test_index(client):
    response = client.get('/timeline/')
    assert response.status_code == 200
