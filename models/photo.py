from pydantic import BaseModel


class Photo(BaseModel):
    id: int
    owner_id: int
    url: str

    @staticmethod
    def of(photo: dict):
        """Converts the received data to a model

        Args:
            photo (dict): the received data

        Returns:
            Photo: photo model
        """
        return Photo(
            id=photo["id"],
            owner_id=photo["owner_id"],
            url=photo["sizes"][len(photo["sizes"]) - 1]["url"],
        )
