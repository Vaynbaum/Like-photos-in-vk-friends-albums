from abc import ABC, abstractmethod


class Language(ABC):
    pass

    @abstractmethod
    def name_language(self):
        """Returns the name of the language

        Returns:
            str: Name of the language
        """
        pass

    @abstractmethod
    def install_language(self):
        """Sets the language
        """ 
        pass

    @abstractmethod
    def abbreviation(self) -> str:
        """Returns the abbreviation of the currently installed language

        Returns:
            str: Language abbreviation
        """ 
        pass
