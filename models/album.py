from pydantic import BaseModel


class Album(BaseModel):
    id: int
    title: str
    size: int
    owner_id: int

    @staticmethod
    def of(album: dict):
        """Converts the received data to a model

        Args:
            album (dict): the received data

        Returns:
            Album: album model
        """        
        return Album(**album)
