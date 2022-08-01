import vk
from vk.exceptions import VkAPIError
from models.album import Album
from models.photo import Photo
from models.user import User

from handlers.photo.exceptions.get_albums_exception import GetAlbumsException
from handlers.photo.exceptions.get_photos_exception import GetPhotosException


class PhotoHandler:
    def get_albums(self, api: vk.API, owner: User, lang: str) -> list[Album]:
        """Getting user album data

        Args:
            api (vk.API): API with an authorized session
            owner (User): User selected
            lang (str): Language abbreviation

        Raises:
            GetAlbumsException: If the albums of the selected user could not be retrieved

        Returns:
            list[Album]: List of user's albums
        """        
        try:
            albums = api.photos.getAlbums(owner_id=owner.id, need_system=1, lang=lang)
            return [Album.of(album) for album in albums["items"]]
        except VkAPIError:
            raise GetAlbumsException(
                _("The albums of the selected user could not be received")
            )

    def get_photos(self, api: vk.API, album: Album, like)-> list[Photo]:
        """Getting album photos data

        Args:
            api (vk.API): API with an authorized session
            album (Album): Album selected
            like (bool, optional): Flag whether the photos are liked by the current user

        Raises:
            GetPhotosException: If it was't possible to get photos from the selected album

        Returns:
            list[Photo]: List of album photos
        """        
        try:
            photos = api.photos.get(
                owner_id=album.owner_id,
                album_id=album.id,
                extended="1",
                count=album.size + 1,
            )

            return [
                Photo.of(photo)
                for photo in photos["items"]
                if photo["likes"]["user_likes"] == (0 if like else 1)
            ]
        except VkAPIError:
            raise GetPhotosException(_("Couldn't get photos of the selected album"))
