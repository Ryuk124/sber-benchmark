"""
Парсер текста со страниц для анализа LLM.
Скачивает HTML, чистит от скриптов/стилей и возвращает очищенный текст.
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
import logging

logger = logging.getLogger(__name__)


class PageTextParser:
    """
    Парсер, который:
    - получает список URL
    - скачивает страницы
    - чистит текст от HTML
    - возвращает готовый текст для анализа LLM
    """

    DEFAULT_TIMEOUT = 15
    DEFAULT_HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    def __init__(self, competitor: str, product: str, criterion: str, urls: list):
        self.competitor = competitor
        self.product = product
        self.criterion = criterion
        self.urls = urls

    def fetch_html(self, url: str) -> str:
        """Скачиваем HTML"""
        try:
            resp = requests.get(
                url,
                timeout=self.DEFAULT_TIMEOUT,
                headers=self.DEFAULT_HEADERS,
                verify=True
            )
            resp.raise_for_status()
            return resp.text
        except requests.RequestException as e:
            logger.error(f"Failed to fetch {url}: {e}")
            raise

    def clean_html(self, html: str) -> str:
        """Удаляем скрипты/стили, приводим текст к простому виду"""
        soup = BeautifulSoup(html, 'html.parser')

        # Удаляем скрипты, стили и другой ненужный контент
        for tag in soup(['script', 'style', 'noscript', 'meta', 'link']):
            tag.decompose()

        # Получаем текст с переносами строк
        text = soup.get_text(separator="\n")

        # Удаляем лишние пустые строки
        text = re.sub(r'\n\s*\n', '\n', text)
        
        # Удаляем лишние пробелы в начале и конце каждой строки
        text = '\n'.join(line.strip() for line in text.split('\n') if line.strip())

        return text.strip()

    def run(self) -> list:
        """
        Возвращает список объектов с очищенным текстом для каждой страницы.
        
        Returns:
            list: Список словарей с полями:
                - competitor: название конкурента
                - product: тип продукта
                - criterion: критерий сравнения
                - source_url: URL источника
                - parsed_at: время парсинга
                - cleaned_text: очищенный текст
                - error: (опционально) текст ошибки если произошла
        """
        results = []
        
        for url in self.urls:
            try:
                logger.info(f"Parsing {url}")
                html = self.fetch_html(url)
                cleaned_text = self.clean_html(html)
                
                results.append({
                    "competitor": self.competitor,
                    "product": self.product,
                    "criterion": self.criterion,
                    "source_url": url,
                    "parsed_at": datetime.utcnow().isoformat(),
                    "cleaned_text": cleaned_text,
                    "status": "success"
                })
            except Exception as e:
                logger.error(f"Error parsing {url}: {str(e)}")
                results.append({
                    "competitor": self.competitor,
                    "product": self.product,
                    "criterion": self.criterion,
                    "source_url": url,
                    "parsed_at": datetime.utcnow().isoformat(),
                    "error": str(e),
                    "status": "error"
                })
        
        return results
