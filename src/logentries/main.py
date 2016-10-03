import sys
import time
import json
from os import path

import requests
from colorama import Fore

home = path.expanduser("~")
with open(path.join(home, '.logentries')) as conf:
    json_conf = json.load(conf)

API_KEY = json_conf['API_KEY']
LOG_DICT = json_conf['LOG_DICT']

TO = int(time.time())*1000
FROM = TO - 10*60000
QUERY = sys.argv[2]
LOG_ID = LOG_DICT[sys.argv[1]]


def continue_request(req):
    if 'links' in req.json():
        continue_url = req.json()['links'][0]['href']
        new_response = make_request(continue_url)
        handle_response(new_response)


def print_resp(resp):
    json_resp = resp.json()
    if 'events' in json_resp:
        for event in json_resp['events']:
            print(event['message'].replace(QUERY, Fore.RED+QUERY+Fore.RESET))
    if 'links' in json_resp:
        input('Press ENTER for more logs: ')
        continue_request(resp)


def handle_response(resp):
    response = resp
    if response.status_code == 200:
        print_resp(resp)
        return
    if response.status_code == 202:
        continue_request(resp)
        return
    if response.status_code > 202:
        print('Error status code ' + str(response.status_code))
        return


def make_request(provided_url=None):
    headers = {'x-api-key': API_KEY}

    url = "https://rest.logentries.com/query/logs/"+LOG_ID+"/?query=where("+QUERY+")&from="+str(FROM)+"&to="+str(TO)
    if provided_url:
        url = provided_url
    req = requests.get(url, headers=headers)
    return req


def print_query():
    req = make_request()
    handle_response(req)


def start():
    print_query()


if __name__ == '__main__':
    start()
