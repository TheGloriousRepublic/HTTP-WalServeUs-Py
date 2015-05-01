from requests import get

open('WalServeUs.py', 'w').write(get('https://raw.githubusercontent.com/hppavilion1/HTTP-WalServeUs/master/WalServeUs.py'))
open('update.py', 'w').write(get('https://raw.githubusercontent.com/hppavilion1/HTTP-WalServeUs/master/Update.py'))
