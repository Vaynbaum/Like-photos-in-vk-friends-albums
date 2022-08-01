from time import sleep
from tkinter import *
from tkinter import messagebox

from handlers.auth.exceptions.auth_password_exceptoin import AuthPasswordException
from handlers.main.main_handler import MainHandler


class AuthPasswordForm:
    def __init__(self, main_handler: MainHandler, width=320, length=200):
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
        root.title(_("Authorization by password"))
        root.geometry(f"{width}x{length}")
        root.resizable(width=False, height=False)

        self.__init_entries(root)
        self.__init_button(root)
        return root

    def __init_entries(self, root: Tk) -> None:
        """Initializes the data entry fields on the form

        Args:
            root (Tk): Form window
        """
        login_value = StringVar(root)
        password_value = StringVar(root)

        Label(root, text=_("Login")).grid(
            row=1,
            column=1,
            padx=self.__padx,
            pady=self.__pady,
        )

        Entry(root, textvariable=login_value).grid(
            row=1,
            column=2,
            padx=self.__padx,
            pady=self.__pady,
        )

        Label(root, text=_("Password")).grid(
            row=3,
            column=1,
            padx=self.__padx,
            pady=self.__pady,
        )
        Entry(root, textvariable=password_value).grid(
            row=3,
            column=2,
            padx=self.__padx,
            pady=self.__pady,
        )

        self.__login_value = login_value
        self.__password_value = password_value

    def __init_button(self, root: Tk) -> None:
        """Initializes buttons on the form

        Args:
            root (Tk): Form window
        """
        btn = Button(root, text=_("Enter"), command=self.__login)
        btn.grid(
            row=4,
            column=2,
            padx=self.__padx,
            pady=self.__pady,
        )

    def __login(self) -> None:
        """Authorization button handler"""
        try:
            self.__main_handler.auth_by_password(
                self.__login_value.get(), self.__password_value.get()
            )
            messagebox.showinfo(
                _("Authorization successful"),
                _(
                    "You have successfully logged in using the login and password you entered"
                ),
            )
            sleep(0.25)
            self.__root.destroy()
        except AuthPasswordException as e:
            messagebox.showinfo(
                _("Authorization failed"),
                f'{e}. {_("Check the entered data or try to log in with an access token")}',
            )
