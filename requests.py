url = 'http://127.0.0.1:5000/'
params ={'query': 'that movie was boring'}
response = requests.get(url, params)
response.json()

Output: {'confidence': 0.128, 'prediction': 'Negative'}
