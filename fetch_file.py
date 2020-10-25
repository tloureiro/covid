import requests
import os
import datetime
from dateutil.parser import parse as parsedate
import pytz
import urllib.request


local_file_path = './data/main.csv'
remote_file_path = 'https://storage.googleapis.com/covid19-open-data/v2/main.csv'
utc = pytz.UTC

request = requests.head(remote_file_path)
url_time = request.headers['last-modified']
url_date = parsedate(url_time)

if os.path.exists(local_file_path):
    file_time = utc.localize(datetime.datetime.fromtimestamp(os.path.getmtime(local_file_path)))
    if url_date > file_time:
        urllib.request.urlretrieve(remote_file_path, local_file_path)
    else:
        print('Nothing to download')
        exit()
else:
    urllib.request.urlretrieve(remote_file_path, local_file_path)

exec(open('./to_feather.py').read())




