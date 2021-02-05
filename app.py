from tkinter import *
from tkinter import ttk

# from db import create_connection
from password_hash_provider import PasswordHashProvider
from settings import USER_DB
from models.users import UserDatabase

class SampleApp(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.current_frames = []

        self._frame = None
        self.init_frame(Application)
        
    def init_frame(self, frame_class):
        new_frame = frame_class(self)
        self._frame = new_frame
        self.current_frames = self.winfo_children()
        self._frame.pack()
    
    def switch_frame(self, frame_class):
        """Destroys current frame and replaces it with a new one."""
        new_frame = frame_class(self)

        for child in self.winfo_children():
            if child in self.current_frames:
                child.destroy()

        self.current_frames = self.winfo_children()
        self._frame = new_frame
        self._frame.pack()


class Application(Frame):
    def __init__(self, master=None):
        # Connects to the database
        # self.conn = create_connection(USER_DB)
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
        self.password_input = Entry(self.password_container)
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
        self.register_user_label = Label(self.register_user_container, text='Usuário', width=10)
        self.register_user_input = Entry(self.register_user_container)
        self.register_user_label.pack(side=LEFT)
        self.register_user_input.pack()

        # Password container
        self.register_password_container = Frame(self.tab2)
        self.register_password_container['pady'] = 10
        self.register_password_container['padx'] = 10
        self.register_password_container.pack()
        # Password input and label
        self.register_password_label = Label(self.register_password_container, text='Senha', width=10)
        self.register_password_input = Entry(self.register_password_container)
        self.register_password_label.pack(side=LEFT)
        self.register_password_input.pack()

        # Password container
        self.register_confirm_password_container = Frame(self.tab2)
        self.register_confirm_password_container['pady'] = 10
        self.register_confirm_password_container['padx'] = 10
        self.register_confirm_password_container.pack()
        # Password input and label
        self.register_confirm_password_label = Label(self.register_confirm_password_container, text='Confirmar senha', width=10)
        self.register_confirm_password_input = Entry(self.register_confirm_password_container)
        self.register_confirm_password_label.pack(side=LEFT)
        self.register_confirm_password_input.pack()

        # Submit button
        self.register_submit_container = Frame(self.tab2)
        self.register_submit_container.pack()
        self.register_submit_container['pady'] = 10
        # Submit button
        self.register_submit_button = Button(self.register_submit_container)
        self.register_submit_button['text'] = 'Cadastrar'
        self.register_submit_button['command'] = self.register
        self.register_submit_button.pack()

    def login(self, master):
        user = self.user_input.get()
        password = self.password_input.get()

        if user == 'teste' and password == 'teste':
            print('logou')
            master.switch_frame(PasswordPage)
    
    def register(self):
        print('cadastro')
        # Check if password matches confirmation
        password = self.register_password_input.get()
        confirm_password = self.register_confirm_password_input.get()
        if password != confirm_password:
            print('Senha e confirmação não batem')
            return None

        # Creates the password hash
        hashed_password = self.hash_provider.encrypt_password(password)

        # Stores hash in database


class PasswordPage(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        # Header container
        self.header_container = Frame(master)
        self.header_container.pack()
        self.header_container['pady'] = 10
        # Header Text
        self.header = Label(self.header_container, text='Pagina das senhas')
        self.header.pack()
