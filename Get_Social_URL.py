import requests
from bs4 import BeautifulSoup
import re
import phonenumbers

def extract_and_validate_phone_numbers(text):
    phone_numbers = []

    for match in phonenumbers.PhoneNumberMatcher(text, "ANY"):
        parsed_number = phonenumbers.parse(match.raw_string, None)
        if phonenumbers.is_valid_number(parsed_number):
            formatted_number = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)
            phone_numbers.append(formatted_number)

    return phone_numbers

def scrape_website(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        social_links = []
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            if re.search(r'(facebook\.com|linkedin\.com|twitter\.com|instagram\.com)', href):
                social_links.append(href)

        email = None
        email_tag = soup.find('a', href=lambda href: href and 'mailto:' in href)
        if email_tag:
            email = email_tag['href'][7:]  # Removing 'mailto:' from the href

        contact = None
        contact_tag = soup.find('p', string=lambda s: s and ('contact' in s.lower() or 'phone' in s.lower()))
        if contact_tag:
            contact = contact_tag.get_text()
            contact_numbers = extract_and_validate_phone_numbers(contact)
        
        # Add the specific contact pattern you provided
        specific_contact_pattern = re.search(r'\+\d{1} \d{3} \d{3} \d{4}', contact)
        if specific_contact_pattern:
            contact_numbers.append(specific_contact_pattern.group(0))

        return {
            "social_links": social_links,
            "email": email,
            "contact": contact_numbers
        }
    else:
        print("Failed to retrieve the website content.")
        return None

if __name__ == "__main__":
    user_input = input("Enter the website URL: ")
    scraped_data = scrape_website(user_input)
    if scraped_data:
        print("Social links -")
        for link in scraped_data["social_links"]:
            print(link)
        print("Email:", scraped_data["email"])
        if scraped_data["contact"]:
            print("Contact:")
            for number in scraped_data["contact"]:
                print(number)
