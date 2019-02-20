# last edit: 20.02.2019 (callFEELD)
from socket import timeout
import urllib.error, urllib.request, json

from src.handler.logger import logger

class  JSON_APIRequest:

    # timeout per reques in seconds
    timeout = 5

    def __init__(self, url=None):
        self.url = url

    def set_url(self, url):
        self.url = url

    def get_data(self):
        try:
            url = urllib.request.urlopen(self.url, timeout=self.timeout)
            data = json.loads(str(url.read().decode()).encode('utf-8'))
            return data
        except (urllib.error.HTTPError, urllib.error.URLError) as e:
            logger.error(e)
            return None
        except timeout:
            logger.error("Socket timeout")
            return None
        except Exception as e:
            logger.error(e)
            return None
