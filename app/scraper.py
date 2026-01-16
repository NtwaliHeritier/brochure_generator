from bs4 import BeautifulSoup
import requests

def fetch_website_link_urls(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    links = [link.get("href") for link in soup.find_all("a")]
    return [link for link in links if link]

fetch_website_link_urls("https://heritier-portfolio.netlify.app")