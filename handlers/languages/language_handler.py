from handlers.languages.language import Language


class LanguageHandler:
    def __init__(self, languages: list[Language]):
        self.__languages = languages
        self.__current_language = self.__languages[0]
        self.__current_language.install_language()

    def languages(self) -> list[Language]:
        """Returns a list of languages

        Returns:
            list[Language]: List of languages
        """
        return self.__languages

    def install_language(self, name_language: str):
        """Sets the language

        Args:
            name_language (str)
        """
        lang = list(
            filter(
                lambda language: name_language == language.name_language(),
                self.__languages,
            )
        )
        self.__current_language = lang[0]
        self.__current_language.install_language()

    def get_current_language_abbreviation(self) -> str:
        """Returns the abbreviation of the currently installed language

        Returns:
            str: Language abbreviation
        """       
        return self.__current_language.abbreviation()
