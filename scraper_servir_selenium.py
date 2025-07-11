from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')

driver = webdriver.Chrome(options=options)
url = "https://app.servir.gob.pe/DifusionOfertasExterno/faces/consultas/ofertas_laborales.xhtml"
driver.get(url)

WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "frmListarOfertasLaborales:tblOfertasLaborales_data"))
)
time.sleep(2)

rows = driver.find_elements(By.CSS_SELECTOR, "#frmListarOfertasLaborales\\:tblOfertasLaborales_data > tr")
convocatorias = []

for row in rows:
    cols = row.find_elements(By.TAG_NAME, "td")
    if len(cols) >= 6:
        titulo = cols[0].text.strip()
        entidad = cols[1].text.strip()
        fecha = cols[2].text.strip()
        try:
            link = cols[5].find_element(By.TAG_NAME, "a").get_attribute("href")
        except:
            link = "#"

        convocatoria = {
            "titulo": f"{entidad} - {titulo}",
            "fecha": fecha,
            "region": "Perú",
            "perfiles": [titulo],
            "enlace": link
        }
        convocatorias.append(convocatoria)

with open("convocatorias.json", "w", encoding="utf-8") as f:
    json.dump(convocatorias, f, indent=2, ensure_ascii=False)

print(f"Se extrajeron {len(convocatorias)} convocatorias.")
driver.quit()