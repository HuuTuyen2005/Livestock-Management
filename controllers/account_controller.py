from views.account_view import AccountView
from services.account_service import AccountService
from auth.session import Session

class AccountController:
    def __init__(self):
        self.view = AccountView()
        self.service = AccountService()
        self.load_account_info()

    def load_account_info(self):
        user_id = Session.current_user["id"]
        info = self.service.get_account_info(user_id)
        if info:
            self.view.lbl_fullname.setText(info["fullname"])
            self.view.lbl_email.setText(info["email"])
            self.view.lbl_phone.setText(info["phone"])
            self.view.lbl_username.setText(info["username"])
