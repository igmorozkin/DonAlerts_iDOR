import requests
import time

from random import randrange
from concurrent.futures import ThreadPoolExecutor
import re

counter = 0
discovered = []   # List of already found audios


def fetch(session, audio_id: tuple):
    global counter
    global discovered

    url = 'http://static.donationalerts.ru/audiodonations/{0}/{0}{1}.wav'.format(*audio_id)
    response = session.get(url)
    counter += 1
    if counter % 100 == 0:
        print(f'processed count: {counter}; discovered: {len(discovered)}')

    if response.status_code == 200:
        if audio_id not in discovered:
            discovered.append(audio_id)
            print(f'connection done: {url}')
            with open('result.txt', 'a') as f:  # Saving result to result.txt
                f.write(url + '\n')
        else:
            print(f'connection done, but audio has already been discovered previously: {url}')


def make_audio_id():
    r1 = int('6' + str(randrange(1111, 9999)))
    r2 = randrange(111, 999)
    return (r1, r2)


if __name__ == '__main__':
    # Try to load audio identifiers that has already been discovered previously
    try:
        with open('result.txt', 'r') as f:
            audio_url_pattern = re.compile(
                r'http://static.donationalerts.ru/audiodonations/(\d{5})/\d{5}(\d{3})\.wav')
            for line in f.read().splitlines():
                m = re.match(audio_url_pattern, line)
                if m:
                    discovered.append(
                            (int(m.group(1)), int(m.group(2)))
                        )
    except FileNotFoundError:
        pass

    session = requests.Session()

    with ThreadPoolExecutor(64) as executor:
        while True:
            audio_id = make_audio_id()
            executor.submit(fetch, session, audio_id)

            time.sleep(0.01)
