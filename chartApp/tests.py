from bs4 import BeautifulSoup
import cloudscraper
import os
import json
import requests


class Parser:

    def get_pages(self):

        if not os.path.exists("data"):
            os.mkdir("data")

        scraper = cloudscraper.create_scraper()

        for i in range(1, 5):
            url = f"https://etherscan.io/accounts/{i}"
            html = scraper.get(url)
            with open(f"data/page_{i}.html", "w") as file:
                file.write(html.text)

    def collect_data(self):
        addresses = []
        for page in range(1, 5):
            with open(f"data/page_{page}.html") as file:
                html = file.read()

            soup = BeautifulSoup(html, 'lxml')
            for tr in soup.find_all('tr'):
                tds = tr.find_all('td')
                for td in tds:
                    address_exist = td.findChild('a')
                    if address_exist:
                        addresses.append(address_exist.text)
        result = []
        chunked_addresses = [addresses[i:i + 20] for i in range(0, len(addresses), 20)]
        base_url = "https://api.etherscan.io/api"

        for i in range(0, 5):
            params = {
                'module': 'account',
                'action': 'balancemulti',
                'address': ','.join(chunked_addresses[i]),
                'apikey': '3NEQDF6DPP57PB5QDPNAPPKG9F3VVR1W67'
            }

            r = requests.get(base_url, params=params)
            result.extend(r.json()['result'])

            for sub in result:
                sub['balance'] = int(sub['balance']) * 10 ** (-18)

        with open(f"result.json", "w") as file:
            json.dump(result, file, indent=4, ensure_ascii=False)
