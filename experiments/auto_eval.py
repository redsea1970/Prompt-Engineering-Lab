"""
Prompt-Engineering-Lab: автооценка промптов (20 задач × 3 варианта).
Опора: глава 5 книги «AI-инженерия» (Чип Хьюен).
"""

import json
import os
import re

TASKS = [
    {"id": 1, "question": "Как создать функцию в Python?", "expected": "def"},
    {"id": 2, "question": "Как объявить переменную в Python?", "expected": "="},
    {"id": 3, "question": "Как сделать ветку в Git?", "expected": "git branch"},
    {"id": 4, "question": "Как сделать коммит в Git?", "expected": "git commit"},
    {"id": 5, "question": "Как собрать Docker-образ?", "expected": "docker build"},
    {"id": 6, "question": "Как запустить контейнер?", "expected": "docker run"},
    {"id": 7, "question": "Как обработать исключение в Python?", "expected": "try"},
    {"id": 8, "question": "Как открыть файл в Python?", "expected": "open"},
    {"id": 9, "question": "Как создать список в Python?", "expected": "["},
    {"id": 10, "question": "Как добавить элемент в список?", "expected": "append"},
    {"id": 11, "question": "Как отправить изменения в Git?", "expected": "git push"},
    {"id": 12, "question": "Как клонировать репозиторий?", "expected": "git clone"},
    {"id": 13, "question": "Как указать базовый образ в Dockerfile?", "expected": "FROM"},
    {"id": 14, "question": "Как скопировать файлы в Dockerfile?", "expected": "COPY"},
    {"id": 15, "question": "Как запустить команду в Dockerfile?", "expected": "RUN"},
    {"id": 16, "question": "Как вернуть значение из функции?", "expected": "return"},
    {"id": 17, "question": "Как создать цикл в Python?", "expected": "for"},
    {"id": 18, "question": "Как проверить условие в Python?", "expected": "if"},
    {"id": 19, "question": "Как соединить строки в Python?", "expected": "+"},
    {"id": 20, "question": "Как импортировать модуль в Python?", "expected": "import"},
]

PROMPTS = {
    "baseline": "Ответь на вопрос: {q}",
    "ricce": "Роль: эксперт. Инструкция: ответь кратко и по делу. Контекст: вопрос ниже. Ограничения: не выдумывай. Вопрос: {q}",
    "few_shot": "Пример: Вопрос: Как объявить переменную? Ответ: x = 1.\nВопрос: {q}\nОтвет:",
}


def demo_model(prompt_text):
    """Заглушка: отвечает по ключевым словам вопроса, а не по промпту."""
    if "функци" in prompt_text:
        return "def my_func(): pass"
    if "переменн" in prompt_text:
        return "x = 10"
    if "ветк" in prompt_text:
        return "git branch feature"
    if "коммит" in prompt_text:
        return "git commit -m 'msg'"
    if "образ" in prompt_text and "собр" in prompt_text:
        return "docker build -t app ."
    if "контейнер" in prompt_text and "запуст" in prompt_text:
        return "docker run app"
    if "исключен" in prompt_text:
        return "try:\n    pass\nexcept Exception:\n    pass"
    if "открыть файл" in prompt_text:
        return "open('file.txt', 'r')"
    if "список" in prompt_text:
        return "[]"
    if "добавить элемент" in prompt_text:
        return "lst.append(x)"
    if "push" in prompt_text or "отправить изменен" in prompt_text:
        return "git push origin main"
    if "клон" in prompt_text:
        return "git clone <url>"
    if "базовый образ" in prompt_text:
        return "FROM python:3.11"
    if "скопировать" in prompt_text:
        return "COPY . ."
    if "запустить команд" in prompt_text:
        return "RUN pip install -r requirements.txt"
    if "вернуть" in prompt_text:
        return "return value"
    if "цикл" in prompt_text:
        return "for i in range(10): pass"
    if "условие" in prompt_text:
        return "if x > 0: pass"
    if "соединить строк" in prompt_text:
        return "'a' + 'b'"
    if "импортировать" in prompt_text:
        return "import os"
    return "Не знаю"


def evaluate_variant(prompt_template, tasks):
    correct = 0
    total_len = 0
    details = []
    for task in tasks:
        prompt = prompt_template.format(q=task["question"])
        answer = demo_model(prompt)
        ok = task["expected"].lower() in answer.lower()
        correct += int(ok)
        total_len += len(answer)
        details.append({"id": task["id"], "expected": task["expected"], "answer": answer, "correct": ok})
    n = len(tasks)
    return {
        "accuracy": round(correct / n, 4) if n else 0,
        "avg_answer_len": round(total_len / n, 1) if n else 0,
        "details": details,
    }

def main():
    results = {}
    for name, template in PROMPTS.items():
        results[name] = evaluate_variant(template, TASKS)

    os.makedirs("results", exist_ok=True)
    with open("results/auto_eval.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print("=" * 70)
    print(f"{'Вариант':<12} {'Accuracy':>10} {'Avg len':>10}")
    print("-" * 70)
    for name, r in results.items():
        print(f"{name:<12} {r['accuracy']:>10.2%} {r['avg_answer_len']:>10.1f}")
    print("=" * 70)
    print("Результаты сохранены в results/auto_eval.json")

if __name__ == "__main__":
    main()
