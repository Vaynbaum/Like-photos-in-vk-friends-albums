import requests
from io import BytesIO
from PIL import Image

from handlers.download.exceptions.timeout_exception import DownloadImageException


class DownloadHandler:
    def load_image(self, url: str) -> Image.Image:
        """Downloads an image by url

        Args:
            url (str): Image URL

        Raises:
            DownloadImageException: If timeout error or HTTP error

        Returns:
            Image.Image: Downloaded image
        """ 
        try:
            response = requests.get(url, timeout=10)
            if response.status_code != 200:
                DownloadImageException(f'{_("HTTP error")} {response.status_code}')
            else:
                return Image.open(BytesIO(response.content))
        except requests.exceptions.Timeout:
            raise DownloadImageException(_("Timeout error"))
