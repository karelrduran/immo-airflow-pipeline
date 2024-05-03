from datetime import datetime
import pytz

# from src.scraper.data_collection import DataCollector
from .src.scraper.data_collection import DataCollector

from ..database.src.database_manipulation import DBManipulation

from ..settings.settings_manipulation import SettingsManipulation


def scrape():
    sett_dm = SettingsManipulation()
    SETTINGS = sett_dm.load_json()

    LAST_UPDATE = datetime.strptime(SETTINGS['LAST_UPDATE'], "%Y-%m-%dT%H:%M:%S.%f%z")
    MAX_PAGES = SETTINGS['MAX_PAGES']

    data_collector = DataCollector(LAST_UPDATE)

    PAGE = 1
    TEMP_DATE = datetime.now()
    TEMP_DATE = TEMP_DATE.astimezone(pytz.UTC)

    NEWEST_DATE = LAST_UPDATE
    NEWEST_DATE = NEWEST_DATE.astimezone(pytz.UTC)

    while (LAST_UPDATE < TEMP_DATE) and (PAGE <= MAX_PAGES):
        property_urls = data_collector.get_property_links(page=PAGE)
        # print(f"PAGE: {PAGE} - properties: {len(property_urls)}")

        dbm = DBManipulation(
            dbname=SETTINGS['POSTGRES_DB_CONNECTION']['dbname'],
            user=SETTINGS['POSTGRES_DB_CONNECTION']['user'],
            password=SETTINGS['POSTGRES_DB_CONNECTION']['password'],
            host=SETTINGS['POSTGRES_DB_CONNECTION']['host'],
            tbname=SETTINGS['POSTGRES_DB_CONNECTION']['tbname']
        )

        for link in property_urls:
            if LAST_UPDATE < TEMP_DATE:
                property_data = data_collector.get_data_from_html(link)

                query_result = dbm.select_property_by_id(id=property_data['id'])
                if query_result[0]:
                    dbm.update(property_data['id'], property_data)
                else:
                    dbm.insert(property_data['id'], property_data)

                TEMP_DATE = datetime.strptime(property_data['data']['publication']['lastModificationDate'],
                                              "%Y-%m-%dT%H:%M:%S.%f%z")
                TEMP_DATE = TEMP_DATE.astimezone(pytz.UTC)

                NEWEST_DATE = TEMP_DATE if NEWEST_DATE < TEMP_DATE else NEWEST_DATE

        PAGE += 1

    # NEWEST_DATE = datetime.strptime(NEWEST_DATE, "%Y-%m-%dT%H:%M:%S.%f%z")
    sett_dm.update_last_date(last_date=NEWEST_DATE)

    # return NEWEST_DATE


# LAST_UPDATE = scrape()
#
# print(f"LAST_UPDATE: {LAST_UPDATE}")


# {
#   "POSTGRES_DB_CONNECTION":{
#     "dbname": "properties_raw_data",
#     "user": "karel",
#     "password": "karel123",
#     "host": "localhost",
#     "tbname": "property"
#   },
#   "LAST_UPDATE": "2024-04-29T13:00:07.270+0000",
#   "MAX_PAGES": 1
# }

scrape()
