import string
import os
import requests
from bs4 import BeautifulSoup


class WebScraper:
    """WebScraper object that takes two input, number of pages to look and the article type"""
    def __init__(self):
        self.pageNumber = int(input())
        self.articlesType = input()

    def main(self):
        """Grab the pages requested and create a folder for each page to store the body of the article as text files"""
        for page in range(1, self.pageNumber + 1):
            try:
                os.mkdir(os.getcwd() + f"/Page_{str(page)}")
            except FileExistsError:
                pass
            page_path = os.getcwd() + f"/Page_{str(page)}"  # use the path of the directory created to write file to
            url = f"https://www.nature.com/nature/articles?searchType=journalSearch&sort=PubDate&page={str(page)}"
            req = requests.get(url, headers={'Accept-Language': 'en-US,en;q=0.5'})
            soup = BeautifulSoup(req.content, 'html.parser')
            articles = soup.find_all('article', {"class": "u-full-height c-card c-card--flush"})  # look for article
            for article in articles:  # for each article found, search the meta type to  get requested article type
                article_type = article.find('span', class_="c-meta__type")
                body_url = "https://www.nature.com"
                if article_type.string == self.articlesType:
                    if article_type.string == "Research Highlight":
                        # Note: Research Highlight article types has a different name for class containing body
                        link = article.a.get('href')  # grabs the article link to concatenate with base url
                        full_url = body_url + link
                        body_req = requests.get(full_url, headers={'Accept-Language': 'en-US,en;q=0.5'})

                        # user another soup instance to parse body
                        body_soup = BeautifulSoup(body_req.content, 'html.parser')

                        # find the article body following the redirected url, different class than other article types
                        body = body_soup.find("div", "article-item__body").text.strip()

                        # find the heading to create the article name for the text file containing body
                        heading = article.find('a').text.strip()

                        # remove any punctuation and replacing any spaces between article name with _
                        article_name = heading.translate(heading.maketrans('', '', string.punctuation)).replace(" ",
                                                                                                                "_")

                        # write text file to the page path of the directory created, in binary UTF-8
                        with open(os.path.join(page_path, "{}.txt".format(article_name)), "wb") as outfile:
                            outfile.write(body.encode())
                    else:
                        # for all other article types
                        link = article.a.get('href')
                        full_url = body_url + link
                        body_req = requests.get(full_url, headers={'Accept-Language': 'en-US,en;q=0.5'})
                        body_soup = BeautifulSoup(body_req.content, 'html.parser')
                        body = body_soup.find("div", "c-article-body").text.strip()
                        heading = article.find('a').text.strip()
                        article_name = heading.translate(heading.maketrans('', '', string.punctuation)).replace(" ",
                                                                                                                "_")
                        with open(os.path.join(page_path, "{}.txt".format(article_name)), "wb") as outfile:
                            outfile.write(body.encode())


if __name__ == "__main__":
    ws = WebScraper()
    ws.main()

