from tkinter import Frame, Label, Entry, Button, LEFT
from tkinter import ttk

from settings import USER_DB
from models.repositories.users_repository import UserDatabase
from src.password_screen import PasswordPage

import sys
sys.path.append("..")

from providers.password_hash_provider import PasswordHashProvider


class LoginPage(Frame):
    def __init__(self, master=None):
        # Connects to the database
        self.conn = UserDatabase('SQLITE', dbname=USER_DB)

        # Creates the hash provider instance
        self.hash_provider = PasswordHashProvider()

        Frame.__init__(self, master)

        # Create the tabs for the login screen
        self.tabControl = ttk.Notebook(master)
        self.tab1 = ttk.Frame(self.tabControl)
        self.tab2 = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tab1, text='Login')
        self.tabControl.add(self.tab2, text='Cadastro')
        self.tabControl.pack(expand=1, fill="both")

        # LOGIN SCREEN -----------------------------------------
        # Header container
        self.header_container = Frame(self.tab1)
        self.header_container.pack()
        self.header_container['pady'] = 10
        # Header Text
        self.header = Label(self.header_container, text='Login')
        self.header.pack()

        # User name container
        self.user_container = Frame(self.tab1)
        self.user_container['pady'] = 10
        self.user_container['padx'] = 10
        self.user_container.pack()
        # User name input and label
        self.user_label = Label(self.user_container, text='Usuário', width=10)
        self.user_input = Entry(self.user_container)
        self.user_label.pack(side=LEFT)
        self.user_input.pack()

        # Password container
        self.password_container = Frame(self.tab1)
        self.password_container['pady'] = 10
        self.password_container['padx'] = 10
        self.password_container.pack()
        # Password input and label
        self.password_label = Label(self.password_container, text='Senha', width=10)
        self.password_input = Entry(self.password_container, show="*")
        self.password_label.pack(side=LEFT)
        self.password_input.pack()

        # Submit button
        self.submit_container = Frame(self.tab1)
        self.submit_container.pack()
        self.submit_container['pady'] = 10
        # Submit button
        self.submit_button = Button(self.submit_container)
        self.submit_button['text'] = 'Login'
        self.submit_button['command'] = lambda: self.login(master)
        self.submit_button.pack()

        # Login message container
        self.login_message_container = Frame(self.tab1)
        self.login_message_container['pady'] = 10
        self.login_message_container['padx'] = 10
        self.login_message_container.pack()
        # Login message
        self.login_message = Label(self.login_message_container, text='')
        self.login_message.pack()

        # REGISTER SCREEN -----------------------------------------
        # Header container
        self.register_header_container = Frame(self.tab2)
        self.register_header_container.pack()
        self.register_header_container['pady'] = 10
        # Header Text
        self.header = Label(self.register_header_container, text='Cadastro de usuário')
        self.header.pack()

        # User name container
        self.register_user_container = Frame(self.tab2)
        self.register_user_container['pady'] = 10
        self.register_user_container['padx'] = 10
        self.register_user_container.pack()
        # User name input and label
        self.register_user_label = Label(self.register_user_container, text='Usuário', width=20)
        self.register_user_input = Entry(self.register_user_container)
        self.register_user_label.pack(side=LEFT)
        self.register_user_input.pack()

        # Password container
        self.register_password_container = Frame(self.tab2)
        self.register_password_container['pady'] = 10
        self.register_password_container['padx'] = 10
        self.register_password_container.pack()
        # Password input and label
        self.register_password_label = Label(self.register_password_container, text='Senha', width=20)
        self.register_password_input = Entry(self.register_password_container, show="*")
        self.register_password_label.pack(side=LEFT)
        self.register_password_input.pack()

        # Password container
        self.register_confirm_password_container = Frame(self.tab2)
        self.register_confirm_password_container['pady'] = 10
        self.register_confirm_password_container['padx'] = 10
        self.register_confirm_password_container.pack()
        # Password input and label
        self.register_confirm_password_label = Label(self.register_confirm_password_container, text='Confirmar senha',
                                                     width=20)
        self.register_confirm_password_input = Entry(self.register_confirm_password_container, show="*")
        self.register_confirm_password_label.pack(side=LEFT)
        self.register_confirm_password_input.pack()

        # Submit button container
        self.register_submit_container = Frame(self.tab2)
        self.register_submit_container.pack()
        self.register_submit_container['pady'] = 10
        # Submit button
        self.register_submit_button = Button(self.register_submit_container)
        self.register_submit_button['text'] = 'Cadastrar'
        self.register_submit_button['command'] = self.register
        self.register_submit_button.pack()

        # Register message container
        self.register_message_container = Frame(self.tab2)
        self.register_message_container['pady'] = 10
        self.register_message_container['padx'] = 10
        self.register_message_container.pack()
        # Register message
        self.register_message = Label(self.register_message_container, text='')
        self.register_message.pack()

    def login(self, master):
        user = self.user_input.get()
        password = self.password_input.get()

        user = self.conn.get_user_by_name(username=user)

        if not user:
            self.login_message['text'] = 'User not found'
            return

        check_password_match = self.hash_provider.check_encrypted_password(password=password, hashed=user.password)

        if check_password_match:
            master.switch_frame(PasswordPage)
        else:
            self.login_message['text'] = 'Wrong user password'

    def register(self):
        # Check if password matches confirmation
        username = self.register_user_input.get()
        password = self.register_password_input.get()
        confirm_password = self.register_confirm_password_input.get()
        if password != confirm_password:
            self.register_message['text'] = 'Password and password confirmation don\'t match'
            return None

        # Creates the password hash
        hashed_password = self.hash_provider.encrypt_password(password)

        # Stores hash in database
        create_user_message = self.conn.create_user(username=username, password=hashed_password)
        self.register_message['text'] = create_user_message
