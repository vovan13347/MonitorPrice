import asyncio
import aiohttp
import requests
import time

import configparser
config = configparser.ConfigParser()
config.read("config.ini")
URL = config.get('SERVER', 'URL')

async def get_goods(session):
    async with session.get(URL) as response:
        data = await response.json()
        return {item['id']: item['price'] for item in data}

async def main():
    async with aiohttp.ClientSession() as session:
        print(f" Мониторинг товаров запущен")
        previous_prices = await get_goods(session)
        while True:
            await asyncio.sleep(5)
            current_prices = await get_goods(session)
            for id, price in current_prices.items():
                if id in previous_prices and price != previous_prices[id]:
                    print(f" Старая цена {previous_prices[id]} Новая цена {price}")
            previous_prices = current_prices

if __name__ == "__main__":
    asyncio.run(main())