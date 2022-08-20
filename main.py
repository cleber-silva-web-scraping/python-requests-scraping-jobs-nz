import requests
from bs4 import BeautifulSoup

class Crawler:
    
    def __init__(self):
        self.url = 'https://jobs.govt.nz/jobtools/jncustomsearch.searchAction'
        self.per_page = 160

    def _get(self, url):
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        return soup

    def _table(self, soup):
        trs = soup.find('table').find_all('tr')
        print('- - - - - - - - - - - - -')
        for tr in trs:
            td = tr.find_all('td')
            print('{} {}'.format(td[0].text, td[1].text))
        print('')
    
    def _post(self, page = 0):
        print('\nGet page {} - Record {}'.format(page/self.per_page, page/self.per_page * self.per_page + 1))
        data = {
            'in_organid': '16563',
            'in_jobDate': 'All',
            'in_summary': 'S',
            'in_totalrows' : '2999',
            'in_nav': 'next_set',
            'in_prevpg': '20',
            'in_pg': page
        }
        r = requests.post(self.url, data = data)
        soup = BeautifulSoup(r.text, 'html.parser')
        table = soup.find('table')
        links = table.find_all('a')

        for link in links:
            href = 'https://jobs.govt.nz/jobtools/{}'.format(link['href'])
            body = self._get(href)
            self._table(body)

        if len(links) > 0:
            self._post(page + self.per_page)


crawler = Crawler()
crawler._post()
