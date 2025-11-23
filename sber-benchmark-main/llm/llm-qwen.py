import json
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

MODEL_NAME = "Qwen/Qwen-14B-Chat"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

print(f"Загружаем модель {MODEL_NAME}...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    device_map="auto",
    torch_dtype=torch.float16,
    load_in_4bit=True
)
print("Модель загружена!")

def run_llm(
    competitor: str,
    product: str,
    criterion: str,
    text: str = "",
    mode: str = "facts",
    context: dict = None
) -> dict | str:
    """
    Единая функция для работы с LLM в разных режимах.
    mode = "facts" → извлечение фактов
    mode = "recommendations" → генерация рекомендации на основе value
    """

    if mode == "facts":
        prompt = f"""
Ты аналитик банковских услуг.
Банк: {competitor}
Продукт: {product}
Критерий: {criterion}

Извлеки точное значение по критерию из текста.
Если информации нет — напиши "нет данных".

Верни строго JSON:
{{"competitor": "{competitor}", "product": "{product}", "criterion": "{criterion}", "value": "..."}}

Текст:
\"\"\"{text}\"\"\"
        """

    elif mode == "recommendations":
        if not context or "value" not in context:
            raise ValueError("Для режима 'recommendations' нужен context с ключом 'value'")

        value = context["value"]

        prompt = f"""
Ты эксперт по банковскому маркетингу.

Дано:
Банк: {competitor}
Продукт: {product}
Критерий: {criterion}
Значение: {value}

Правила:
- Если значение > 500 ₽/год → рекомендовать снижение комиссии.
- Если значение = "нет данных" → рекомендовать проверить информацию.
- Если процентная ставка > 15% → предложить улучшение условий.
- Иначе — оставить без изменений.

Выведи краткую рекомендацию на русском языке.
        """

    else:
        raise ValueError(f"Unknown mode: {mode}")

    inputs = tokenizer(prompt, return_tensors="pt").to(DEVICE)
    output_ids = model.generate(**inputs, max_new_tokens=256)
    output = tokenizer.decode(output_ids[0], skip_special_tokens=True)

    if mode == "facts":
        try:
            return json.loads(output)
        except json.JSONDecodeError:
            return {
                "competitor": competitor,
                "product": product,
                "criterion": criterion,
                "value": "FORMAT_ERROR"
            }
    else:
        return output.strip()