import asyncio
from telegram import Bot
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
import time

BOT_TOKEN = "8180882685:AAHb7zYf3v-Xr1inr0JQly7_p-oDLj4aWWw"
CHAT_ID = "1688985791"

productos = [
    {"asin": "B08DFX7GHS", "nombre": "Mini Elíptica"},
    {"asin": "B0DNG5ZWT5", "nombre": "ECO-4010"},
    {"asin": "B0FCYGZHCN", "nombre": "Sillón Relax"}
]

async def get_second_category_rank(asin):
    url = f"https://www.amazon.es/dp/{asin}"
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        print(f"🔎 Procesando {asin}")
        try:
            await page.goto(url, timeout=60000)
            content = await page.content()
            soup = BeautifulSoup(content, "html.parser")

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
            await browser.close()

async def main():
    bot = Bot(token=BOT_TOKEN)
    for producto in productos:
        asin = producto["asin"]
        nombre = producto["nombre"]
        rank = await get_second_category_rank(asin)
        mensaje = f"> Amazon Rank Bot:\n🛍️ {nombre}\n📊 {rank}"
        await bot.send_message(chat_id=CHAT_ID, text=mensaje)
        await asyncio.sleep(2)
    # Separador visual entre ejecuciones
    await bot.send_message(chat_id=CHAT_ID, text="───────────── ⏱️ Fin de ejecución ─────────────")

if __name__ == "__main__":
    while True:
        asyncio.run(main())
        print("⏳ Esperando 2 horas...")
        time.sleep(2 * 60 * 60)
