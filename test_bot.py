import asyncio
from telegram import Bot
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

BOT_TOKEN = "8180882685:AAHb7zYf3v-Xr1inr0JQly7_p-oDLj4aWWw"
CHAT_ID = "1688985791"

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
        time.sleep(5)
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
    separador = "🔄 *Nueva ejecución del chequeo de rankings*\n━━━━━━━━━━━━━━━━━━━━━━━"
    await bot.send_message(chat_id=CHAT_ID, text=separador, parse_mode="Markdown")
    for producto in productos:
        asin = producto["asin"]
        nombre = producto["nombre"]
        rank = get_second_category_rank(asin)
        mensaje = f"> Amazon Rank Bot:\n🛍️ {nombre}\n📊 {rank}"
        await bot.send_message(chat_id=CHAT_ID, text=mensaje)
        time.sleep(2)

if __name__ == "__main__":
    while True:
        asyncio.run(main())
        time.sleep(2 * 60 * 60)
