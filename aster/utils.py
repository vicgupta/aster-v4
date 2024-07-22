def create_prompt(role: str, content: str):
    args = {"role": role, "content": content}
    return {**args}

# pip install requests beautifulsoup4
from bs4 import BeautifulSoup
import requests
def get_text_from_url(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text()
        return text
    except Exception as e:
        print("An error occurred:", e)
        return None
