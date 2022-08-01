from threading import Event
import vk
from PIL import Image

from handlers.auth.auth_handler import AuthHandler
from handlers.auth.exceptions.auth_password_exceptoin import AuthPasswordException
from handlers.auth.exceptions.auth_token_exception import AuthTokenException
from handlers.auth.exceptions.parse_url_exception import ParseURLException
from handlers.download.download_handler import DownloadHandler
from handlers.download.exceptions.timeout_exception import DownloadImageException
from handlers.languages.english_language import EnglishLanguage
from handlers.languages.language_handler import LanguageHandler
from handlers.languages.russian_language import RussianLanguage
from handlers.like.like_handler import LikeHandler
from handlers.main.exceptions.no_auth_exception import NoAuthException
from models.album import Album
from models.photo import Photo
from models.user import User
from handlers.photo.exceptions.get_albums_exception import GetAlbumsException
from handlers.photo.exceptions.get_photos_exception import GetPhotosException
from handlers.photo.photo_handler import PhotoHandler
from handlers.user.exceptions.get_current_user_exceptoin import GetCurrentUserException
from handlers.user.exceptions.get_friends_exception import GetFriendsException
from handlers.user.user_handler import UserHandler


class MainHandler:
    def __init__(self):
        english_language = EnglishLanguage()
        russian_language = RussianLanguage()
        self.__api = None
        self.__current_user = None
        self.__owners_albums = None

        self.__language_handler = LanguageHandler([russian_language, english_language])
        self.__auth_handler = AuthHandler()
        self.__user_handler = UserHandler()
        self.__photo_handler = PhotoHandler()
        self.__like_handler = LikeHandler()
        self.__download_handler = DownloadHandler()

    def languages(self):
        """Returns a list of languages

        Returns:
            list[Language]: List of languages
        """
        return self.__language_handler.languages()

    def install_language(self, name_language: str):
        """Sets the language

        Args:
            name_language (str)
        """
        self.__language_handler.install_language(name_language)

    def auth_by_password(self, login: str, password: str) -> vk.API:
        """Login and password authorization

        Args:
            login (str) password (str)

        Raises:
            AuthPasswordException: If the username or password is incorrect

        Returns:
            vk.API: API with an authorized session
        """
        try:
            self.__api = self.__auth_handler.auth_password(login, password)
        except AuthPasswordException as e:
            raise AuthPasswordException(f"{e}")

    def auth_by_access_token(self, token: str = None) -> vk.API:
        """Token authorization

        Args:
            token (str, optional): Defaults to None.

        Raises:
            AuthTokenException: If the token is invalid
        Returns:
            vk.API: API with an authorized session
        """
        try:
            self.__api = self.__auth_handler.auth_token(token)
        except AuthTokenException as e:
            raise AuthTokenException(f"{e}")

    def go_site_to_auth(self) -> None:
        """Go to the site to get a token"""
        self.__auth_handler.go_to_site()

    def parse_url(self, url: str) -> str:
        """Parsing the URL getting an access token

        Args:
            url (str)

        Raises:
            ParseURLException: ParseURLException: If the query parameters are set incorrectly
            or the access token couldn't be found

        Returns:
            str: Access token
        """
        try:
            return self.__auth_handler.parse_url(url)
        except ParseURLException as e:
            raise ParseURLException(f"{e}")

    def get_info_current_user(self) -> User:
        """Retrieves the data of the current authorized user

        Raises:
            NoAuthException: If the user is not logged in yet
            GetCurrentUserException: If the current user's data could not be retrieved

        Returns:
            User: The data of the current authorized user
        """
        if not self.check_api():
            raise NoAuthException(_("No API"))
        lang = self.__language_handler.get_current_language_abbreviation()
        try:
            self.__current_user = self.__user_handler.get_current_user(self.__api, lang)
            return self.__current_user
        except GetCurrentUserException as e:
            raise GetCurrentUserException(f"{e}")

    def get_owners_albums(self) -> list[User]:
        """Getting the data about album owners

        Raises:
            NoAuthException: If the user is not logged in yet
            GetFriendsException: If it was not possible to get the data of
            the current user's friends

        Returns:
            list[User]: Data of friends of the current authorized user
        """
        if not self.check_api():
            raise NoAuthException(_("No API"))
        lang = self.__language_handler.get_current_language_abbreviation()
        try:
            self.__owners_albums = self.__user_handler.get_friends(
                self.__api, self.__current_user.id, lang
            )
            self.__owners_albums.insert(0, self.__current_user)
            return self.__owners_albums

        except GetFriendsException as e:
            raise GetFriendsException(f"{e}")

    def get_albums(self, ind: int) -> list[Album]:
        """Getting user album data

        Args:
            ind (int): index of the album owner

        Raises:
            NoAuthException: If the user is not logged in yet
            GetAlbumsException: If the albums of the selected user could not be retrieved

        Returns:
            list[Album]: List of user's album
        """
        if not self.check_api():
            raise NoAuthException(_("No API"))
        user = self.__owners_albums[ind]
        lang = self.__language_handler.get_current_language_abbreviation()
        try:
            self.__albums = self.__photo_handler.get_albums(self.__api, user, lang)
            return self.__albums
        except GetAlbumsException as e:
            raise GetAlbumsException(f"{e}")

    def delete_saved_access_token(self) -> None:
        """Deleting a saved token from a file"""
        self.__auth_handler.delete_saved_access_token()
        self.__api = None

    def __get_photos(self, ind_album: int, like: bool) -> list[Photo]:
        """Getting album photos data

        Args:
            ind_album (int): Index of the selected album
            like (bool): Are the photos rated by an authorized user

        Raises:
            NoAuthException: If the user is not logged in yet
            GetPhotosException: If it was't possible to get photos from the selected album

        Returns:
            list[Photo]: List of album photos
        """
        if not self.check_api():
            raise NoAuthException(_("No API"))
        album = self.__albums[ind_album]
        try:
            return self.__photo_handler.get_photos(self.__api, album, like)
        except GetPhotosException as e:
            raise GetPhotosException(f"{e}")

    def put_likes(
        self, ind_album: int, event: Event, display_progress, display_captcha
    ) -> None:
        """Put likes on photos

        Args:
            ind_album (int): Index of the selected album
            event (Event):  Operation cancellation event
            display_progress: Callback progress display functions
            display_captcha: Callback captcha display functions

        Raises:
            NoAuthException: If the user is not logged in yet
            GetPhotosException: If it was't possible to get photos from the selected album
        """
        if not self.check_api():
            raise NoAuthException(_("No API"))
        try:
            photos = self.__get_photos(ind_album, True)
            self.__like_handler.put_likes(
                self.__api, photos, event, display_progress, display_captcha
            )
        except GetPhotosException as e:
            raise GetPhotosException(f"{e}")

    def remove_likes(
        self, ind_album: int, event: Event, display_progress, display_captcha
    ):
        """Remove likes from photos

        Args:
            ind_album (int): Index of the selected album
            event (Event):  Operation cancellation event
            display_progress: Callback progress display functions
            display_captcha: Callback captcha display functions

        Raises:
            NoAuthException: If the user is not logged in yet
            GetPhotosException: If it was't possible to get photos from the selected album
        """
        if not self.check_api():
            raise NoAuthException(_("No API"))
        try:
            photos = self.__get_photos(ind_album, False)
            self.__like_handler.remove_likes(
                self.__api, photos, event, display_progress, display_captcha
            )
        except GetPhotosException as e:
            raise GetPhotosException(f"{e}")

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
            return self.__download_handler.load_image(url)
        except DownloadImageException as e:
            raise DownloadImageException(f"{e}")

    def check_api(self) -> bool:
        """Checks for an api with an authorized session

        Returns:
            bool: True if there is an api and False otherwise
        """
        return self.__api is not None
