import pandas as pd
import re

df = pd.read_csv("companies_list.csv", delimiter=";", dtype=str, nrows=5)#ЗДЕСЬ УБРАТЬ nrows ДЛЯ АНАЛИЗА ВСЕЙ ТАБЛИЦЫ

base_columns = [
    "Наименование",
    "ИНН",
    "Дата регистрации",
    "ФИО руководителя",
    "Номер телефона",
    "Ссылка на сайт",
    "Основной вид деятельности"
]

email_columns = ["Электронная почта"] + [f"Дополнительная электронная почта {i}" for i in range(1, 10)]

def email_priority(email: str) -> int:
    email = email.lower()
    if re.search(r"(hr|marketing|pr)", email):
        return 3
    if re.search(r"(info|support|sales|hello|sale|help)", email):
        return 2
    return 1

def collect_emails(row):
    emails = [row[col] for col in email_columns if pd.notna(row.get(col, None)) and row[col].strip()]
    if not emails:
        return None
    emails_sorted = sorted(emails, key=email_priority)
    return ", ".join(emails_sorted)

result = df[base_columns].copy()
result["Электронные почты"] = df.apply(collect_emails, axis=1)

result.to_csv("companies_filtered.csv", index=False, sep=";")
