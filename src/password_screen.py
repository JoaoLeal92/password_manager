from tkinter import ttk, Frame, Label, Entry, Button, LEFT
from models.repositories.credentials_repository import CredentialsDatabase
from settings import CREDENTIALS_DB

import sys
sys.path.append("..")

from providers.password_hash_provider import PasswordHashProvider


class PasswordPage(Frame):
    def __init__(self, master=None):
        # Connects to the database
        self.conn = CredentialsDatabase('SQLITE', dbname=CREDENTIALS_DB)

        # Creates the hash provider instance
        self.hash_provider = PasswordHashProvider()

        Frame.__init__(self, master)

        # Create the tabs for the login screen
        self.tabControl = ttk.Notebook(master)
        self.tab1 = ttk.Frame(self.tabControl)
        self.tab2 = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tab1, text='Create credentials')
        self.tabControl.add(self.tab2, text='Registered credentials')
        self.tabControl.pack(expand=1, fill="both")

        # Create credentials screen ----------------------------------------
        # Header container
        self.create_credential_header_container = Frame(self.tab1)
        self.create_credential_header_container.pack()
        self.create_credential_header_container['pady'] = 10
        # Header Text
        self.create_credential_header = Label(self.create_credential_header_container, text='Cadastro de credenciais')
        self.create_credential_header.pack()

        # Credential name container
        self.register_credential_name_container = Frame(self.tab1)
        self.register_credential_name_container['pady'] = 10
        self.register_credential_name_container['padx'] = 10
        self.register_credential_name_container.pack()
        # Credential name input and label
        self.register_credential_name_label = Label(self.register_credential_name_container, text='Nome da credencial', width=20)
        self.register_credential_name_input = Entry(self.register_credential_name_container)
        self.register_credential_name_label.pack(side=LEFT)
        self.register_credential_name_input.pack()

        # Credential url container
        self.register_credential_url_container = Frame(self.tab1)
        self.register_credential_url_container['pady'] = 10
        self.register_credential_url_container['padx'] = 10
        self.register_credential_url_container.pack()
        # Credential url input and label
        self.register_credential_url_label = Label(self.register_credential_url_container, text='Url da credencial',
                                                   width=20)
        self.register_credential_url_input = Entry(self.register_credential_url_container)
        self.register_credential_url_label.pack(side=LEFT)
        self.register_credential_url_input.pack()

        # Password container
        self.register_credential_password_container = Frame(self.tab1)
        self.register_credential_password_container['pady'] = 10
        self.register_credential_password_container['padx'] = 10
        self.register_credential_password_container.pack()
        # Password input and label
        self.register_credential_password_label = Label(self.register_credential_password_container, text='Senha', width=20)
        self.register_credential_password_input = Entry(self.register_credential_password_container, show="*")
        self.register_credential_password_label.pack(side=LEFT)
        self.register_credential_password_input.pack()

        # Password container
        self.register_confirm_credential_password_container = Frame(self.tab1)
        self.register_confirm_credential_password_container['pady'] = 10
        self.register_confirm_credential_password_container['padx'] = 10
        self.register_confirm_credential_password_container.pack()
        # Password input and label
        self.register_confirm_credential_password_label = Label(self.register_confirm_credential_password_container,
                                                                text='Confirmar senha', width=20)
        self.register_confirm_credential_password_input = Entry(self.register_confirm_credential_password_container,
                                                                show="*")
        self.register_confirm_credential_password_label.pack(side=LEFT)
        self.register_confirm_credential_password_input.pack()

        # Submit button container
        self.register_submit_container = Frame(self.tab1)
        self.register_submit_container.pack()
        self.register_submit_container['pady'] = 10
        # Submit button
        self.register_submit_button = Button(self.register_submit_container)
        self.register_submit_button['text'] = 'Cadastrar credencial'
        self.register_submit_button['command'] = self.register_credential
        self.register_submit_button.pack()

        # Register message container
        self.register_message_container = Frame(self.tab1)
        self.register_message_container['pady'] = 10
        self.register_message_container['padx'] = 10
        self.register_message_container.pack()
        # Register message
        self.register_message = Label(self.register_message_container, text='')
        self.register_message.pack()

    def register_credential(self):
        credential_name = self.register_credential_name_input.get()
        credential_url = self.register_credential_url_input.get()
        credential_password = self.register_credential_password_input.get()
        credential_confirm_password = self.register_confirm_credential_password_input.get()

        if credential_password != credential_confirm_password:
            self.register_message['text'] = 'Password and password confirmation don\'t match'
            return None

        # Creates the password hash
        hashed_password = self.hash_provider.encrypt_password(credential_password)

        # Stores hash in database
        create_create_credential_message = self.conn.create_credential(credential_name=credential_name,
                                                                       credential_password=hashed_password,
                                                                       credential_url=credential_url)
        self.register_message['text'] = create_create_credential_message
