import json
from datetime import datetime
from typing import List, Dict

class MappingConfig:
    """
    Класс конфигурации для парсинга банковских продуктов.
    Загружает структуры из уже существующего config.json.
    """

    def __init__(self, config_path: str = "config.json"):
        self.config_path = config_path

        self.load()

    def load(self):
        """Загрузить конфигурацию из config.json (если нет — бросить исключение)"""
        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Конфигурационный файл '{self.config_path}' не найден. "
                                    f"Создайте его перед запуском.")

        self.bank_mapping: Dict[str, List[str]] = data.get("bank_mapping", {})
        self.product_mapping: Dict[str, List[str]] = data.get("product_mapping", {})
        self.criteria_mapping: Dict[str, List[str]] = data.get("criteria_mapping", {})

    def get_bank_links(self, bank: str) -> List[str]:
        return self.bank_mapping.get(bank, [])

    def get_product_links(self, product: str) -> List[str]:
        return self.product_mapping.get(product, [])

    def get_criteria_links(self, criterion: str) -> List[str]:
        return self.criteria_mapping.get(criterion, [])

    def get_combined_links(self, banks: List[str], product: str, criteria: List[str]) -> List[str]:
        """
        Объединяет ссылки из bank_mapping, product_mapping и criteria_mapping
        """
        combined_links = []
        for bank in banks:
            combined_links.extend(self.get_bank_links(bank))

        combined_links.extend(self.get_product_links(product))

        for crit in criteria:
            combined_links.extend(self.get_criteria_links(crit))

        return list(set(combined_links))

    def generate_tasks(self, banks: List[str], product: str, criteria: List[str]) -> List[dict]:
        tasks = []
        for crit in criteria:
            crit_links = self.get_criteria_links(crit)
            product_links = self.get_product_links(product)
            for bank in banks:
                bank_links = self.get_bank_links(bank)
                combined = set(bank_links) | set(product_links) | set(crit_links)
                if combined:
                    tasks.append({
                        "competitor": bank,
                        "product": product,
                        "criterion": crit,
                        "urls": list(combined),
                        "generated_at": datetime.utcnow().isoformat()
                    })
        return tasks