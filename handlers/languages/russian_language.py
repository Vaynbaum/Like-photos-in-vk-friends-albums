import gettext, os

from handlers.languages.language import Language


class RussianLanguage(Language):
    def __init__(self):
        FOLDER_OF_THIS_FILE = os.path.dirname(os.path.abspath(__file__))
        self.__name = "Русский"
        self.__abbreviation = "ru"
        self.__lang = gettext.translation(
            "like",
            localedir=os.path.join(FOLDER_OF_THIS_FILE, "locale"),
            languages=[self.__abbreviation],
        )

    def name_language(self) -> str:
        """Returns the name of the language

        Returns:
            str: Name of the language
        """
        return self.__name

    def install_language(self) -> None:
        """Sets the language
        """        
        self.__lang.install()

    def abbreviation(self) -> str:
        """Returns the abbreviation of the currently installed language

        Returns:
            str: Language abbreviation
        """         
        return self.__abbreviation
