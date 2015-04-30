import requests
open('WalServeUs.py', 'w').write(requests.get('http://127.0.0.1/WalServeUs.py').text)
