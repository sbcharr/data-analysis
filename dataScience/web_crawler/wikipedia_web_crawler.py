import requests
from bs4 import BeautifulSoup 
import urllib
import time


# This is a simple wikipedia crawler and meant for fun
class webCrawler:
    
    def __init__(self, seed_url, target_url="https://en.wikipedia.org/wiki/Philosophy", max_visited=20):
        self.seed_url = seed_url
        self.target_url = target_url
        self.max_visited = max_visited
        
        
    def __continue_crawl(self, search_history, target_url, max_visited):
        """helper function to decide whether to continue crawl or stop crawl
        """
        
        if search_history[-1] == target_url:
            print("Target page is reached; hence quitting...")
            return False
        elif len(search_history) > max_visited:
            print("Length of search has exceeded the max depth of {}; hence quitting...".format(max_visited))
            return False
        elif search_history[-1] in search_history[:-1]:
            print("The page is already viewed earlier; hence quitting...")
            return False
        else:    
            return True     
        
        
    def __find_first_link(self, url):
        """helper function to find the first link to an article inside a wikipedia page
        """
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        content_div = soup.find(id="mw-content-text").find(class_="mw-parser-output")
        
        article_link = None
        
        for element in content_div.find_all("p", recursive=False):
            if element.find("a", recursive=False):
                article_link = element.find("a", recursive=False).get('href')
                break
            
        if not article_link:
            return
        
        first_link = urllib.parse.urljoin("https://en.wikipedia.org/", article_link)
        
        return first_link    
        
        
    def web_crawl(self):
        """web crawling starts here
        """
        article_chain = []
        article_chain.append(self.seed_url)
        i = 0
        
        while self.__continue_crawl(article_chain, self.target_url, self.max_visited): 
            print("visiting site::{}".format(article_chain[-1]))
            # download html of last article in article_chain
            # find the first link in that html
            first_link = self.__find_first_link(article_chain[-1])
            # add the first link to article chain
            article_chain.append(first_link)
            # delay for two seconds, not to make continuous calls to wikipedia
            time.sleep(2)
            i += 1
        return i   
    
 
    
# Example code to use the wikipedia web crawler
if __name__ == "__main__":
    seed = "https://en.wikipedia.org/wiki/Indian_Space_Research_Organisation"
    max_visited = 10
    
    web_crawler = webCrawler(seed, max_visited=max_visited)
    c = web_crawler.web_crawl()
    
    print("total sites visited={}".format(c)) 
    


# TODO: add unit test scripts to test functionality of individual units automatically through assertions