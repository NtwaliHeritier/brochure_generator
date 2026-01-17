from app.llm_generator import generate_brochure
import json

def main():
    company_name = input("Enter company name: ")
    company_url = input("Enter company website url: ")
    print(generate_brochure(company_name, company_url))

if __name__ == "__main__":
    main()
