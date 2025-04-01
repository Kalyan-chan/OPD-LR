from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import pandas as pd
import time

def get_jobs():
    opt = Options()
    opt.add_argument("--headless")
    opt.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36")
    drv = webdriver.Chrome(options=opt)
    drv.get("https://hh.ru/search/vacancy?text=Python&area=1")
    
    try:
        WebDriverWait(drv, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-qa^='vacancy-serp__vacancy']")))
    except TimeoutException:
        time.sleep(5)
    
    lst = []
    
    for itm in drv.find_elements(By.CSS_SELECTOR, "div[data-qa^='vacancy-serp__vacancy']"):
        try:
            tit = itm.find_element(By.CSS_SELECTOR, "a[data-qa='serp-item__title'] span[data-qa='serp-item__title-text']").text
            lnk = itm.find_element(By.CSS_SELECTOR, "a[data-qa='serp-item__title']").get_attribute("href")
        except:
            tit, lnk = "", ""
        
        try:
            emp = itm.find_element(By.CSS_SELECTOR, "a[data-qa='vacancy-serp__vacancy-employer'] span[data-qa='vacancy-serp__vacancy-employer-text']").text
        except:
            emp = ""
        
        try:
            sal = itm.find_element(By.CSS_SELECTOR, "div.compensation-labels--vwum2s12fQUurc2J span").text.strip()
            if "опыт" in sal.lower() or not sal:
                sal = "Не указана"
        except:
            sal = "Не указана"
        
        lst.append({"Вакансия": tit, "Компания": emp, "Зарплата": sal, "Ссылка": lnk})
    
    drv.quit()
    pd.DataFrame(lst).to_excel("jobs.xlsx", index=False)
    print("Файл сохранён.")

if __name__ == "__main__":
    get_jobs()
