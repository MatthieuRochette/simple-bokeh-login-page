import panel as pn
import bokeh as bk
# Here I use panel to create the server because it makes the code easier to
# understand and faster to code, but it is essentially the same because
# Panel is based on Bokeh

from cryptography.hazmat.primitives.kdf.scrypt import Scrypt, InvalidKey
from cryptography.hazmat.backends import default_backend

class Login():
    """Class that creates a simple password protection to th dahsboard"""

    def __init__(self, pw_hashed, salt, callback, *cback_args, **cback_kwargs):
        """
        pw_hashed:  binary string
            This is the string that must be entered to access the dahsboard.
        salt:       binary string
            The salt used for the hashing process of the password
        callback:   function
            Function to call if the user enters the right password.
        cback_args: any
            the arguments for your callback function (e.g. "my_title")
        cback_kwargs:   any
            the named arguments for your callback function (e.g. name='Bob')
        """

        self.password = pw_hashed
        self.callback = callback
        self.cback_args = cback_args
        self.cback_kwargs = cback_kwargs
        self._backend = default_backend()
        self.salt = salt

        self.password_text = bk.models.Div(
            text="Enter the password then press OK")
        self.password_field = bk.models.widgets.inputs.PasswordInput()
        self.wrong_password_text = bk.models.Div(
            text="Wrong password. Try again.")

        self.confirm_button = bk.models.Button(label="OK",
            button_type="primary")
        self.confirm_button.on_click(self.verify_password)
        self.col = pn.Column(self.password_text, self.password_field,
            self.confirm_button)
        # If i did not use Panel, it would be like this:
        # self.col = bk.models.Column(self.password_text,
        #   self.password_field, self.confirm_button)

    def verify_password(self, *e):
        self.kdf = Scrypt(salt=self.salt, length=32,
            n=2**14, r=8, p=1, backend=self._backend)
        try:
            self.kdf.verify(str(self.password_field.value).encode(),
                           self.password)
            self.password_text.text = "Success"
            self.callback(*self.cback_args, **self.cback_kwargs)
        except InvalidKey:
            if self.wrong_password_text not in self.col:
                self.col.append(self.wrong_password_text)

def show_page_after_login():
    global page_container, succesful_login

    for i in page_container:
        page_container.remove(i)
    page_container.append(succesful_login)

succesful_login = bk.models.widgets.Div(text="Logged in !")

# password is:  'test' (without brackets)
login_page = Login(
    b'SX\xd3\x0f\x1c\x15\xbf\xbe4 \xad\x96\xc9\xe9&z^\xdfW\xccw\x00|\xff\xa0\xbb\x1c5\t\x15\x16l',
    b'\xf0\xb4\xe3"\xb3y\xa4\xb5\x14)P\xc6\xcc\x06\x94\xa4',
    show_page_after_login)

page_container = pn.Row(login_page.col)
page_container.servable()