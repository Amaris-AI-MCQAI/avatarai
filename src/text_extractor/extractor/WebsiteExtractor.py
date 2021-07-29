from ..constants import EXTRACTOR_MODE_WEB
from .Extractor import Extractor
from newspaper import Article
import re

RESPONSE: str

class WebsiteExtractor(Extractor):
    def __init__(self):
        self.mode = EXTRACTOR_MODE_WEB
    
    def read_input(self, filepath):
        article = Article(filepath, language='en')
        article.download()
        article.parse()
        article.nlp()
        print("authors", article.authors)
        print("publish_date: ", article.publish_date)
        print("text: ", article.text)
        print("image link: ", article.images)
        print("Video :", article.movies)
        print("title: ", article.title)
        print(self.get_token_list(self.process_raw_text(article.text)))
        return self.process_raw_text(article.text)

    def process_raw_text(self, text):
        # Remove citation
        text = re.sub(r'\[[a-zA-Z0-9]+\]', '', text)
        return text
    
    def get_token_list(self, text):
        text_list = text.split("\n")
        return [i for i in text_list if len(i) > 30]



    # def read_input(self, filepath):
    #     global RESPONSE
    #     MySpider.start_urls = [filepath]
    #     process = CrawlerProcess()
    #     process.crawl(MySpider)
    #     process.start()
    #     return str(self.process_raw_response_body(RESPONSE))
    
    # def process_raw_response_body(self, response):
    #     soup = BeautifulSoup(response.body, 'html.parser')
    #     soup.p.i.unwrap()
    #     return soup.find_all('p')

    

