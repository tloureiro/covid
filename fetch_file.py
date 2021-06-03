import requests
import os
import datetime
from dateutil.parser import parse as parsedate
import pytz
import urllib.request
import sys
import time


def report_hook(count, block_size, total_size):
    global start_time
    if count == 0:
        start_time = time.time()
        return
    duration = time.time() - start_time
    progress_size = int(count * block_size)
    speed = int(progress_size / (1024 * duration))
    percent = int(count * block_size * 100 / total_size)
    sys.stdout.write("\rDonwloading file...%d%%, %d MB, %d KB/s, %d seconds passed" %
                     (percent, progress_size / (1024 * 1024), speed, duration))
    sys.stdout.flush()


local_file_path = './data/main.csv'
remote_file_path = 'https://storage.googleapis.com/covid19-open-data/v2/main.csv'
remote_file_path_vaccinations = 'https://storage.googleapis.com/covid19-open-data/v2/vaccinations.csv'
local_file_path_vaccinations = './data/vaccinations.csv'
utc = pytz.UTC

request = requests.head(remote_file_path)
url_time = request.headers['last-modified']
url_date = parsedate(url_time)

print('Downloading covid data...')
if os.path.exists(local_file_path):
    file_time = utc.localize(datetime.datetime.fromtimestamp(os.path.getmtime(local_file_path)))
    if url_date > file_time:
        urllib.request.urlretrieve(remote_file_path, local_file_path, report_hook)
    else:
        print('Nothing to download')
        exit()
else:
    urllib.request.urlretrieve(remote_file_path, local_file_path, report_hook)

print()
print('Downloading vaccinations data...')
if os.path.exists(local_file_path_vaccinations):
    file_time = utc.localize(datetime.datetime.fromtimestamp(os.path.getmtime(local_file_path)))
    if url_date > file_time:
        urllib.request.urlretrieve(remote_file_path_vaccinations, local_file_path_vaccinations, report_hook)
    else:
        print('Nothing to download')
        exit()
else:
    urllib.request.urlretrieve(remote_file_path_vaccinations, local_file_path_vaccinations, report_hook)

print('')
print('Converting csv to feather...')
exec(open('./to_feather.py').read())
