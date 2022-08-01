from tkinter import *
from PIL import ImageTk

from handlers.download.exceptions.timeout_exception import DownloadImageException
from handlers.main.main_handler import MainHandler
from models.captcha import Captcha


class CaptchaForm:
    def __init__(
        self,
        main_handler: MainHandler,
        captcha: Captcha,
        width=350,
        length=300,
    ):
        self.__main_handler = main_handler
        self.__captcha = captcha

        self.__init_form(width, length, captcha.url)

    def register_event_destroy(self, func) -> None:
        """Adds a callback to the destroy event of the form

        Args:
            func: callback function
        """
        self.__root.bind("<Destroy>", func)

    def __init_form(self, width: int, length: int, url: str) -> None:
        """Initializes the form

        Args:
            width (int): Width of the form
            length (int): Length of the form
            url (str): Captcha URL
        """
        self.__root = Tk()
        self.__root.title(_("Captcha from the image"))
        self.__root.geometry(f"{width}x{length}")
        self.__root.resizable(width=False, height=False)

        captcha_image = Label(self.__root, text=_("Loading an image..."))
        captcha_image.grid(row=0, column=1)

        self.__captcha_value = StringVar(self.__root)

        Entry(self.__root, textvariable=self.__captcha_value).grid(
            row=1, column=1, padx=15, pady=15
        )
        Button(
            self.__root, text=_("Enter the text"), command=self.__enter_captcha
        ).grid(row=2, column=1, padx=15, pady=15)

        try:
            pil_image = self.__main_handler.load_image(url)
            image = ImageTk.PhotoImage(pil_image, master=self.__root)
            captcha_image.config(image=image, text="")
            captcha_image.image = image
        except DownloadImageException as e:
            captcha_image.config(text=e)

    def __enter_captcha(self) -> None:
        """Captcha text input button handler"""
        self.__captcha.text = self.__captcha_value.get()
        self.__root.destroy()

    def run(self) -> None:
        """Launches the form"""
        self.__root.mainloop()
