import json

# Пример ответа от модели (можно заменить на реальный)
model_response = '''
[
  {"id": 1, "sentiment": "positive", "reason": "Хороший сервис"},
  {"id": 2, "sentiment": "negative", "reason": "Плохая доставка"}
]
'''

def validate_response(response_text):
    try:
        data = json.loads(response_text)
        if not isinstance(data, list):
            return "Ошибка: ответ должен быть массивом JSON"
        
        for item in data:
            if "id" not in item or "sentiment" not in item or "reason" not in item:
                return f"Ошибка: в объекте {item} не хватает полей"
            if item["sentiment"] not in ["positive", "negative", "neutral"]:
                return f"Ошибка: недопустимое значение sentiment: {item['sentiment']}"
        
        return f"Успех: проверено {len(data)} записей. Все поля на месте."
    except json.JSONDecodeError as e:
        return f"Ошибка JSON: {e}"

# Запуск проверки
print(validate_response(model_response))