import asyncio
import aiohttp
import configparser

config = configparser.ConfigParser()
config.read("config.ini")
SERVER_URL = config.get('API', 'URL')

async def fetch_goods(session):
    """
    Асинхронно получает список альбомов с сервера.
    :param session: асинхронная сессия aiohttp.
    """
    try:
        async with session.get(SERVER_URL) as response:
            response.raise_for_status()
            return await response.json()
    except aiohttp.ClientError as e:
        print(f"Ошибка при получении данных с сервера: {e}")
        return []

async def monitor_new_price(poll_interval=5):
    """
    Следит за добавлением новых данных на сервер асинхронно.
    :param poll_interval: интервал между запросами в секундах.
    """
    print("Начинаем асинхронный мониторинг новых товаров...")
    known_goods = {}

    async with aiohttp.ClientSession() as session:
        # Первоначальная загрузка альбомов
        goods = await fetch_goods(session)
        known_goods = {good['id']: good for good in goods}

        while True:
            await asyncio.sleep(poll_interval)  # Асинхронная пауза
            goods = await fetch_goods(session)

            # Проверяем новые альбомы
            for good in goods:
                if good['id'] not in known_goods:
                    print(f"Новый товар добавлен: {good['name']} - {good['price']}")
                    known_goods[good['id']] = good  # Добавляем новый альбом в известные

if __name__ == "__main__":
    # Запуск асинхронного мониторинга
    asyncio.run(monitor_new_price(poll_interval=5))
