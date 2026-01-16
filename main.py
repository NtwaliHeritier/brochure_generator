from app.scraper import filter_company_urls
import json

def main():
    url_input = input("Enter company website url: ")
    urls = filter_company_urls(url_input)
    print(json.loads(urls))


if __name__ == "__main__":
    main()
