import vk
import webbrowser

from handlers.auth.exceptions.auth_password_exceptoin import AuthPasswordException
from handlers.auth.exceptions.auth_token_exception import AuthTokenException
from handlers.auth.exceptions.parse_url_exception import ParseURLException


class AuthHandler:
    def __init__(self):
        self.__version = "5.131"
        self.__url = """https://oauth.vk.com/authorize?client_id=6287487&scope=1073737727&redirect_uri=https://oauth.vk.com/blank.html&display=page&response_type=token&revoke=1"""
        self.__scope = "1073737727"
        self.__app_id = "8231739"
        self.__name_file = "auth_vk.ini"

    def auth_password(self, login: str, password: str) -> vk.API:
        """Login and password authorization

        Args:
            login (str)
            password (str)

        Raises:
            AuthPasswordException: If the username or password is incorrect

        Returns:
            vk.API: API with an authorized session
        """
        try:
            session = vk.AuthSession(
                app_id=self.__app_id,
                user_login=login,
                user_password=password,
                scope=self.__scope,
            )
            file = open(self.__name_file, "w")
            file.writelines(session.access_token)
            api = vk.API(session, v=self.__version)
            api.account.getProfileInfo()
            return api
        except:
            raise AuthPasswordException(_("The username or password is not correct"))

    def auth_token(self, token: str | None) -> vk.API:
        """Token authorization

        Args:
            token (str | None)

        Raises:
            AuthTokenException: If the token is invalid

        Returns:
            vk.API: API with an authorized session
        """
        try:
            if token is None:
                file = open(self.__name_file, "r")
                token = file.readline()
            else:
                file = open(self.__name_file, "w")
                file.writelines(token)

            api = vk.API(vk.Session(token), v=self.__version)
            api.account.getProfileInfo()
            return api
        except:
            raise AuthTokenException(_("Token is not valid"))

    def go_to_site(self):
        """Go to the site to get a token"""
        webbrowser.open(self.__url)

    def parse_url(self, url: str) -> str:
        """Parsing the URL getting an access token

        Args:
            url (str)

        Raises:
            ParseURLException: If the query parameters are set incorrectly or
            the access token couldn't be found

        Returns:
            str: Access token
        """
        parts = url.split("access_token=")
        if len(parts) == 2:
            token_part = parts[1]
            access_token_parts = token_part.split("&")

            if len(access_token_parts) > 0:
                return access_token_parts[0]
            raise ParseURLException(_("Query parameters are set incorrectly"))

        raise ParseURLException(_("Couldn't find access token"))

    def delete_saved_access_token(self):
        """Deleting a saved token from a file"""
        open(self.__name_file, "w")
