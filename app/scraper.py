from bs4 import BeautifulSoup
import requests
from openai import OpenAI
import json

MODEL_NAME = "llama3.2"
BASE_URL = "http://localhost:11434/v1"

def generate_brochure(company_name, url):
    urls = filter_company_urls(url)

    brochure_system_prompt = """
    You are an assistant that analyzes content from relevant pages of a company website and produces a concise, professional brochure for prospective customers, investors, and job candidates.

    Write the response in Markdown.
    Do not use code blocks.
    Organize the brochure with clear headings and short paragraphs.

    Include information about the company’s purpose, products or services, customers, culture, and careers/jobs when such information is available.
    If certain details are not present in the source material, omit them rather than making assumptions.
    """

    user_prompt = f"""
    You are looking at a company called: {company_name}
    Here are the contents of its landing page and other relevant pages;
    use this information to build a short brochure of the company in markdown without code blocks.\n\n
    """

    for link in urls["links"]:
        user_prompt += f"\n\n### Link: {link['type']}\n"
        user_prompt += fetch_website_contents(link["url"])
    
    print("Generating a brochure...")
    ollama = use_llm()
    messages = [
        {"role": "system", "content": brochure_system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    response = ollama.chat.completions.create(model="llama3.2", messages=messages)
    return response.choices[0].message.content


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

    print("Fetching relevant links...")
    ollama = use_llm()
    response = ollama.chat.completions.create(model="llama3.2", messages=messages, response_format={"type": "json_object"})
    return json.loads(response.choices[0].message.content)

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

def use_llm():
    return OpenAI(base_url=BASE_URL, api_key="ollama")