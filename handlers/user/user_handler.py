import vk
from vk.exceptions import VkAPIError

from models.user import User
from handlers.user.exceptions.get_current_user_exceptoin import GetCurrentUserException
from handlers.user.exceptions.get_friends_exception import GetFriendsException


class UserHandler:
    def get_current_user(self, api: vk.API, lang: str) -> User:
        """Retrieves the data of the current authorized user

        Args:
            api (vk.API): API with an authorized session
            lang (str): Language abbreviation

        Raises:
            GetCurrentUserException: If the current user's data could not be retrieved

        Returns:
            User: The data of the current authorized user
        """
        try:
            user = api.account.getProfileInfo(lang=lang)
            return User.of(user)
        except VkAPIError:
            raise GetCurrentUserException(
                _("Could not get the data of the current user")
            )

    def get_friends(self, api: vk.API, user_id: int, lang: str) -> list[User]:
        """Getting the data of the user's friends

        Args:
            api (vk.API): API with an authorized session
            user_id (int): current authorized user id 
            lang (str): Language abbreviation

        Raises:
            GetFriendsException: If it was not possible to get the data of the current user's friends

        Returns:
            list[User]: Data of friends of the current authorized user
        """
        try:
            friends = api.friends.get(user_id=user_id, fields="all", lang=lang)
            return [User.of(friend) for friend in friends["items"]]
        except VkAPIError:
            raise GetFriendsException(
                _("Couldn't get the friends data of the current user")
            )
