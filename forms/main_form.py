from tkinter import *
from tkinter import messagebox
from threading import Event

from handlers.auth.exceptions.auth_token_exception import AuthTokenException
from forms.auth_by_password_form import AuthPasswordForm
from forms.auth_by_token_form import AuthTokenForm
from forms.captcha_form import CaptchaForm
from handlers.main.exceptions.no_auth_exception import NoAuthException
from handlers.main.main_handler import MainHandler
from models.album import Album
from models.captcha import Captcha
from models.user import User
from handlers.photo.exceptions.get_albums_exception import GetAlbumsException
from handlers.photo.exceptions.get_photos_exception import GetPhotosException
from handlers.user.exceptions.get_current_user_exceptoin import GetCurrentUserException
from handlers.user.exceptions.get_friends_exception import GetFriendsException


class MainForm:
    def __init__(self, width=750, length=400):
        self.__main_handler = MainHandler()
        self.__last_select_owner = None
        self.__event_cancel_liking = None
        self.__init_form(width, length)

    def run(self) -> None:
        """Launches the form"""
        self.__root.mainloop()

    def __init_form(self, width: int, length: int) -> None:
        """Initializes the form

        Args:
            width (int): Width of the form
            length (int): Length of the form
        """
        self.__root = Tk()
        self.__root.title(_("Like photos in VK albums"))
        self.__root.geometry(f"{width}x{length}")
        self.__init_menu(self.__root)
        self.__init_main_components(self.__root)

    def __init_menu(self, root: Tk) -> None:
        """Initializing the menu on the form

        Args:
            root (Tk): Form window
        """
        self.__langs_menu = Menu(root, tearoff=0)
        self.__main_menu = Menu(root, tearoff=0)
        self.__auth_menu = Menu(root, tearoff=0)

        langs = self.__main_handler.languages()
        self.__lang = StringVar(root, value=langs[0].name_language())
        self.__lang.trace("w", self.__change_language)

        for lang in langs:
            name = lang.name_language()
            self.__langs_menu.add_radiobutton(
                label=name, value=name, variable=self.__lang
            )

        self.__auth_menu.add_command(
            label=_("Auth by password"), command=self.__auth_by_password
        )
        self.__auth_menu.add_command(
            label=_("Auth by access token"), command=self.__auth_by_token
        )
        self.__auth_menu.add_command(
            label=_("Delete a saved access token"), command=self.__delete_access_token
        )

        self.__main_menu.add_cascade(label=_("Auth"), menu=self.__auth_menu)
        self.__main_menu.add_cascade(label=_("Language"), menu=self.__langs_menu)
        root.config(menu=self.__main_menu)

    def __init_main_components(self, root: Tk) -> None:
        """Initialization of the main components on the form

        Args:
            root (Tk): Form window
        """
        self.__owner_title = StringVar(root, value=_("Owners albums"))
        self.__owner_button = StringVar(root, value=_("Show albums"))

        self.__albums_title = StringVar(root, value=_("Albums"))
        self.__put_like = StringVar(root, value=_("Put likes"))
        self.__remove_like = StringVar(root, value=_("Remove likes"))

        Label(root, textvariable=self.__owner_title).grid(row=0, column=0)
        self.__owners_listbox = Listbox(root, width=45, height=20, selectmode=SINGLE)
        self.__owners_listbox.grid(
            row=1, column=0, sticky=f"{W}{E}", columnspan=2, rowspan=2
        )
        self.__button_show_albums = Button(
            textvariable=self.__owner_button,
            state="disabled",
            command=self.__show_albums,
        )
        self.__button_show_albums.grid(row=0, column=1)

        Label(root, textvariable=self.__albums_title).grid(row=0, column=2)
        self.__albums_listbox = Listbox(root, width=60, height=20, selectmode=SINGLE)
        self.__albums_listbox.grid(
            row=1, column=2, sticky=f"{W}{E}", columnspan=3, rowspan=2
        )
        self.__button_put_likes = Button(
            textvariable=self.__put_like, state="disabled", command=self.__put_likes
        )
        self.__button_put_likes.grid(row=0, column=3)
        self.__button_remove_likes = Button(
            textvariable=self.__remove_like,
            state="disabled",
            command=self.__remove_likes,
        )
        self.__button_remove_likes.grid(row=0, column=4)

    def __change_language(self, *args) -> None:
        """Language selection handler in the menu"""
        name_language = self.__lang.get()
        old_main_menu_names = [_("Auth"), _("Language")]
        old_auth_menu_names = [
            _("Auth by password"),
            _("Auth by access token"),
            _("Delete a saved access token"),
        ]

        self.__main_handler.install_language(name_language)

        self.__update_language_title()
        self.__update_language_menu(
            old_main_menu_names, [_("Auth"), _("Language")], self.__main_menu
        )
        self.__update_language_menu(
            old_auth_menu_names,
            [
                _("Auth by password"),
                _("Auth by access token"),
                _("Delete a saved access token"),
            ],
            self.__auth_menu,
        )
        self.__update_language_main_components()
        self.__update_language_data()

    def __update_language_menu(
        self, old_main_menu_names: list[str], main_menu_names: list[str], menu: Menu
    ) -> None:
        """_sumChanging the menu languagemary_

        Args:
            old_main_menu_names (list[str]): Old names of menu items
            main_menu_names (list[str]): Changed names of menu items
            menu (Menu): Form Menu
        """
        for i in range(0, len(old_main_menu_names)):
            menu.entryconfigure(old_main_menu_names[i], label=main_menu_names[i])

    def __update_language_title(self) -> None:
        """Changing the form header language"""
        self.__root.title(_("Like photos in VK albums"))

    def __update_language_main_components(self) -> None:
        """Changing the language of the main components of the form"""
        self.__owner_title.set(_("Owners albums"))
        self.__owner_button.set(_("Show albums"))
        self.__albums_title.set(_("Albums"))
        self.__put_like.set(_("Put likes"))
        self.__remove_like.set(_("Remove likes"))

    def __update_language_data(self) -> None:
        """Changing the data language on the form"""
        try:
            self.__display_info_current_user()
            self.__display_owners_albums(self.__main_handler.get_owners_albums())

            if self.__last_select_owner is not None:
                self.__display_albums(
                    self.__main_handler.get_albums(self.__last_select_owner)
                )
        except (
            NoAuthException,
            GetCurrentUserException,
            GetFriendsException,
            GetAlbumsException,
        ) as e:
            messagebox.showinfo(_("The data was not received successfully"), f"{e}")

    def __display_owners_albums(self, owners: list[User]) -> None:
        """Displaying a list of album owners on the form

        Args:
            owners (list[User]): List of album owners
        """
        self.__owners_listbox.delete(0, self.__owners_listbox.size())

        for owner in owners:
            self.__owners_listbox.insert(END, owner.fullname())

    def __clear_list_albums(self) -> None:
        """Deleting data in the album list"""
        self.__albums_listbox.delete(0, self.__albums_listbox.size())

    def __display_info_current_user(self) -> None:
        """Displaying the authorized user's data on the form"""
        user = self.__main_handler.get_info_current_user()
        Label(text=user.fullname()).grid(row=0, column=5)

    def __display_albums(self, albums: list[Album]) -> None:
        """Displaying the selected user's album data on the form

        Args:
            albums (list[Album]): List of albums of the selected user
        """
        TITLE_PHOTO = _("Count photo")

        self.__clear_list_albums()
        for album in albums:
            self.__albums_listbox.insert(
                END, f"{album.title} - {TITLE_PHOTO}: {album.size}"
            )

    def __auth_success(self, *args) -> None:
        """Event handler for the destruction of authorization forms"""
        self.__main_menu.entryconfigure(_("Auth"), state="normal")
        self.__button_show_albums.config(state="normal")
        self.__button_put_likes.config(state="normal")
        self.__button_remove_likes.config(state="normal")
        try:
            if self.__main_handler.check_api():
                self.__display_info_current_user()
                self.__display_owners_albums(self.__main_handler.get_owners_albums())
                self.__clear_list_albums()
        except (NoAuthException, GetCurrentUserException, GetFriendsException) as e:
            messagebox.showinfo(_("The data was not received successfully"), f"{e}")

    def __show_albums(self) -> None:
        """Album display button handler"""
        self.__button_show_albums.config(state="disabled")
        selection = self.__owners_listbox.curselection()
        if len(selection) == 0:
            messagebox.showinfo(
                _("The owner of the albums is not selected"), _("Select one user")
            )
        else:
            self.__last_select_owner = selection[0]
            try:
                self.__display_albums(
                    self.__main_handler.get_albums(self.__last_select_owner)
                )
            except (NoAuthException, GetAlbumsException) as e:
                messagebox.showinfo(_("Albums not received"), f"{e}")
        self.__button_show_albums.config(state="normal")

    def __auth_by_password(self) -> None:
        """Password authorization button handler"""
        self.__main_menu.entryconfigure(_("Auth"), state="disabled")
        try:
            self.__main_handler.auth_by_access_token()
            self.__auth_success()
            messagebox.showinfo(
                _("Authorization successful"),
                _("You have successfully logged in using the saved token"),
            )
        except AuthTokenException:
            auth_form = AuthPasswordForm(self.__main_handler)
            auth_form.register_event_destroy(self.__auth_success)
            auth_form.run()

    def __auth_by_token(self) -> None:
        """Token authorization button handler"""
        self.__main_menu.entryconfigure(_("Auth"), state="disabled")
        try:
            self.__main_handler.auth_by_access_token()
            self.__auth_success()
            messagebox.showinfo(
                _("Authorization successful"),
                _("You have successfully logged in using the saved token"),
            )
        except AuthTokenException:
            auth_form = AuthTokenForm(self.__main_handler)
            auth_form.register_event_destroy(self.__auth_success)
            auth_form.run()

    def __delete_access_token(self) -> None:
        """Deleting a saved token from a file"""
        self.__main_handler.delete_saved_access_token()
        messagebox.showinfo(_("Token successfully deleted"), _("You can log in again"))

    def __put_likes(self) -> None:
        """The handler of the button to put likes to photos"""
        self.__event_cancel_liking = Event()
        self.__init_liking()
        selection = self.__albums_listbox.curselection()
        if len(selection) == 0:
            messagebox.showinfo(_("Albums is not selected"), _("Select one album"))
        else:
            try:
                self.__main_handler.put_likes(
                    selection[0],
                    self.__event_cancel_liking,
                    self.__display_progress,
                    self.__display_captcha,
                )
                if self.__event_cancel_liking.is_set():
                    messagebox.showinfo(
                        _("Cancel"), _("Operation canceled successfully")
                    )
                else:
                    messagebox.showinfo(
                        _("Likes have been successfully putted"),
                        _("All photos of the album are liked"),
                    )
            except (NoAuthException, GetPhotosException) as e:
                messagebox.showinfo(_("Photos not received"), f"{e}")
        self.finish_liking()

    def __remove_likes(self) -> None:
        """Handler of the remove likes to photos button"""
        self.__event_cancel_liking = Event()
        self.__init_liking()
        selection = self.__albums_listbox.curselection()
        if len(selection) == 0:
            messagebox.showinfo(_("Albums is not selected"), _("Select one album"))
        else:
            try:
                self.__main_handler.remove_likes(
                    selection[0],
                    self.__event_cancel_liking,
                    self.__display_progress,
                    self.__display_captcha,
                )
                if self.__event_cancel_liking.is_set():
                    messagebox.showinfo(
                        _("Cancel"), _("Operation canceled successfully")
                    )
                else:
                    messagebox.showinfo(
                        _("Likes have been successfully removed"),
                        _("All likes are removed from photos from the album"),
                    )
            except (NoAuthException, GetPhotosException) as e:
                messagebox.showinfo(_("Photos not received"), f"{e}")
        self.finish_liking()

    def __init_liking(self) -> None:
        """Initialization before operations with likes"""
        self.__button_put_likes.config(state="disabled")
        self.__button_remove_likes.config(state="disabled")
        self.__display_cancel_button()

    def finish_liking(self) -> None:
        """Changing form components after operations with likes"""
        self.__button_put_likes.config(state="normal")
        self.__button_remove_likes.config(state="normal")
        self.__cancel_liking_button.destroy()

    def __display_cancel_button(self) -> None:
        """Display on the form of the button to cancel the operation with likes"""
        self.__cancel_liking_button = Button(
            self.__root, text=_("Cancel"), command=self.__cancel_liking
        )
        self.__cancel_liking_button.grid(row=3, column=4)

    def __display_progress(
        self, count_execute: int, count_all: int, part: int, all_parts: int
    ) -> None:
        """Displaying the progress of adding likes or removing likes  on the form

        Args:
            count_execute (int)
            count_all (int)
        """
        begin_text = _("Progress")
        part_text = _("parts")
        count_text = _("count")
        Label(
            width=25,
            text="{0}: {1}/{2} {3};".format(begin_text, part, all_parts, part_text),
        ).grid(row=3, column=2)
        Label(
            width=25,
            text="{0}/{1} {2}".format(count_execute, count_all, count_text),
        ).grid(row=4, column=2)
        self.__root.update()

    def __display_captcha(self, captcha: Captcha, event: Event) -> None:
        """Captcha image display

        Args:
            captcha (Captcha)
            event (Event): Captcha recognition completion event
        """
        self.__event = event
        self.__captcha = captcha
        captcha_form = CaptchaForm(self.__main_handler, self.__captcha)
        captcha_form.register_event_destroy(self.__set_event)
        captcha_form.run()

    def __set_event(self, *args) -> None:
        """Set a captcha recognition completion event"""
        self.__event.set()

    def __cancel_liking(self) -> None:
        """Canceling the operation with likes"""
        self.__button_put_likes.config(state="normal")
        self.__button_remove_likes.config(state="normal")
        self.__cancel_liking_button.config(state="disabled")
        self.__event_cancel_liking.set()
        self.__cancel_liking_button.destroy()
