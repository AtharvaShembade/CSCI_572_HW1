from bs4 import BeautifulSoup
import time
import requests
from random import randint
from html.parser import HTMLParser
from tqdm import tqdm

USER_AGENT = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'}

class SearchEngine:
    @staticmethod
    def search(query, sleep=True):
        if sleep: 
            time.sleep(randint(2, 20))
        temp_url = '+'.join(query.split())

        url = 'https://www.bing.com/search?q=' + temp_url
        soup = BeautifulSoup(requests.get(url, headers=USER_AGENT).text,"html.parser")
        new_results = SearchEngine.scrape_search_result(soup)
        return new_results
    
    @staticmethod
    def scrape_search_result(soup):
        raw_results = soup.find_all('li', {'class': 'b_algo'})
        results = []
        seen_links = []

        for result in raw_results:
            link_tag = result.find('a')
            if link_tag and 'href' in link_tag.attrs:
                link = link_tag['href']
                
                if link not in seen_links:
                    seen_links.append(link)
                    results.append(link)
                    
                if len(results) == 10:
                    break 
                
        return results
    
if __name__=="__main__":
    import json
    results_dict = {}  # Dictionary to store queries and their results
    with open('100QueriesSet1.txt', 'r') as file:
        for line in tqdm(file):
            query = line.strip()
            if query:  # Ensure the line is not empty
                search_results = SearchEngine.search(query)
                results_dict[query] = search_results  # Store results in the dictionary

    # Write the results dictionary to a JSON file
    with open('hw1.json', 'w') as json_file:
        json.dump(results_dict, json_file, indent=4)
        
    