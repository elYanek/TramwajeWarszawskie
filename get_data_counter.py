# -*- coding: utf-8 -*-

import time
import datetime
import get_json

while True:
    print("\n################################")
    print("Adding values to database.\n")
    start_time = time.time()
    get_json.main()
    elapsed_time = time.time() - start_time

    print('Elapsed time: {0} s.'.format(elapsed_time))
    print('Execute time: {0}'.format(datetime.datetime.now()))
    print("\n################################")
    time.sleep(60)