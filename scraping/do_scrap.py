import os
from datetime import datetime, timedelta
import pytz
import json

from src.scraper.data_collection import DataCollector

test_DATE = '2024-04-29T00:00:00.000+0000'

current_date = datetime.now()
current_date = current_date.astimezone(pytz.UTC)
print(current_date.date())

LAST_UPDATE = datetime.strptime(test_DATE, "%Y-%m-%dT%H:%M:%S.%f%z")
LAST_UPDATE = LAST_UPDATE.astimezone(pytz.UTC)
print(LAST_UPDATE)

# if LAST_UPDATE < current_date:
#     print('LAST_UPDATE < current_date')


MAX_PAGES = 1


def load_json(json_file):
    if os.path.exists(json_file):
        with open(json_file, 'r') as f:
            json_data = json.load(f)
            if json_data:
                return json_data
    else:
        save_json({}, json_file)
    return {}


def save_json(json_data, json_file):
    with open(json_file, 'w') as f:
        json.dump(json_data, f)


def update_json(json_data, json_file):
    if os.path.exists(json_file):
        with open(json_file, 'r') as f:
            json_data = json.load(f)
            if json_data:
                json_data.update(json_data)
            save_json(json_data, json_file)


def scrape():
    data_collector = DataCollector(LAST_UPDATE)

    PAGE = 1
    TEMP_DATE = datetime.now()
    TEMP_DATE = TEMP_DATE.astimezone(pytz.UTC)

    NEWEST_DATE = LAST_UPDATE
    NEWEST_DATE = NEWEST_DATE.astimezone(pytz.UTC)

    while (LAST_UPDATE < TEMP_DATE) and (PAGE <= MAX_PAGES):
        property_urls = data_collector.get_property_links(page=PAGE)
        print(f"PAGE: {PAGE} - properties: {len(property_urls)}")

        for link in property_urls:
            print(TEMP_DATE)
            if LAST_UPDATE < TEMP_DATE:
                property_data = data_collector.get_data_from_html(link)

                # Actializar la BD, si la propiedad existe, actializarla, si no, insertarla
                print(property_data)

                TEMP_DATE = datetime.strptime(property_data['data']['publication']['lastModificationDate'],
                                              "%Y-%m-%dT%H:%M:%S.%f%z")
                TEMP_DATE = TEMP_DATE.astimezone(pytz.UTC)

                NEWEST_DATE = TEMP_DATE if NEWEST_DATE < TEMP_DATE else NEWEST_DATE

        PAGE += 1

    return NEWEST_DATE


LAST_UPDATE = scrape()

print(f"LAST_UPDATE: {LAST_UPDATE}")
