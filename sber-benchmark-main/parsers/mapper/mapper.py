from mapping_config import MappingConfig

class AnalysisMapper:
    """
    Генератор задач для анализа, используя конфиг
    """
    def __init__(self, config_path: str = "config.json", competitors=None):
        self.config = MappingConfig(config_path)
        self.competitors = competitors or []

    def get_tasks(self, product: str, criteria: list) -> list:
        """
        Возвращает задачи в формате:
        {
            competitor: str,
            product: str,
            criterion: str,
            urls: list[str],
            generated_at: str
        }
        """
        return self.config.generate_tasks(self.competitors, product, criteria)