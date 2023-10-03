import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup

class Crawler:
    def __init__(self, url, max_depth=5):
        self.visited_urls = []
        self.urls_to_visit = [(url, 0)]
        self.max_depth = max_depth

    def download_url(self, url):
        response = requests.get(url)
        response.raise_for_status()  
        return response.text

    def get_linked_urls(self, url, html):
        soup = BeautifulSoup(html, 'html.parser')
        for link in soup.find_all('a'):
            path = link.get('href')
            if path and path.startswith('/'):
                path = urljoin(url, path)
            yield path

    def add_url_to_visit(self, url, depth):
        if url not in self.visited_urls and (url, depth) not in self.urls_to_visit and depth <= self.max_depth:
            self.urls_to_visit.append((url, depth))

    def crawl(self, url, depth):
        html = self.download_url(url)
        for linked_url in self.get_linked_urls(url, html):
            self.add_url_to_visit(linked_url, depth + 1)

    def run(self):
        while self.urls_to_visit:
            url, depth = self.urls_to_visit.pop(0)
            print(f'Crawling: {url} (Depth: {depth})')
            try:
                self.crawl(url, depth)
            except requests.exceptions.RequestException as e:
                print(f'Failed to crawl: {url} - {e}')
            except KeyboardInterrupt:
                print('\n'f'[!] Keyboard Interrupt!')
                break
            except Exception as e:
                print(f'Failed to crawl: {url} - {e}')
            finally:
                self.visited_urls.append(url)


if __name__ == '__main__':
    url = input(f"URL: ")
    max_depth = int(input(f"Max Depth: "))
    crawler = Crawler(url, max_depth=max_depth)
    crawler.run()
