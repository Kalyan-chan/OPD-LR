import requests
import pandas as pd

def get_jobs():
    url = "https://api.hh.ru/vacancies"
    params = {
        "text": "Python",
        "area": 1, 
        "per_page": 20 
    }

    response = requests.get(url, params=params)
    data = response.json()

    jobs_list = []

    for item in data["items"]:
        title = item["name"]
        link = item["alternate_url"]
        company = item["employer"]["name"]
        salary = item["salary"]
        location = item["area"]["name"]

        salary_text = "Не указана"
        if salary:
            salary_from = salary.get("from")
            salary_to = salary.get("to")
            salary_currency = salary.get("currency")
            salary_text = f"{salary_from or ''} - {salary_to or ''} {salary_currency or ''}".strip(" -")

        jobs_list.append({
            "Вакансия": title,
            "Компания": company,
            "Зарплата": salary_text,
            "Местоположение": location,
            "Ссылка": link
        })

    df = pd.DataFrame(jobs_list)
    df.to_excel("jobs.xlsx", index=False)
    print("Данные успешно записаны в файл.")

if __name__ == "__main__":
    get_jobs()
