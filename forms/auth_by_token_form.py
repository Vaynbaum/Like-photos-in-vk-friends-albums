from time import sleep
from tkinter import *
from tkinter import messagebox


from handlers.auth.exceptions.auth_password_exceptoin import AuthPasswordException
from handlers.auth.exceptions.parse_url_exception import ParseURLException
from handlers.main.main_handler import MainHandler


class AuthTokenForm:
    def __init__(self, main_handler: MainHandler, width=450, length=200):
        self.__main_handler = main_handler
        self.__padx = 15
        self.__pady = 15

        self.__root: Tk = self.__init_form(width, length)

    def run(self) -> None:
        """Launches the form"""
        self.__root.mainloop()

    def register_event_destroy(self, func) -> None:
        """Adds a callback to the destroy event of the form

        Args:
            func: callback function
        """
        self.__root.bind("<Destroy>", func)

    def __init_form(self, width: int, length: int) -> Tk:
        """Initializes the form

        Args:
            width (int): Width of the form
            length (int): Length of the form

        Returns:
            Tk: Form window
        """
        root = Tk()
        self.__url_value = StringVar(root)

        root.title(_("Authorization by access token"))
        root.geometry(f"{width}x{length}")
        root.resizable(width=False, height=False)

        label_text = _(
            """Go to the site, allow access,\nafter redirecting to another page,\nenter the URL in the field"""
        )
        Label(root, text=label_text, justify=LEFT).grid(
            row=1,
            column=1,
            padx=self.__padx,
            pady=self.__pady,
        )
        Button(
            root,
            text=_("Go to the website"),
            command=self.__main_handler.go_site_to_auth,
        ).grid(row=1, column=2)
        Label(root, text="URL").grid(
            row=2,
            column=1,
            padx=self.__padx,
            pady=self.__pady,
        )
        Entry(root, textvariable=self.__url_value).grid(
            row=2,
            column=2,
            padx=self.__padx,
            pady=self.__pady,
        )
        Button(root, text=_("Enter"), command=self.__login).grid(row=3, column=1)
        return root

    def __login(self)-> None:
        """Authorization button handler"""
        try:
            token = self.__main_handler.parse_url(self.__url_value.get())

            self.__main_handler.auth_by_access_token(token)
            messagebox.showinfo(
                _("Authorization successful"),
                _("You have successfully logged in using the entered url"),
            )
            sleep(0.25)
            self.__root.destroy()
        except (AuthPasswordException, ParseURLException) as e:
            messagebox.showinfo(_("Authorization failed"), e)
