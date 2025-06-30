import asyncio
from telegram import Bot
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

BOT_TOKEN = "8180882685:AAHb7zYf3v-Xr1inr0JQly7_p-oDLj4aWWw"
CHAT_ID = "1688985791"

# ASIN + nombre personalizado para identificar el producto
productos = [
    {"asin": "B08DFX7GHS", "nombre": "Mini Elíptica"},
    {"asin": "B0DNG5ZWT5", "nombre": "ECO-4010"},
    {"asin": "B0FCYGZHCN", "nombre": "Sillón Relax"}
]

def init_driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(options=options)

def get_second_category_rank(asin):
    url = f"https://www.amazon.es/dp/{asin}"
    driver = init_driver()
    print(f"🔎 Procesando {asin}")
    try:
        driver.get(url)
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "wayfinding-breadcrumbs_feature_div"))
        )
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        all_text = soup.get_text(separator="\n")
        lines = [line.strip() for line in all_text.split("\n") if line.strip().startswith("nº") and " en " in line]
        unique_lines = []
        for line in lines:
            if line not in unique_lines:
                unique_lines.append(line)

        if len(unique_lines) >= 2:
            return unique_lines[1]
        elif len(unique_lines) == 1:
            return unique_lines[0]
        else:
            return "Ranking específico no encontrado"
    except Exception as e:
        return f"❌ Error: {str(e)}"
    finally:
        driver.quit()

async def main():
    bot = Bot(token=BOT_TOKEN)
    for producto in productos:
        asin = producto["asin"]
        nombre = producto["nombre"]
        rank = get_second_category_rank(asin)
        mensaje = f"> Amazon Rank Bot:\n🛍️ {nombre}\n📊 {rank}"
        await bot.send_message(chat_id=CHAT_ID, text=mensaje)
        time.sleep(2)

    # Separador para siguiente ejecución
    await bot.send_message(chat_id=CHAT_ID, text="⏱️ Próximo chequeo en 2 horas...")

if __name__ == "__main__":
    while True:
        asyncio.run(main())
        print("⏱️ Esperando 2 horas para la próxima ejecución...")
        time.sleep(2 * 60 * 60)
