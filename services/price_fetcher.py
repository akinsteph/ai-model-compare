import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import re

class PriceFetcher:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
    def clean_text(self, text):
        return re.sub(r'\s+', ' ', text).strip()

    def fetch_openai_pricing(self):
        try:
            response = requests.get('https://openai.com/pricing', headers=self.headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            pricing_data = {
                'gpt4': {'input': None, 'output': None},
                'gpt35': {'input': None, 'output': None}
            }
            
            # Find pricing tables
            pricing_tables = soup.find_all('table')
            for table in pricing_tables:
                rows = table.find_all('tr')
                for row in rows:
                    cells = row.find_all(['td', 'th'])
                    if len(cells) >= 2:
                        text = self.clean_text(cells[0].get_text().lower())
                        if 'gpt-4' in text:
                            pricing_data['gpt4']['input'] = self.clean_text(cells[1].get_text())
                        elif 'gpt-3.5' in text:
                            pricing_data['gpt35']['input'] = self.clean_text(cells[1].get_text())
            
            return pricing_data
        except Exception as e:
            print(f"Error fetching OpenAI pricing: {e}")
            return None

    def fetch_anthropic_pricing(self):
        try:
            response = requests.get('https://www.anthropic.com/pricing', headers=self.headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            pricing_data = {
                'claude2': {'input': None, 'output': None}
            }
            
            # Find pricing information
            pricing_elements = soup.find_all(['div', 'p'], string=re.compile(r'\$.*per.*tokens?', re.I))
            for element in pricing_elements:
                text = self.clean_text(element.get_text().lower())
                if 'input' in text:
                    pricing_data['claude2']['input'] = text
                elif 'output' in text:
                    pricing_data['claude2']['output'] = text
            
            return pricing_data
        except Exception as e:
            print(f"Error fetching Anthropic pricing: {e}")
            return None

    def fetch_google_palm_pricing(self):
        try:
            response = requests.get('https://cloud.google.com/vertex-ai/pricing', headers=self.headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            pricing_data = {
                'palm2': {'input': None, 'output': None}
            }
            
            # Find pricing tables
            pricing_tables = soup.find_all('table')
            for table in pricing_tables:
                if 'PaLM' in table.get_text() or 'Language Model' in table.get_text():
                    rows = table.find_all('tr')
                    for row in rows:
                        cells = row.find_all(['td', 'th'])
                        if len(cells) >= 2:
                            text = self.clean_text(cells[0].get_text().lower())
                            if 'input' in text:
                                pricing_data['palm2']['input'] = self.clean_text(cells[1].get_text())
                            elif 'output' in text:
                                pricing_data['palm2']['output'] = self.clean_text(cells[1].get_text())
            
            return pricing_data
        except Exception as e:
            print(f"Error fetching Google pricing: {e}")
            return None

    def fetch_all_pricing(self):
        pricing_data = {
            'last_updated': datetime.now().isoformat(),
            'providers': {
                'openai': self.fetch_openai_pricing(),
                'anthropic': self.fetch_anthropic_pricing(),
                'google': self.fetch_google_palm_pricing()
            }
        }
        return pricing_data

    def save_pricing(self, pricing_data):
        with open('data/current_pricing.json', 'w') as f:
            json.dump(pricing_data, f, indent=4)
