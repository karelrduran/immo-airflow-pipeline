import os
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures
import json
import re
from typing import Dict, Optional

from bs4 import BeautifulSoup
from .data_manipulation import DataManipulation
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class DataCollector:
    """
    A class to collect data from Immoweb website.

    Attributes:
    session (Session): A session object for making HTTP requests.
    """

    def __init__(self, last_update: str):
        """
        Initializes DataCollector with a session object.
        """
        self.LAST_UPDATE = last_update

        self.driver = webdriver.Chrome()
        options = Options()
        # options.add_argument('--headless')
        options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(options=options)

    def __del__(self):
        self.driver.quit()

    def get_links_from_page(self, page):
        """
        Retrieves property links from a given page.

        Args:
        page (int): The page number to retrieve links from.

        Returns:
        list: A list of property URLs.
        """
        # self.page = page
        base_url = "https://www.immoweb.be/en/search/house-and-apartment/for-sale"
        search_url = f"{base_url}?countries=BE&page={page}&orderBy=newest"

        self.driver.get(search_url)
        html_content = self.driver.page_source

        soup = BeautifulSoup(html_content, "html.parser")
        property_links = soup.find_all("a", class_="card__title-link")

        return [link["href"] for link in property_links if "href" in link.attrs]

    # This function retrieves the URLs of the properties listed on the Immoweb search results page
    # It now uses concurrent requests to speed up the process
    def get_property_links(self, page):
        """
        Retrieves property links from multiple pages concurrently.

        Args:
        pages (int): The number of pages to retrieve links from.

        Returns:
        list: A list of property URLs.
        """
        # self.pages = pages
        all_urls = []
        with ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(self.get_links_from_page, page)
                # for page in range(1, pages + 1)
            ]
            for future in concurrent.futures.as_completed(futures):
                all_urls.extend(future.result())
        return all_urls

    def get_data_from_html(self, url: str) -> Optional[Dict]:
        """
        Retrieves data from HTML content.

        Args:
        html (str): The HTML content to extract data from.

        Returns:
        dict: Extracted data in JSON format.
        """

        try:
            self.driver.get(url)
            html_content = self.driver.page_source

            regex = (
                r"(<script type=\"text/javascript\">\n\s+window\.classified = )(.*)"
            )
            match = re.search(regex, html_content)

            # print(match.group(2)[:-1])
            # print(json.loads(match.group(2)[:-1]))

            result = json.loads(match.group(2)[:-1])

            data = {
                'id': result['id'],
                'property': result['property']['type'],
                'creationDate': result['publication']['creationDate'],
                'expirationDate': result['publication']['expirationDate'],
                'lastModificationDate': result['publication']['lastModificationDate'],
                'data': result
            }
            return data

        except Exception as e:
            return None































    def check_existant(self, id: str):
        """
        Checks if a property ID exists in the data.

        Args:
        id (str): The ID to check.

        Returns:
        bool: True if the ID exists, False otherwise.
        """
        with open(os.path.join("data", "data.json"), "r", encoding="utf-8") as file:
            if str(id) in file.read():
                return True
        return False

    def estate_check(self, data: dict):
        """
        Checks if the property is a new real estate project or not.

        Args:
        data (dict): The data of the property.

        """

        # self.data = data
        cluster = data.get("cluster")
        if cluster is None:
            # if self.check_existant(data.get("id")) == False:
            DataManipulation().get_data(data)
        else:
            unitlist = []
            units = data.get("cluster").get("units")[0].get("items")
            for item in units:
                salestatus = DataManipulation().safeget(item, ["saleStatus"])
                if salestatus == "AVAILABLE":
                    locality = DataManipulation().safeget(
                        data, ["cluster", "units", "items", "locality"], default=None
                    )
                    postalcode = DataManipulation().safeget(
                        data, ["property", "location", "postalCode"], default=None
                    )
                    id = item.get("id")
                    housetype = DataManipulation().safeget(
                        item, ["subtype"], default=None
                    )
                    baseurl = f"https://www.immoweb.be/en/classified/{housetype}/for-sale/{locality}/{postalcode}/{id}"
                    unitlist.append(baseurl)
            for unit in unitlist:
                rawdata = self.get_data_from_html(unit)
                if self.check_existant(rawdata.get("id")) == False:
                    DataManipulation().get_data(rawdata)
