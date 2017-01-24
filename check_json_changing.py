import json
import time
from urllib.request import urlopen

log_file_name = 'json_changing.txt'

log_file = open(log_file_name, 'w')

url = 'https://api.um.warszawa.pl/api/action/wsstore_get/?id=c7238cfe-8b1f-4c38-bb4a-de386db7e776&apikey=c67f064e-90ed-4bea-bd92-686ab39eb916'

start_time = time.time()

last_trams = []

sleep_time = 5
listening_time = 300

x = 1
while True:
    count = "{}.\n".format(x)
    print("{}\n".format(count))
    x += 1
    log_file.write(count)
    try:
        u = urlopen(url).read().decode("utf-8")
    except:
        log = 'Unable to connect with url.\n'
        print(log)
        continue

    rest = json.loads(u)

    trams = rest['result']

    if len(last_trams) == 0:
        log = 'Returned 0 objects.\n'
        print(log)
        log_file.write(log)
        last_trams = trams

    else:
        log = 'Comparison of two trams list after {0} seconds.\n {1}\n'.format(sleep_time, last_trams==trams)

        print(log)
        log_file.write(log)

        last_trams = trams

    if time.time() - start_time > listening_time:
        break

    time.sleep(sleep_time)

log_file.close()