from bs4 import BeautifulSoup
import requests
from openai import OpenAI

MODEL_NAME = "llama3.2"
BASE_URL = "http://localhost:11434/v1"

def filter_company_urls(url):
    system_prompt = """
    You are provided with a list of links found on a webpage.
    You are able to decide which of the links would be most relevant to include in a brochure about the company,
    such as links to an About page, or a Company page, or Careers/Jobs pages.
    You should respond in JSON as in this example:

    {
        "links": [
            {"type": "<page type>", "url": "<full https URL>"}
        ]
    }
    """

    user_prompt = """
    Here is a list of links found on the website {url}.

    Please decide which of these links are relevant for inclusion in a brochure about the company.
    Respond with the full HTTPS URLs in JSON format.

    Do not include links related to Terms of Service, Privacy Policies, or email (mailto:) links.

    Some of the links may be relative paths.

    Links: (some might be relative links):
    """

    links = fetch_website_link_urls(url)
    user_prompt += "\n".join(links)

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

    ollama = OpenAI(base_url=BASE_URL, api_key="ollama")
    response = ollama.chat.completions.create(model="llama3.2", messages=messages, response_format={"type": "json_object"})
    return response.choices[0].message.content

def fetch_website_link_urls(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    links = [link.get("href") for link in soup.find_all("a")]
    return [link for link in links if link]