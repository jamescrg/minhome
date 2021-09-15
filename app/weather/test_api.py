import api

def test_response_status():
    url = 'https://api.thedogapi.com/v1/breeds/1'
    response = api.get_response(url)
    assert response.status_code == 200

def test_response_text():
    url = 'https://api.thedogapi.com/v1/breeds/1'
    response = api.get_response(url)
    assert 'Affenpinscher' in response.text

def test_write_response():
    url = 'https://api.thedogapi.com/v1/breeds/1'
    response = api.get_response(url)
    api.write_response(response, 'data_testing.json')
    file = open('data_testing.json', 'r')
    stored_text = file.read()
    assert stored_text == response.text
