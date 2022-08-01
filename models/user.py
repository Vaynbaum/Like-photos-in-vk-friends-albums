from pydantic import BaseModel


class User(BaseModel):
    id: int
    first_name: str
    last_name: str

    @staticmethod
    def of(user: dict):
        """Converts the received data to a model

        Args:
            user (dict): the received data

        Returns:
            User: user model
        """
        return User(**user)

    def fullname(self) -> str:
        """The full name of the user

        Returns:
            str: Created full name
        """
        return f"{self.first_name} {self.last_name}"
