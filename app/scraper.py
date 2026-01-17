from bs4 import BeautifulSoup
import requests

def fetch_website_contents(url):
    print("Fetching content on " + url)
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    title = soup.title.string if soup.title else "No title found"
    if soup.body:
        for irrelevant in soup.body(["script", "style", "img", "input"]):
            irrelevant.decompose()
        text = soup.body.get_text(separator="\n", strip=True)
    else:
        text = ""
    return (title + "\n\n" + text)[:2_000]
    

def fetch_website_link_urls(url):
    print("Scraping the company website for urls...")
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    links = [link.get("href") for link in soup.find_all("a")]
    return [link for link in links if link]