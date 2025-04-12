import logging
import os
import time

import requests

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(filename)s - %(name)s/%(funcName)s - %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
logger = logging.getLogger("task_1_sync")
logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT))
logger.addHandler(console_handler)


class SyncFetcher:
    def __init__(self, url: str, counter: int, save_path: str) -> None:
        self.url = url
        self.counter = counter
        self.save_path = save_path
        os.makedirs(self.save_path, exist_ok=True)

    def fetch_image(self, idx: int) -> None:
        try:
            response = requests.get(self.url)
            if response.status_code == 200:
                file_path = os.path.join(self.save_path, f"image_{idx}.jpg")
                with open(file_path, "wb") as file:
                    file.write(response.content)
                    logger.info("Файл сохраненен")
            else:
                logger.warning("Не удалось загрузить изображение %i: статус %i", idx, response.status_code)
        except Exception as e:
            logger.error("Ошибка при загрузке изображения %i: %s", idx, e)

    def fetch(self) -> None:
        for idx in range(self.counter):
            self.fetch_image(idx)


if __name__ == "__main__":
    fetcher = SyncFetcher("https://picsum.photos/200", 5, "artifacts/task_1_sync")

    start = time.time()
    fetcher.fetch()
    duration = time.time() - start

    logger.info("Синхронная загрузка завершена за %.2f секунд.", duration)
