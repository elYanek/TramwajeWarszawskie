from urllib.request import urlopen
import json
import time
import datetime

url = 'https://api.um.warszawa.pl/api/action/wsstore_get/?id=c7238cfe-8b1f-4c38-bb4a-de386db7e776&apikey=c67f064e-90ed-4bea-bd92-686ab39eb916'

log_file_name = r'api_logs.txt'
log_file = open(log_file_name, 'w')

def full_log_message(log_number, message, time):
    full_log = "Log " + str(log_number) + \
               "\n====================\n\n" \
               + message + '\n' \
               + 'at time: ' + str(time) \
               + '\n' \
               + "\n===================="

    return full_log

def write_log(message):
    log_file.write(str(message))


def log_message(log_number, url):
    try:
        cur_time = datetime.datetime.now()
        u = urlopen(url).read().decode("utf-8")

        rest = json.loads(u)
        trams = rest['result']

        trams_count = len(trams)

        if trams_count == 0:
            log = 'Returned 0 elements from JSON.'

            full_log = full_log_message(log_number, log, cur_time)

            return full_log
        else:
            log = '\nLog {0}.\nData has been downloaded from api using JSON in count: {1}.\nTime: {2}.\n'.format(log_number,trams_count, cur_time)
            return log
    except:
        log = "Couldn't connect with api using url."

        full_log = full_log_message(log_number, log, cur_time)

        return full_log


x = 1
start_time = time.time()
while True:
    message = log_message(x, url)

    write_log(message)
    print(message)
    time.sleep(15)
    end_time = time.time()

    if end_time - start_time > 3600:
        break
    x += 1

log_file.close()