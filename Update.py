import requests
def main():
    open('WalServeUs.py', 'w').write(requests.get('https://raw.githubusercontent.com/hppavilion1/HTTP-WalServeUs/master/WalServeUs.py').text)

if __name__=='__main__':
    main()
