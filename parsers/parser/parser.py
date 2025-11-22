import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re

class PageTextParser:
    """
    Парсер, который:
    - получает список URL
    - скачивает страницы
    - чистит текст от HTML
    - возвращает готовый текст для анализа LLM
    """
    def __init__(self, competitor: str, product: str, criterion: str, urls: list):
        self.competitor = competitor
        self.product = product
        self.criterion = criterion  # пока просто метаданные, LLM их может использовать
        self.urls = urls

    def fetch_html(self, url: str) -> str:
        """Скачиваем HTML"""
        resp = requests.get(url, timeout=15, headers={"User-Agent": "Mozilla/5.0"})
        resp.raise_for_status()
        return resp.text
    
    def clean_html(self, html: str) -> str:
        """Удаляем скрипты/стили, приводим текст к простому виду"""
        soup = BeautifulSoup(html, 'html.parser')

        for tag in soup(['script', 'style', 'noscript']):
            tag.decompose()

        text = soup.get_text(separator="\n")

        text = re.sub(r'\n\s*\n', '\n', text)

        return text.strip()

    def run(self) -> list:
        """
        Возвращает список объектов с очищенным текстом для каждой страницы
        """
        results = []
        for url in self.urls:
            try:
                html = self.fetch_html(url)
                cleaned_text = self.clean_html(html)
                results.append({
                    "competitor": self.competitor,
                    "product": self.product,
                    "criterion": self.criterion,
                    "source_url": url,
                    "parsed_at": datetime.utcnow().isoformat(),
                    "cleaned_text": cleaned_text
                })
            except Exception as e:
                results.append({
                    "competitor": self.competitor,
                    "product": self.product,
                    "criterion": self.criterion,
                    "source_url": url,
                    "parsed_at": datetime.utcnow().isoformat(),
                    "error": str(e)
                })
        return results