"""
Базовый парсер для сбора данных банков.
Это заготовка для реализации конкретных парсеров.
"""

import logging
import time
from abc import ABC, abstractmethod
from typing import Dict, List, Tuple, Optional
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logger = logging.getLogger(__name__)


class BaseParser(ABC):
    """Базовый класс для всех парсеров"""
    
    DEFAULT_TIMEOUT = 30
    DEFAULT_RETRIES = 3
    USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'

    def __init__(self, timeout: int = None, max_retries: int = None):
        self.timeout = timeout or self.DEFAULT_TIMEOUT
        self.max_retries = max_retries or self.DEFAULT_RETRIES
        self.session = self._create_session()

    def _create_session(self) -> requests.Session:
        """Создаёт сессию с retry стратегией"""
        session = requests.Session()
        
        retry_strategy = Retry(
            total=self.max_retries,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=['HEAD', 'GET', 'OPTIONS']
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        session.headers.update({'User-Agent': self.USER_AGENT})
        
        return session

    def fetch_page(self, url: str) -> Optional[str]:
        """Загружает страницу"""
        try:
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            logger.error(f'Error fetching {url}: {str(e)}')
            return None

    @abstractmethod
    def parse(self, **kwargs) -> Dict[str, any]:
        """
        Парсит данные из источника.
        
        Returns:
            Dict с структурой:
            {
                'bank': 'sber',
                'criteria': {
                    'cost': {'value': True, 'confidence': 0.9, 'source_url': '...'},
                    'sms': {'value': False, 'confidence': 0.8, 'source_url': '...'},
                }
            }
        """
        pass

    def close(self):
        """Закрывает сессию"""
        self.session.close()


class MockParser(BaseParser):
    """Mock парсер для тестирования"""
    
    def parse(self, bank: str = 'sber', **kwargs) -> Dict[str, any]:
        """Возвращает mock-данные"""
        import random
        
        criteria_list = [
            'cost', 'sms', 'withdrawal', 'transfers', 'interest',
            'limit', 'rate', 'payment', 'loyalty', 'cashback'
        ]
        
        criteria = {}
        for crit_id in criteria_list:
            criteria[crit_id] = {
                'value': random.choice([True, False]),
                'confidence': round(random.uniform(0.6, 1.0), 2),
                'source_url': 'https://example.com',
            }
        
        return {
            'bank': bank,
            'criteria': criteria,
        }


class BankiRuParser(BaseParser):
    """
    Парсер для banki.ru
    TODO: Реализовать логику парсинга
    """
    
    BASE_URL = 'https://banki.ru'
    
    def parse(self, product: str = 'deposits', **kwargs) -> Dict[str, any]:
        """
        Парсит banki.ru для конкретного продукта.
        TODO: Реализовать
        """
        logger.info(f'BankiRuParser: parsing {product}')
        # Здесь должна быть логика парсинга
        raise NotImplementedError('BankiRuParser.parse() - to be implemented')


class SravniRuParser(BaseParser):
    """
    Парсер для sravni.ru
    TODO: Реализовать логику парсинга
    """
    
    BASE_URL = 'https://sravni.ru'
    
    def parse(self, product: str = 'credits', **kwargs) -> Dict[str, any]:
        """
        Парсит sravni.ru для конкретного продукта.
        TODO: Реализовать
        """
        logger.info(f'SravniRuParser: parsing {product}')
        # Здесь должна быть логика парсинга
        raise NotImplementedError('SravniRuParser.parse() - to be implemented')


class RBKParser(BaseParser):
    """
    Парсер для rbc.ru/quotes
    TODO: Реализовать логику парсинга
    """
    
    BASE_URL = 'https://www.rbc.ru/quotes'
    
    def parse(self, **kwargs) -> Dict[str, any]:
        """
        Парсит RBC для банковских данных.
        TODO: Реализовать
        """
        logger.info('RBKParser: parsing')
        # Здесь должна быть логика парсинга
        raise NotImplementedError('RBKParser.parse() - to be implemented')


class OfficialBankParser(BaseParser):
    """
    Парсер для официальных сайтов банков (sber.ru, vtb.ru и т.д.)
    TODO: Реализовать логику парсинга
    """
    
    def parse(self, bank: str, product: str = 'deposits', **kwargs) -> Dict[str, any]:
        """
        Парсит официальный сайт банка.
        TODO: Реализовать
        """
        logger.info(f'OfficialBankParser: parsing {bank} - {product}')
        # Здесь должна быть логика парсинга
        raise NotImplementedError('OfficialBankParser.parse() - to be implemented')
