import httpx
import hishel
from loguru import logger
import os

class Client:
    def __init__(self, proxy_pool: str | None = None):
        self.proxy_pool = proxy_pool
        if self.proxy_pool:
            logger.info(f"Using proxy pool: {self.proxy_pool}")

        cache_dir = os.path.expanduser('~/.cache/hishel')
        self.storage = hishel.FileStorage(base_path=cache_dir)
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36 Edg/85.0.564.60"
        }

    def random_proxy(self):
        if not self.proxy_pool:
            return None

        with httpx.Client() as client:
            r = client.get(self.proxy_pool)
            if r.status_code == httpx.codes.OK:
                return 'http://' + r.json().get('proxy')
            else:
                logger.error(f"Failed to get proxy from {self.proxy_pool}")
                return None

    def get(self, url_generator):
        with hishel.CacheClient(headers=self.headers, storage=self.storage, proxies=self.random_proxy()) as client:
            html = None
            while True:
                try:
                    url = url_generator.send(html)
                except StopIteration:
                    break
                r = client.get(url, follow_redirects=True, extensions={"force_cache": True})
                if r.status_code == httpx.codes.OK:
                    html = r.text
                else:
                    logger.error(f"Failed to fetch {url}")
                    html = None
