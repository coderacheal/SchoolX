import kivy
import sqlite3
import datetime
import src.exceptions.exceptions as exceptions
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRectangleFlatButton, MDFlatButton
# from kivy.metrics import dp
# from kivymd.uix.datatables import MDDataTable


class Expenditure(Screen):
    def spinner_clicked(self, value):
        self.ids.text = value
        return value

    def file_expense(self, obj):
        the_date = datetime.datetime.today()
        self.year = the_date.year
        self.date = the_date.replace(microsecond=0)
        self.month_nm = str(the_date.month)
        datetime_object = datetime.datetime.strptime(self.month_nm, "%m")
        self.month_name = datetime_object.strftime("%B")
        try:
            conn = sqlite3.connect("school.db")
            c = conn.cursor()

            c.execute("""INSERT INTO expenditure VALUES(:date, :year, :term, :purpose, :expenditure_amt,
                :purpose_description, :Authorised_by, :Signitory_1, :Signitory_2,
                :Signitory_3)""",
                      {
                          'date': self.date,
                          'year': self.year,
                          'term': self.ids.select_term_spinner.text,
                          'purpose': self.ids.purpose_of_expenditure_spinner.text,
                          'expenditure_amt': self.ids.expenditure_amt.text,
                          'purpose_description': self.ids.description_of_expense.text,
                          'Authorised_by': self.ids.authorised_by.text,
                          'Signitory_1': self.ids.first_signatory.text,
                          'Signitory_2': self.ids.second_signatory.text,
                          'Signitory_3': self.ids.third_signatory.text,

                      })
            c.execute(
                """INSERT INTO income_and_expenditure VALUES (:income, :expenditure, :p_l, :month,
                :term, :year)""",
                {
                    'income': 0,
                    'expenditure': self.ids.expenditure_amt.text,
                    'p_l': 0,
                    'month': self.month_name,
                    'term': self.ids.select_term_spinner.text,
                    'year': self.year, })
            if self.ids.purpose_of_expenditure_spinner.text == "Select Purpose":
                raise exceptions.EmptyFieldError
            elif self.ids.authorised_by.text == " " or self.ids.authorised_by.text == "":
                raise exceptions.AuthorizationError
            elif self.ids.first_signatory.text == " " or self.ids.first_signatory.text == "":
                raise exceptions.SignitoryError
            elif self.ids.expenditure_amt.text == " " or int(self.ids.expenditure_amt.text) <= 0 or self.ids.expenditure_amt.text == "":
                raise exceptions.NoAmountError

        except exceptions.AuthorizationError:
            self.authorization_error_dialog = MDDialog(
                title="Authorization required!",
                text="The 'Authorised by' field cannot be blank",
                radius=[40, 7, 40, 7],
                auto_dismiss=False,
                buttons=[
                    MDRectangleFlatButton(
                        text="OK", on_release=self.close_authorization_error_dialog,
                    ),
                ],
            )

            self.authorization_error_dialog.open()
        except exceptions.SignitoryError:
            self.authorization_error_dialog = MDDialog(
                title="Signitory required!",
                radius=[40, 7, 40, 7],
                text="At least one signitory is required",
                auto_dismiss=False,
                buttons=[
                    MDRectangleFlatButton(
                        text="OK", on_release=self.close_authorization_error_dialog,
                    ),
                ],
            )

            self.authorization_error_dialog.open()
        except exceptions.EmptyFieldError:
            self.no_purpose_dialog = MDDialog(
                title="Purpose required?",
                radius=[40, 7, 40, 7],
                auto_dismiss=False,
                text="You have to select a purpose for expenditure",
                buttons=[
                    MDRectangleFlatButton(
                        text="OK", on_release=self.close_no_purpose_dialog,
                    ),
                ],
            )

            self.no_purpose_dialog.open()
        except exceptions.NoAmountError:
            self.no_amt_dialog = MDDialog(
                title="Bad Transaction Alert!",
                radius=[40, 7, 40, 7],
                auto_dismiss=False,
                text="Amount cannot be less than or equal to 0",
                buttons=[
                    MDRectangleFlatButton(
                        text="OK", on_release=self.close_no_amt_dialog,
                    ),
                ],
            )

            self.no_amt_dialog.open()
        else:
            conn.commit()
            self.ids.purpose_of_expenditure_spinner.text = "Purpose"
            self.ids.expenditure_amt.text = ''
            self.ids.description_of_expense.text = ''
            self.ids.authorised_by.text = ''
            self.ids.first_signatory.text = ""
            self.ids.second_signatory.text = ''
            self.ids.third_signatory.text = ''
            self.ids.purpose_of_expenditure_spinner.background_color = .7, 0, 0, .9
        finally:
            conn.close()

    def close_no_amt_dialog(self, obj):
        self.no_amt_dialog.dismiss()

    def close_no_purpose_dialog(self, obj):
        self.no_purpose_dialog.dismiss()

    def close_authorization_error_dialog(self, obj):
        self.authorization_error_dialog.dismiss()

    def confirm_expense(self):
        self.successful_transaction_dialog = MDDialog(
            title="Confirmation?",
            radius=[40, 7, 40, 7],
            text=f"Are you sure you want to file {self.ids.purpose_of_expenditure_spinner.text} expense of GHC{self.ids.expenditure_amt.text}?",
            buttons=[

                MDRectangleFlatButton(
                    text="YES", on_release=self.file_expense, on_press=self.close_successful_transaction_dialog),
                MDRectangleFlatButton(
                    text="NO", on_press=self.close_successful_transaction_dialog),
            ],
        )

        self.successful_transaction_dialog.open()

    def close_successful_transaction_dialog(self, obj):
        self.successful_transaction_dialog.dismiss()

    def logout(self):
        self.empty_class_dialog = MDDialog(
            title="Logging out...",
            text="Are you sure you want to log out?",
            radius=[40, 7, 40, 7],
            buttons=[
                MDRectangleFlatButton(
                    text="YES", on_release=self.close_dialog_and_logout),
                MDFlatButton(
                    text="NO", on_release=self.close_dialog
                ),
            ],
        )
        self.empty_class_dialog.open()

    def close_dialog(self, obj):
        self.empty_class_dialog.dismiss()

    def close_dialog_and_logout(self, obj):
        self.empty_class_dialog.dismiss()
        self.manager.current = "log in"
