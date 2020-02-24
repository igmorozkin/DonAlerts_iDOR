import requests
import time

from random import randrange
from concurrent.futures import ThreadPoolExecutor

counter = 0

def fetch(session, url):
    response = session.get(url)
    global counter
    counter += 1
    if counter % 100 == 0:
        print('processed count:', counter)

    if response.status_code == 200:
        print('connection done: ', url)
        with open('result.txt', 'a') as f:  # Saving result to result.txt
            f.write(url + '\n')

def make_url():
    r1 = randrange(11111, 99999)
    r2 = randrange(111, 999)
    return f'http://static.donationalerts.ru/audiodonations/{r1}/{r1}{r2}.wav'


if __name__ == '__main__':
    session = requests.Session()

    with ThreadPoolExecutor(64) as executor:
        while True:
            url = make_url()
            executor.submit(fetch, session, url)

            time.sleep(0.01)
