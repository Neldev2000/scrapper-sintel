import pandas as pd

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By 
from selenium.webdriver.chrome.options import Options

import time
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)





url = input("Coloca el enlace del cuestionario: ")
iteraciones = int(input("Cuantas itereaciones vas a necesitar: "))
#url = "http://www.ing.ula.ve/mentor/Sistemas%20Inteligentes/Agentes%20Cognoscitivos/Teleclase/Evaluacion%20Centralizada/Autoevaluacion/Autoevaluacion.php"

#Comienzo Web Scraping   
service = Service(ChromeDriverManager().install())

data = pd.DataFrame({'Pregunta' : [], 'index' : [], 'respuesta' : []})
idx = 0
for y in range(iteraciones):
    driver = webdriver.Chrome(service=service, chrome_options=chrome_options)
    driver.get(url)
    for i in range(10):
        html = driver.page_source
        pregunta = str(driver.find_element(By.NAME, "Pregunta").get_attribute("value"))
        respuesta = int(driver.find_element(By.NAME, "Correcta").get_attribute("value"))

        string_ini = f"<br><input name=\"Respuesta\" type=\"radio\" size=\"80\" value=\"{respuesta}\">"
 
        j = html.find(string_ini) + len(string_ini)
        k = html.find('\n', j)

        texto_res = html[j:k]
        
        opcion_correcta = driver.find_element(By.XPATH, f"//input[@name='Respuesta'][@value='{respuesta}']").click()

        new_row = pd.DataFrame({'Pregunta' : pregunta, 'index' : respuesta, 'respuesta' : texto_res},  index=[0])
        data = pd.concat([data, new_row], ignore_index=True)

        driver.find_element(By.XPATH, "//input[@type='submit']").click()
        driver.find_element(By.XPATH, "//input[@type='submit']").click()
    time.sleep(2)
    driver.close()

print("FIN")
data = data.drop_duplicates(subset=['Pregunta'])
data.to_excel("respuestas.xlsx")