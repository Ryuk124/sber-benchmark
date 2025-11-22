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

def analyze_with_llm(text: str, competitor: str, product: str, criterion: str) -> dict:
    """
    Обрабатывает текст страницы через Qwen-14B-Chat и возвращает структурированный JSON.
    """

    prompt = f"""
Ты аналитик банковских услуг.
Банк: {competitor}
Продукт: {product}
Критерий: {criterion}

Извлеки точное значение по критерию из текста.
Если информации нет — напиши "нет данных".

Верни строго JSON в формате (больше ничего писать не нужно):
{{"competitor": "{competitor}", "product": "{product}", "criterion": "{criterion}", "value": "..."}}

Текст:
\"\"\"{text}\"\"\"
    """
    inputs = tokenizer(prompt, return_tensors="pt").to(DEVICE)
    output_ids = model.generate(**inputs, max_new_tokens=256)
    output = tokenizer.decode(output_ids[0], skip_special_tokens=True)

    try:
        return json.loads(output)
    except json.JSONDecodeError:
        return {
            "competitor": competitor,
            "product": product,
            "criterion": criterion,
            "value": "FORMAT_ERROR"
        }