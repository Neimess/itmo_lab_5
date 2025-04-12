# Доделка 5 домашки picsum.photos
import asyncio
import logging
import os

import aiofiles
import aiohttp

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(filename)s - %(name)s/%(funcName)s - %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
logger = logging.getLogger("task_1")
logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT))
logger.addHandler(console_handler)


class Fetcher:
    def __init__(self, url: str, counter: int, save_path: str) -> None:
        """_summary_

        Args:
            counter (int): Количество картинок
            save_path (str): Путь для сохранения картинок
        """
        self.url = url
        self.counter = counter
        self.save_path = save_path
        os.makedirs(self.save_path, exist_ok=True)

    async def _fetch_image(self, session: aiohttp.ClientSession, idx: int) -> None:
        """
        Загружает одно изображение.

        Args:
            session (aiohttp.ClientSession): Сессия для запросов.
            idx (int): Индекс изображения (для отладки или сохранения).
        """
        try:
            async with session.get(self.url) as response:
                if response.status == 200:
                    data = await response.read()
                    file_path = os.path.join(self.save_path, f"image_{idx}.jpg")
                    async with aiofiles.open(file_path, "wb") as file:
                        await file.write(data)
                        logger.info("Файл сохраненен")
                else:
                    logger.warning("Не удалось загрузить изображение %i: статус %i", idx, response.status)
        except Exception as e:
            logger.error("Ошибка при загрузке изображения %i: %s", idx, e)

    async def fetch(self) -> None:
        async with aiohttp.ClientSession() as session:
            tasks = [self._fetch_image(session, idx) for idx in range(self.counter)]
            await asyncio.gather(*tasks)


async def main() -> None:
    fetcher = Fetcher("https://picsum.photos/200", 5, "artifacts/task_1")
    start = asyncio.get_event_loop().time()
    await fetcher.fetch()
    duration = asyncio.get_event_loop().time() - start
    logger.info("Асинхронная загрузка завершена за %.2f секунд.", duration)


if __name__ == "__main__":
    asyncio.run(main())
