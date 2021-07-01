import requests
from bs4 import BeautifulSoup
import sys
import logging

ems_base_url = 'https://items.ems.post/api/publicTracking/track'
logging.basicConfig(level=logging.DEBUG)


class TrackingData:
    def __init__(self, date, message, location=''):
        self.date = date
        self.location = location
        self.message = message


def track(parcel_id):
    params = {'language': 'EN', 'itemId': parcel_id}
    response = requests.get(url=ems_base_url, params=params)
    logging.info(f'EMS response status code is {response.status_code}')
    if response.status_code == 404:
        raise ValueError('error in EMS base url')
    return response.text


def extract(html_data):
    soup = BeautifulSoup(html_data, "html.parser")
    rows = soup.find_all("tr", {'class': 'result-table-row'})
    logging.info(f'EMS response has {len(rows)} entries')
    if not len(rows):
        raise ValueError('parcel not found')
    return rows


def get_status(parcel_id):
    data = track(parcel_id=parcel_id)
    table = extract(data)
    result = []
    for i in table:
        entry = i.text.strip('\n').split('\n')
        result.append(TrackingData(date=entry[0], message=entry[1], location=entry[2]))
    return result


def main():
    data = track(parcel_id=sys.argv[1:])
    table = extract(data)
    for i in table:
        print(i.text)


if __name__ == "__main__":
    main()