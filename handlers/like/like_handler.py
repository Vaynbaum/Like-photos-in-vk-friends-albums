from threading import *
from vk.exceptions import VkAPIError
from time import sleep
import vk
import math

from models.captcha import Captcha
from models.photo import Photo


class LikeHandler:
    def __calc_sleep(self, arg: float) -> float:
        """Calculating seconds between requests

        Args:
            arg (float): The previous value of the argument for the variable part of seconds

        Returns:
            float: Calculated time
        """
        arg += 0.1
        return 1 + abs(math.sin(arg)) * 2

    def __handle_captcha(self, url: str, display_captcha) -> str:
        """Captcha processing

        Args:
            url (str): Captcha image URL
            display_captcha: Callback captcha display functions

        Returns:
            str: Captcha text
        """
        event = Event()
        captcha = Captcha(url=url)
        thread = Thread(target=display_captcha, args=(captcha, event))
        thread.start()
        thread.join()
        return captcha.text

    def __query_like(self, api: vk.API, photo: Photo, display_captcha) -> dict:
        """Run a query to like

        Args:
            api (vk.API): API with an authorized session
            photo (Photo): Photo model
            display_captcha: Callback captcha display functions

        Returns:
            dict: Query result
        """
        try:
            return api.likes.add(
                type="photo", owner_id=photo.owner_id, item_id=photo.id
            )
        except VkAPIError as exc:
            captcha_key = self.__handle_captcha(exc.captcha_img, display_captcha)
            return api.likes.add(
                type="photo",
                owner_id=photo.owner_id,
                item_id=photo.id,
                captcha_key=captcha_key,
                captcha_sid=exc.captcha_sid,
            )

    def __query_no_like(self, api: vk.API, photo: Photo, display_captcha):
        """Run a query to dislike

        Args:
            api (vk.API): API with an authorized session
            photo (Photo): Photo model
            display_captcha: Callback captcha display functions

        Returns:
            Query result
        """
        try:
            return api.likes.delete(
                type="photo", owner_id=photo.owner_id, item_id=photo.id
            )
        except VkAPIError as exc:
            captcha_key = self.__handle_captcha(exc.captcha_img, display_captcha)
            return api.likes.delete(
                type="photo",
                owner_id=photo.owner_id,
                item_id=photo.id,
                captcha_key=captcha_key,
                captcha_sid=exc.captcha_sid,
            )

    def put_likes(
        self,
        api: vk.API,
        photos: list[Photo],
        event: Event,
        display_progress,
        display_captcha,
        part: int,
        all_part: int,
    ) -> None:
        """Put likes on photos

        Args:
            api (vk.API): API with an authorized session
            photo (Photo): Photo model
            event (Event): Operation cancellation event
            display_progress: Callback progress display functions
            display_captcha: Callback captcha display functions
        """
        arg_sin_offset_sleep = 0
        ind_photo = 0
        count_photos = len(photos)
        while not event.is_set() and ind_photo < count_photos:
            try:
                res = self.__query_like(api, photos[ind_photo], display_captcha)
                if res["likes"] > -1:
                    display_progress(ind_photo + 1, count_photos, part, all_part)
                sleep(self.__calc_sleep(arg_sin_offset_sleep))
            except VkAPIError:
                sleep(4)
                res = self.__query_like(api, photos[ind_photo], display_captcha)
                if res["likes"] > -1:
                    display_progress(ind_photo + 1, count_photos, part, all_part)
            ind_photo += 1

    def remove_likes(
        self,
        api: vk.API,
        photos: list[Photo],
        event: Event,
        display_progress,
        display_captcha,
        part: int,
        all_part: int,
    ):
        """Remove likes from photos

        Args:
            api (vk.API): API with an authorized session
            photo (Photo): Photo model
            event (Event): Operation cancellation event
            display_progress: Callback progress display functions
            display_captcha: Callback captcha display functions
        """
        arg_sin_offset_sleep = 0
        ind_photo = 0
        count_photos = len(photos)
        while not event.is_set() and ind_photo < count_photos:
            try:
                res = self.__query_no_like(api, photos[ind_photo], display_captcha)
                if res["likes"] > -1:
                    display_progress(ind_photo + 1, count_photos, part, all_part)
                sleep(self.__calc_sleep(arg_sin_offset_sleep))

            except VkAPIError:
                sleep(4)
                res = self.__query_no_like(api, photos[ind_photo], display_captcha)
                if res["likes"] > -1:
                    display_progress(ind_photo + 1, count_photos, part, all_part)
            ind_photo += 1
