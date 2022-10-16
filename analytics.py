# import kivy
import sqlite3
# import datetime
from exceptions import EmptyClassSpinnerError
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRectangleFlatButton, MDFlatButton
from kivy.metrics import dp
from kivymd.uix.datatables import MDDataTable
# from kivymd.uix.picker import MDDatePicker
#import numpy as np
import matplotlib.pyplot as plt


class Analytics(Screen):
    def logout(self):
        self.empty_class_dialog = MDDialog(
            title="Logging out...",
            text="Are you sure you want to log out?",
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


class Figures(Screen):
    table = None
    conn = sqlite3.connect("school.db")
    c = conn.cursor()
    values = [r[0]
              for r in c.execute("SELECT available_years FROM years")]
    years = values

    def get_table(self):
        conn = sqlite3.connect("school.db")
        c = conn.cursor()
        c.execute(
            """UPDATE income_and_expenditure SET p_l = income - expenditure""")
        conn.commit()
        jan = c.execute("""UPDATE income_and_expenditure_previews
                SET
                income_preview = SUM(income),
                expenditure_preview = SUM(expenditure),
                p_l_preview = SUM(p_l),
                term_preview = term,
                year_preview  = year,
                month_preview = month
                FROM income_and_expenditure
                WHERE income_and_expenditure.year =?
                AND income_and_expenditure.month = 'January'
                AND income_and_expenditure_previews.month_preview = 'January'""",
                        (self.ids.select_year_spinner.text,))
        feb = c.execute("""UPDATE income_and_expenditure_previews
                SET
                income_preview = SUM(income),
                expenditure_preview = SUM(expenditure),
                p_l_preview = SUM(p_l),
                term_preview = term,
                year_preview  = year,
                month_preview = month
                FROM income_and_expenditure
                WHERE income_and_expenditure.year =?
                AND income_and_expenditure.month = 'February'
                AND income_and_expenditure_previews.month_preview = 'February'""",
                        (self.ids.select_year_spinner.text,))
        mar = c.execute("""UPDATE income_and_expenditure_previews
                SET
                income_preview = SUM(income),
                expenditure_preview = SUM(expenditure),
                p_l_preview = SUM(p_l),
                term_preview = term,
                year_preview  = year,
                month_preview = month
                FROM income_and_expenditure
                WHERE income_and_expenditure.year =?
                AND income_and_expenditure.month = 'March'
                AND income_and_expenditure_previews.month_preview = 'March'""",
                        (self.ids.select_year_spinner.text,))
        apr = c.execute("""UPDATE income_and_expenditure_previews
                SET
                income_preview = SUM(income),
                expenditure_preview = SUM(expenditure),
                p_l_preview = SUM(p_l),
                term_preview = term,
                year_preview  = year,
                month_preview = month
                FROM income_and_expenditure
                WHERE income_and_expenditure.year =?
                AND income_and_expenditure.month = 'April'
                AND income_and_expenditure_previews.month_preview = 'April'""",
                        (self.ids.select_year_spinner.text,))
        may = c.execute("""UPDATE income_and_expenditure_previews
                SET
                income_preview = SUM(income),
                expenditure_preview = SUM(expenditure),
                p_l_preview = SUM(p_l),
                term_preview = term,
                year_preview  = year,
                month_preview = month
                FROM income_and_expenditure
                WHERE income_and_expenditure.year =?
                AND income_and_expenditure.month = 'May'
                AND income_and_expenditure_previews.month_preview = 'May'""",
                        (self.ids.select_year_spinner.text,))
        june = c.execute("""UPDATE income_and_expenditure_previews
                SET
                income_preview = SUM(income),
                expenditure_preview = SUM(expenditure),
                p_l_preview = SUM(p_l),
                term_preview = term,
                year_preview  = year,
                month_preview = month
                FROM income_and_expenditure
                WHERE income_and_expenditure.year =?
                AND income_and_expenditure.month = 'June'
                AND income_and_expenditure_previews.month_preview = 'June'""",
                         (self.ids.select_year_spinner.text,))
        july = c.execute("""UPDATE income_and_expenditure_previews
                SET
                income_preview = SUM(income),
                expenditure_preview = SUM(expenditure),
                p_l_preview = SUM(p_l),
                term_preview = term,
                year_preview  = year,
                month_preview = month
                FROM income_and_expenditure
                WHERE income_and_expenditure.year =?
                AND income_and_expenditure.month = 'July'
                AND income_and_expenditure_previews.month_preview = 'July'""",
                         (self.ids.select_year_spinner.text,))
        august = c.execute("""UPDATE income_and_expenditure_previews
                SET
                income_preview = SUM(income),
                expenditure_preview = SUM(expenditure),
                p_l_preview = SUM(p_l),
                term_preview = term,
                year_preview  = year,
                month_preview = month
                FROM income_and_expenditure
                WHERE income_and_expenditure.year =?
                AND income_and_expenditure.month = 'August'
                AND income_and_expenditure_previews.month_preview = 'August'""",
                           (self.ids.select_year_spinner.text,))
        sep = c.execute("""UPDATE income_and_expenditure_previews
                SET
                income_preview = SUM(income),
                expenditure_preview = SUM(expenditure),
                p_l_preview = SUM(p_l),
                term_preview = term,
                year_preview  = year,
                month_preview = month
                FROM income_and_expenditure
                WHERE income_and_expenditure.year =?
                AND income_and_expenditure.month = 'September'
                AND income_and_expenditure_previews.month_preview = 'September'""",
                        (self.ids.select_year_spinner.text,))
        october = c.execute("""UPDATE income_and_expenditure_previews
                SET
                income_preview = SUM(income),
                expenditure_preview = SUM(expenditure),
                p_l_preview = SUM(p_l),
                term_preview = term,
                year_preview  = year,
                month_preview = month
                FROM income_and_expenditure
                WHERE income_and_expenditure.year =?
                AND income_and_expenditure.month = 'october'
                AND income_and_expenditure_previews.month_preview = 'october'""",
                            (self.ids.select_year_spinner.text,))
        nov = c.execute("""UPDATE income_and_expenditure_previews
                SET
                income_preview = SUM(income),
                expenditure_preview = SUM(expenditure),
                p_l_preview = SUM(p_l),
                term_preview = term,
                year_preview  = year,
                month_preview = month
                FROM income_and_expenditure
                WHERE income_and_expenditure.year =?
                AND income_and_expenditure.month = 'November'
                AND income_and_expenditure_previews.month_preview = 'November'""",
                        (self.ids.select_year_spinner.text,))
        dec = c.execute("""UPDATE income_and_expenditure_previews
                SET
                income_preview = SUM(income),
                expenditure_preview = SUM(expenditure),
                p_l_preview = SUM(p_l),
                term_preview = term,
                year_preview  = year,
                month_preview = month
                FROM income_and_expenditure
                WHERE income_and_expenditure.year =?
                AND income_and_expenditure.month = 'December'
                AND income_and_expenditure_previews.month_preview = 'December'""",
                        (self.ids.select_year_spinner.text,))
        conn.commit()
        if self.ids.select_term_spinner.text == "Yearly":
            try:
                if self.ids.select_year_spinner.text == "Select Year":
                    raise EmptyClassSpinnerError
                if self.ids.select_term_spinner.text == "Select Term":
                    raise EmptyClassSpinnerError

                data = [r[0:6] for r in c.execute("""SELECT year_preview, term_preview, month_preview,
                        income_preview, expenditure_preview, p_l_preview
                        FROM income_and_expenditure_previews""",)]

                spaces = [(" ", " ", " ", " ", " ", ""), ]
                values = data + spaces

                if not self.table:
                    self.table = MDDataTable(
                        size_hint=(0.8, 0.5),
                        size=(400, 300),
                        pos_hint={"center_x": .5, "center_y": .5},
                        use_pagination=True,
                        column_data=[
                            ('Year', dp(20)),
                            ('Term', dp(25)),
                            ('Month', dp(25)),
                            ("Income", dp(25)),
                            ('Expenditure', dp(25)),
                            ('Surplus/Loss', dp(30)),

                        ],
                        rows_num=9,
                    )
                    self.table.row_data = values
                    self.ids.box.add_widget(self.table)

                if not not self.table:
                    self.table.row_data = values

            except EmptyClassSpinnerError:
                self.empty_spinner_dialog = MDDialog(
                    title="Warning!",
                    text="Please select the year and term to proceed",
                    radius=[40, 7, 40, 7],
                    auto_dismiss=False,
                    buttons=[
                        MDRectangleFlatButton(
                            text="CLOSE", on_release=self.close_empty_spinner_dialog
                        ),

                    ],
                )
                self.empty_spinner_dialog.open()

        else:
            # self.ids.select_term_spinner.text == "First Term":
            try:
                if self.ids.select_year_spinner.text == "Select Year":
                    raise EmptyClassSpinnerError
                if self.ids.select_term_spinner.text == "Select Term":
                    raise EmptyClassSpinnerError

                data = [r[0:6] for r in c.execute("""SELECT year_preview, term_preview, month_preview,
                        income_preview, expenditure_preview, p_l_preview
                        FROM income_and_expenditure_previews
                        WHERE income_and_expenditure_previews.term_preview =?
                        AND income_and_expenditure_previews.year_preview = ?""",
                                                  (self.ids.select_term_spinner.text, self.ids.select_year_spinner,))]
                print(data)
                spaces = [(" ", " ", " ", " ", " ", ""), ]
                values = data + spaces
                if not self.table:
                    self.table = MDDataTable(
                        size_hint=(0.8, 0.5),
                        size=(400, 300),
                        pos_hint={"center_x": .5, "center_y": .5},
                        use_pagination=True,
                        column_data=[
                            ('Year', dp(20)),
                            ('Term', dp(25)),
                            ('Month', dp(25)),
                            ("Income", dp(25)),
                            ('Expenditure', dp(25)),
                            ('Surplus/Loss', dp(30)),

                        ],
                        rows_num=9,
                    )
                    self.table.row_data = values
                    self.ids.box.add_widget(self.table)

                if not not self.table:
                    self.table.row_data = values
            except EmptyClassSpinnerError:
                self.empty_spinner_dialog = MDDialog(
                    title="Warning!",
                    text="Please select the year and term to proceed",
                    radius=[40, 7, 40, 7],
                    auto_dismiss=False,
                    buttons=[
                        MDRectangleFlatButton(
                            text="CLOSE", on_release=self.close_empty_spinner_dialog
                        ),

                    ],
                )
                self.empty_spinner_dialog.open()

        # elif self.ids.select_term_spinner.text == "Second Term":
        #     try:
        #         if self.ids.select_year_spinner.text == "Select Year":
        #             raise EmptyClassSpinnerError
        #         if self.ids.select_term_spinner.text == "Select Term":
        #             raise EmptyClassSpinnerError

        #         data = [r[0:6] for r in c.execute("""SELECT year_preview, term_preview, month_preview,
        #                 income_preview, expenditure_preview, p_l_preview
        #                 FROM income_and_expenditure_previews
        #                 WHERE income_and_expenditure_previews.term_preview =?
        #                 AND income_and_expenditure_previews.year_preview = ?""",
        #                                           (self.ids.select_term_spinner.text, self.ids.select_year_spinner))]

        #         spaces = [(" ", " ", " ", " ", " ", ""), ]
        #         values = data + spaces
        #         if not self.table:
        #             self.table = MDDataTable(
        #                 size_hint=(0.8, 0.5),
        #                 size=(400, 300),
        #                 pos_hint={"center_x": .5, "center_y": .5},
        #                 use_pagination=True,
        #                 column_data=[
        #                     ('Year', dp(20)),
        #                     ('Term', dp(25)),
        #                     ('Month', dp(25)),
        #                     ("Income", dp(25)),
        #                     ('Expenditure', dp(25)),
        #                     ('Surplus/Loss', dp(30)),

        #                 ],
        #                 rows_num=9,
        #             )
        #             self.table.row_data = values
        #             self.ids.box.add_widget(self.table)

        #         if not not self.table:
        #             self.table.row_data = values
        #     except EmptyClassSpinnerError:
        #         self.empty_spinner_dialog = MDDialog(
        #             title="Warning!",
        #             text="Please select the year and term to proceed",
        #             radius=[40, 7, 40, 7],
        #             auto_dismiss=False,
        #             buttons=[
        #                 MDRectangleFlatButton(
        #                     text="CLOSE", on_release=self.close_empty_spinner_dialog
        #                 ),

        #             ],
        #         )
        #         self.empty_spinner_dialog.open()
        # elif self.ids.select_term_spinner.text == "Third Term":
        #     try:
        #         if self.ids.select_year_spinner.text == "Select Year":
        #             raise EmptyClassSpinnerError
        #         if self.ids.select_term_spinner.text == "Select Term":
        #             raise EmptyClassSpinnerError

        #         data = [r[0:6] for r in c.execute("""SELECT year_preview, term_preview, month_preview,
        #                 income_preview, expenditure_preview, p_l_preview
        #                 FROM income_and_expenditure_previews
        #                 WHERE income_and_expenditure_previews.term_preview =?
        #                 AND income_and_expenditure_previews.year_preview = ?""",
        #                                           (self.ids.select_term_spinner.text, self.ids.select_year_spinner))]

        #         spaces = [(" ", " ", " ", " ", " ", ""), ]
        #         values = data + spaces
        #         if not self.table:
        #             self.table = MDDataTable(
        #                 size_hint=(0.8, 0.5),
        #                 size=(400, 300),
        #                 pos_hint={"center_x": .5, "center_y": .5},
        #                 use_pagination=True,
        #                 column_data=[
        #                     ('Year', dp(20)),
        #                     ('Term', dp(25)),
        #                     ('Month', dp(25)),
        #                     ("Income", dp(25)),
        #                     ('Expenditure', dp(25)),
        #                     ('Surplus/Loss', dp(30)),

        #                 ],
        #                 rows_num=9,
        #             )
        #             self.table.row_data = values
        #             self.ids.box.add_widget(self.table)

        #         if not not self.table:
        #             self.table.row_data = values
        #     except EmptyClassSpinnerError:
        #         self.empty_spinner_dialog = MDDialog(
        #             title="Warning!",
        #             text="Please select the year and term to proceed",
        #             radius=[40, 7, 40, 7],
        #             auto_dismiss=False,
        #             buttons=[
        #                 MDRectangleFlatButton(
        #                     text="CLOSE", on_release=self.close_empty_spinner_dialog
        #                 ),

        #             ],
        #         )
        #         self.empty_spinner_dialog.open()

    def close_empty_spinner_dialog(self, obj):
        self.empty_spinner_dialog.dismiss()

    def spinner_clicked(self, value):
        self.ids.text = value
        return value

    def logout(self):
        self.empty_class_dialog = MDDialog(
            title="Logging out...",
            text="Are you sure you want to log out?",
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


class Graphs(Screen):
    conn = sqlite3.connect("school.db")
    c = conn.cursor()
    values = [r[0]
              for r in c.execute("SELECT available_years FROM years")]
    years = values

    def get_income_and_expenditure_graph(self):
        conn = sqlite3.connect("school.db")
        c = conn.cursor()
        p_l = c.execute(
            """UPDATE income_and_expenditure SET p_l = income - expenditure""")
        jan = c.execute("""UPDATE income_and_expenditure_previews
                    SET
                    income_preview = SUM(income),
                    expenditure_preview = SUM(expenditure),
                    p_l_preview = SUM(p_l),
                    term_preview = term,
                    year_preview  = year,
                    month_preview = month
                    FROM income_and_expenditure
                    WHERE income_and_expenditure.year =?
                    AND income_and_expenditure.month = 'January'
                    AND income_and_expenditure_previews.month_preview = 'January'""",
                        (self.ids.select_year_spinner.text,))
        feb = c.execute("""UPDATE income_and_expenditure_previews
                SET
                income_preview = SUM(income),
                expenditure_preview = SUM(expenditure),
                p_l_preview = SUM(p_l),
                term_preview = term,
                year_preview  = year,
                month_preview = month
                FROM income_and_expenditure
                WHERE income_and_expenditure.year =?
                AND income_and_expenditure.month = 'February'
                AND income_and_expenditure_previews.month_preview = 'February'""",
                        (self.ids.select_year_spinner.text,))
        mar = c.execute("""UPDATE income_and_expenditure_previews
                SET
                income_preview = SUM(income),
                expenditure_preview = SUM(expenditure),
                p_l_preview = SUM(p_l),
                term_preview = term,
                year_preview  = year,
                month_preview = month
                FROM income_and_expenditure
                WHERE income_and_expenditure.year =?
                AND income_and_expenditure.month = 'March'
                AND income_and_expenditure_previews.month_preview = 'March'""",
                        (self.ids.select_year_spinner.text,))
        apr = c.execute("""UPDATE income_and_expenditure_previews
                SET
                income_preview = SUM(income),
                expenditure_preview = SUM(expenditure),
                p_l_preview = SUM(p_l),
                term_preview = term,
                year_preview  = year,
                month_preview = month
                FROM income_and_expenditure
                WHERE income_and_expenditure.year =?
                AND income_and_expenditure.month = 'April'
                AND income_and_expenditure_previews.month_preview = 'April'""",
                        (self.ids.select_year_spinner.text,))
        may = c.execute("""UPDATE income_and_expenditure_previews
                SET
                income_preview = SUM(income),
                expenditure_preview = SUM(expenditure),
                p_l_preview = SUM(p_l),
                term_preview = term,
                year_preview  = year,
                month_preview = month
                FROM income_and_expenditure
                WHERE income_and_expenditure.year =?
                AND income_and_expenditure.month = 'May'
                AND income_and_expenditure_previews.month_preview = 'May'""",
                        (self.ids.select_year_spinner.text,))
        june = c.execute("""UPDATE income_and_expenditure_previews
                SET
                income_preview = SUM(income),
                expenditure_preview = SUM(expenditure),
                p_l_preview = SUM(p_l),
                term_preview = term,
                year_preview  = year,
                month_preview = month
                FROM income_and_expenditure
                WHERE income_and_expenditure.year =?
                AND income_and_expenditure.month = 'June'
                AND income_and_expenditure_previews.month_preview = 'June'""",
                         (self.ids.select_year_spinner.text,))
        july = c.execute("""UPDATE income_and_expenditure_previews
                SET
                income_preview = SUM(income),
                expenditure_preview = SUM(expenditure),
                p_l_preview = SUM(p_l),
                term_preview = term,
                year_preview  = year,
                month_preview = month
                FROM income_and_expenditure
                WHERE income_and_expenditure.year =?
                AND income_and_expenditure.month = 'July'
                AND income_and_expenditure_previews.month_preview = 'July'""",
                         (self.ids.select_year_spinner.text,))
        august = c.execute("""UPDATE income_and_expenditure_previews
                SET
                income_preview = SUM(income),
                expenditure_preview = SUM(expenditure),
                p_l_preview = SUM(p_l),
                term_preview = term,
                year_preview  = year,
                month_preview = month
                FROM income_and_expenditure
                WHERE income_and_expenditure.year =?
                AND income_and_expenditure.month = 'August'
                AND income_and_expenditure_previews.month_preview = 'August'""",
                           (self.ids.select_year_spinner.text,))
        sep = c.execute("""UPDATE income_and_expenditure_previews
                SET
                income_preview = SUM(income),
                expenditure_preview = SUM(expenditure),
                p_l_preview = SUM(p_l),
                term_preview = term,
                year_preview  = year,
                month_preview = month
                FROM income_and_expenditure
                WHERE income_and_expenditure.year =?
                AND income_and_expenditure.month = 'September'
                AND income_and_expenditure_previews.month_preview = 'September'""",
                        (self.ids.select_year_spinner.text,))
        october = c.execute("""UPDATE income_and_expenditure_previews
                SET
                income_preview = SUM(income),
                expenditure_preview = SUM(expenditure),
                p_l_preview = SUM(p_l),
                term_preview = term,
                year_preview  = year,
                month_preview = month
                FROM income_and_expenditure
                WHERE income_and_expenditure.year =?
                AND income_and_expenditure.month = 'october'
                AND income_and_expenditure_previews.month_preview = 'october'""",
                            (self.ids.select_year_spinner.text,))
        nov = c.execute("""UPDATE income_and_expenditure_previews
                SET
                income_preview = SUM(income),
                expenditure_preview = SUM(expenditure),
                p_l_preview = SUM(p_l),
                term_preview = term,
                year_preview  = year,
                month_preview = month
                FROM income_and_expenditure
                WHERE income_and_expenditure.year =?
                AND income_and_expenditure.month = 'November'
                AND income_and_expenditure_previews.month_preview = 'November'""",
                        (self.ids.select_year_spinner.text,))
        dec = c.execute("""UPDATE income_and_expenditure_previews
                SET
                income_preview = SUM(income),
                expenditure_preview = SUM(expenditure),
                p_l_preview = SUM(p_l),
                term_preview = term,
                year_preview  = year,
                month_preview = month
                FROM income_and_expenditure
                WHERE income_and_expenditure.year =?
                AND income_and_expenditure.month = 'December'
                AND income_and_expenditure_previews.month_preview = 'December'""",
                        (self.ids.select_year_spinner.text,))
        conn.commit()
        if self.ids.select_data_type_spinner.text == "Bar Chart":
            if self.ids.select_term_spinner.text == "Yearly":
                try:
                    months = [r[0] for r in c.execute(
                        """SELECT months FROM months""",)]
                    months_position = np.arange(len(months))
                    income = [r[0] for r in c.execute("""SELECT income_preview
                                FROM income_and_expenditure_previews
                                WHERE income_and_expenditure_previews.year_preview =?""", (self.ids.select_year_spinner.text,))]
                    expenditure = [r[0] for r in c.execute("""SELECT expenditure_preview
                                FROM income_and_expenditure_previews
                                WHERE income_and_expenditure_previews.year_preview =?""", (self.ids.select_year_spinner.text,))]
                    # print(income)
                    # print(expenditure)
                    # print(len(income))
                    if len(income) != 12 and len(expenditure) != 12:
                        raise ValueError
                    plt.xlabel("Months")
                    plt.ylabel("Amount in GHC")
                    plt.bar(months_position-0.2,  income,
                            width=0.4, label="Income")
                    plt.bar(months_position+0.2,  expenditure,
                            width=0.4, label="Expenditure")
                    plt.xticks(months_position, months)
                    plt.style.use("seaborn")
                    plt.legend()
                    plt.tight_layout()
                    plt.title(
                        f"{self.ids.select_year_spinner.text} Academic Calender - Yearly Income & Exenditure Analysis")
                    plt.show()
                except ValueError:
                    self.empty_class_dialog = MDDialog(
                        title="Empty!",
                        text="Complete data for the selected timeline does not exit yet",
                        radius=[40, 7, 40, 7],
                        auto_dismiss=False,
                        buttons=[
                            MDRectangleFlatButton(
                                text="CLOSE", on_release=self.close_empty_class_dialog
                            ),
                        ],
                    )
                    self.empty_class_dialog.open()

            else:
                try:
                    months = [r[0] for r in c.execute(
                        """SELECT months FROM months WHERE months.month_term = ?""", (self.ids.select_term_spinner.text,))]
                    months_position = np.arange(len(months))
                    income = [r[0] for r in c.execute("""SELECT income_preview
                                FROM income_and_expenditure_previews
                                WHERE income_and_expenditure_previews.year_preview =?
                                AND income_and_expenditure_previews.term_preview = ?""",
                                                      (self.ids.select_year_spinner.text, self.ids.select_term_spinner.text,))]
                    expenditure = [r[0] for r in c.execute("""SELECT expenditure_preview
                                FROM income_and_expenditure_previews
                                WHERE income_and_expenditure_previews.year_preview =?
                                AND income_and_expenditure_previews.term_preview = ?""",
                                                           (self.ids.select_year_spinner.text, self.ids.select_term_spinner.text,))]
                    if len(income) != 4 and len(expenditure) != 4:
                        raise ValueError

                    plt.xlabel("Months")
                    plt.ylabel("Amount in GHC")
                    plt.bar(months_position-0.2,  income,
                            width=0.4, label="Income")
                    plt.bar(months_position+0.2,  expenditure,
                            width=0.4, label="Expenditure")
                    plt.xticks(months_position, months)
                    plt.style.use("seaborn")
                    plt.legend()
                    plt.tight_layout()
                    plt.title(
                        f"{self.ids.select_term_spinner.text} Income & Expenditure Analysis - {self.ids.select_year_spinner.text}")
                    plt.show()

                except ValueError:
                    self.empty_class_dialog = MDDialog(
                        title="Empty!",
                        text="Complete data for the selected timeline does not exit yet",
                        radius=[40, 7, 40, 7],
                        auto_dismiss=False,
                        buttons=[
                            MDRectangleFlatButton(
                                text="CLOSE", on_release=self.close_empty_class_dialog
                            ),
                        ],
                    )
                    self.empty_class_dialog.open()
        elif self.ids.select_data_type_spinner.text == "Pie Chart":
            if self.ids.select_term_spinner.text == "Yearly":
                try:
                    conn = sqlite3.connect("school.db")
                    c = conn.cursor()
                    p_l = c.execute(
                        """UPDATE income_and_expenditure SET p_l = income - expenditure""")
                    conn.commit()
                    income = [r[0] for r in c.execute("""SELECT SUM(income_preview)
                                FROM income_and_expenditure_previews
                                WHERE income_and_expenditure_previews.year_preview =?""",
                                                      (self.ids.select_year_spinner.text, ))]
                    expenditure = [r[0] for r in c.execute("""SELECT SUM(expenditure_preview)
                                FROM income_and_expenditure_previews
                                WHERE income_and_expenditure_previews.year_preview =?""",
                                                           (self.ids.select_year_spinner.text,))]
                    slices = [income, expenditure]
                    labels = ("Income", "Expenditure")
                    explode = (0.02, 0)
                    plt.pie(slices, labels=labels, autopct='%.2f%%',
                            explode=explode, shadow=True, startangle=270)
                    plt.title(
                        f"{self.ids.select_year_spinner.text} Academic Calender - Yearly Income & Exenditure Analysis")
                    plt.style.use('ggplot')
                    plt.axis('equal')
                    plt.tight_layout()
                    plt.legend(loc='upper left')
                    plt.show()
                    print(income)
                    print(expenditure)
                except ValueError:
                    self.empty_class_dialog = MDDialog(
                        title="Empty!",
                        text="Complete data for the selected timeline does not exit yet",
                        radius=[40, 7, 40, 7],
                        auto_dismiss=False,
                        buttons=[
                            MDRectangleFlatButton(
                                text="CLOSE", on_release=self.close_empty_class_dialog
                            ),
                        ],
                    )
                    self.empty_class_dialog.open()
            else:
                try:
                    # conn = sqlite3.connect("school.db")
                    # c = conn.cursor()
                    # p_l = c.execute(
                    #     """UPDATE income_and_expenditure SET p_l = income - expenditure""")
                    # conn.commit()
                    income = [r[0] for r in c.execute("""SELECT SUM(income_preview)
                                FROM income_and_expenditure_previews
                                WHERE income_and_expenditure_previews.year_preview =?
                                AND income_and_expenditure_previews.term_preview = ?""",
                                                      (self.ids.select_year_spinner.text, self.ids.select_term_spinner.text,))]
                    expenditure = [r[0] for r in c.execute("""SELECT SUM(expenditure_preview)
                                FROM income_and_expenditure_previews
                                WHERE income_and_expenditure_previews.year_preview =?
                                AND income_and_expenditure_previews.term_preview = ?""",
                                                           (self.ids.select_year_spinner.text, self.ids.select_term_spinner.text,))]
                    # print(income)
                    # print(expenditure)
                    slices = [income, expenditure]
                    labels = ("Income", "Expenditure")
                    explode = (0.02, 0)
                    plt.pie(slices, labels=labels, autopct='%.2f%%',
                            explode=explode, shadow=True, startangle=270)
                    plt.title(
                        f"{self.ids.select_term_spinner.text} Income & Expenditure Analysis - {self.ids.select_year_spinner.text}")
                    plt.style.use('ggplot')
                    plt.axis('equal')
                    plt.tight_layout()
                    plt.legend(loc='upper left')
                    plt.show()
                except ValueError:
                    self.empty_class_dialog = MDDialog(
                        title="Error",
                        text="Complete data for the selected timeline does not exit yet",
                        radius=[25, 7, 25, 7],
                        auto_dismiss=False,
                        buttons=[
                            MDRectangleFlatButton(
                                text="CLOSE", on_release=self.close_empty_class_dialog
                            ),
                        ],
                    )
                    self.empty_class_dialog.open()
        elif self.ids.select_data_type_spinner.text == "Donut Chart":
            if self.ids.select_term_spinner.text == "Yearly":
                try:
                    # conn = sqlite3.connect("school.db")
                    # c = conn.cursor()
                    # p_l = c.execute(
                    #     """UPDATE income_and_expenditure SET p_l = income - expenditure""")
                    # conn.commit()
                    income = [r[0] for r in c.execute("""SELECT SUM(income_preview)
                                FROM income_and_expenditure_previews
                                WHERE income_and_expenditure_previews.year_preview =?""",
                                                      (self.ids.select_year_spinner.text,))]
                    expenditure = [r[0] for r in c.execute("""SELECT SUM(expenditure_preview)
                                FROM income_and_expenditure_previews
                                WHERE income_and_expenditure_previews.year_preview =?""",
                                                           (self.ids.select_year_spinner.text, ))]

                    slices = [income, expenditure]
                    labels = ["Income", "Expenditure"]
                    plt.pie(slices, labels=labels, autopct='%.2f%%',
                            shadow=True, startangle=270)
                    plt.title(
                        "f{self.ids.select_year_spinner.text} Academic Calender - Yearly Income & Exenditure Analysis")
                    plt.style.use('ggplot')
                    plt.tight_layout()
                    plt.axis('equal')
                    plt.axis('equal')

                    plt.legend(loc='upper left')

                    circle = plt.Circle(
                        xy=[0, 0], radius=.75, facecolor='white')
                    plt.gca().add_artist(circle)
                    plt.show()
                except ValueError:
                    self.empty_class_dialog = MDDialog(
                        title="Error!",
                        text="Complete data for the selected timeline does not exit yet",
                        radius=[25, 7, 25, 7],
                        auto_dismiss=False,
                        buttons=[
                            MDRectangleFlatButton(
                                text="CLOSE", on_release=self.close_empty_class_dialog
                            ),
                        ],
                    )
                    self.empty_class_dialog.open()
            else:
                try:
                    # conn = sqlite3.connect("school.db")
                    # c = conn.cursor()
                    # p_l = c.execute(
                    #     """UPDATE income_and_expenditure SET p_l = income - expenditure""")
                    # conn.commit()
                    income = [r[0] for r in c.execute("""SELECT SUM(income_preview)
                                FROM income_and_expenditure_previews
                                WHERE income_and_expenditure_previews.year_preview =?
                                AND income_and_expenditure_previews.term_preview = ?""",
                                                      (self.ids.select_year_spinner.text, self.ids.select_term_spinner.text,))]
                    expenditure = [r[0] for r in c.execute("""SELECT SUM(expenditure_preview)
                                FROM income_and_expenditure_previews
                                WHERE income_and_expenditure_previews.year_preview =?
                                AND income_and_expenditure_previews.term_preview = ?""",
                                                           (self.ids.select_year_spinner.text, self.ids.select_term_spinner.text,))]
                    slices = [income, expenditure]
                    labels = ["Income", "Expenditure"]
                    plt.pie(slices, labels=labels, autopct='%.2f%%',
                            shadow=True, startangle=270)
                    plt.title(
                        f"{self.ids.select_term_spinner.text} Income & Expenditure Analysis - {self.ids.select_year_spinner.text}")
                    plt.style.use('ggplot')
                    plt.tight_layout()
                    plt.axis('equal')
                    plt.axis('equal')

                    plt.legend(loc='upper left')

                    circle = plt.Circle(
                        xy=[0, 0], radius=.75, facecolor='white')
                    plt.gca().add_artist(circle)
                    plt.show()
                except ValueError:
                    self.empty_class_dialog = MDDialog(
                        title="Error!",
                        text="Complete data for the selected timeline does not exit yet",
                        radius=[25, 7, 25, 7],
                        auto_dismiss=False,
                        buttons=[
                            MDRectangleFlatButton(
                                text="CLOSE", on_release=self.close_empty_class_dialog
                            ),
                        ],
                    )
                    self.empty_class_dialog.open()
        else:
            self.empty_class_dialog = MDDialog(
                title="Empty!",
                text="No Data Exits",
                radius=[25, 7, 25, 7],
                auto_dismiss=False,
                buttons=[
                    MDRectangleFlatButton(
                        text="CLOSE", on_release=self.close_empty_class_dialog
                    ),
                ],
            )
            self.empty_class_dialog.open()

    def get_income_graph(self):
        conn = sqlite3.connect("school.db")
        c = conn.cursor()
        p_l = c.execute(
            """UPDATE income_and_expenditure SET p_l = income - expenditure""")
        jan = c.execute("""UPDATE income_and_expenditure_previews
                    SET
                    income_preview = SUM(income),
                    expenditure_preview = SUM(expenditure),
                    p_l_preview = SUM(p_l),
                    term_preview = term,
                    year_preview  = year,
                    month_preview = month
                    FROM income_and_expenditure
                    WHERE income_and_expenditure.year =?
                    AND income_and_expenditure.month = 'January'
                    AND income_and_expenditure_previews.month_preview = 'January'""",
                        (self.ids.select_year_spinner.text,))
        feb = c.execute("""UPDATE income_and_expenditure_previews
                SET
                income_preview = SUM(income),
                expenditure_preview = SUM(expenditure),
                p_l_preview = SUM(p_l),
                term_preview = term,
                year_preview  = year,
                month_preview = month
                FROM income_and_expenditure
                WHERE income_and_expenditure.year =?
                AND income_and_expenditure.month = 'February'
                AND income_and_expenditure_previews.month_preview = 'February'""",
                        (self.ids.select_year_spinner.text,))
        mar = c.execute("""UPDATE income_and_expenditure_previews
                SET
                income_preview = SUM(income),
                expenditure_preview = SUM(expenditure),
                p_l_preview = SUM(p_l),
                term_preview = term,
                year_preview  = year,
                month_preview = month
                FROM income_and_expenditure
                WHERE income_and_expenditure.year =?
                AND income_and_expenditure.month = 'March'
                AND income_and_expenditure_previews.month_preview = 'March'""",
                        (self.ids.select_year_spinner.text,))
        apr = c.execute("""UPDATE income_and_expenditure_previews
                SET
                income_preview = SUM(income),
                expenditure_preview = SUM(expenditure),
                p_l_preview = SUM(p_l),
                term_preview = term,
                year_preview  = year,
                month_preview = month
                FROM income_and_expenditure
                WHERE income_and_expenditure.year =?
                AND income_and_expenditure.month = 'April'
                AND income_and_expenditure_previews.month_preview = 'April'""",
                        (self.ids.select_year_spinner.text,))
        may = c.execute("""UPDATE income_and_expenditure_previews
                SET
                income_preview = SUM(income),
                expenditure_preview = SUM(expenditure),
                p_l_preview = SUM(p_l),
                term_preview = term,
                year_preview  = year,
                month_preview = month
                FROM income_and_expenditure
                WHERE income_and_expenditure.year =?
                AND income_and_expenditure.month = 'May'
                AND income_and_expenditure_previews.month_preview = 'May'""",
                        (self.ids.select_year_spinner.text,))
        june = c.execute("""UPDATE income_and_expenditure_previews
                SET
                income_preview = SUM(income),
                expenditure_preview = SUM(expenditure),
                p_l_preview = SUM(p_l),
                term_preview = term,
                year_preview  = year,
                month_preview = month
                FROM income_and_expenditure
                WHERE income_and_expenditure.year =?
                AND income_and_expenditure.month = 'June'
                AND income_and_expenditure_previews.month_preview = 'June'""",
                         (self.ids.select_year_spinner.text,))
        july = c.execute("""UPDATE income_and_expenditure_previews
                SET
                income_preview = SUM(income),
                expenditure_preview = SUM(expenditure),
                p_l_preview = SUM(p_l),
                term_preview = term,
                year_preview  = year,
                month_preview = month
                FROM income_and_expenditure
                WHERE income_and_expenditure.year =?
                AND income_and_expenditure.month = 'July'
                AND income_and_expenditure_previews.month_preview = 'July'""",
                         (self.ids.select_year_spinner.text,))
        august = c.execute("""UPDATE income_and_expenditure_previews
                SET
                income_preview = SUM(income),
                expenditure_preview = SUM(expenditure),
                p_l_preview = SUM(p_l),
                term_preview = term,
                year_preview  = year,
                month_preview = month
                FROM income_and_expenditure
                WHERE income_and_expenditure.year =?
                AND income_and_expenditure.month = 'August'
                AND income_and_expenditure_previews.month_preview = 'August'""",
                           (self.ids.select_year_spinner.text,))
        sep = c.execute("""UPDATE income_and_expenditure_previews
                SET
                income_preview = SUM(income),
                expenditure_preview = SUM(expenditure),
                p_l_preview = SUM(p_l),
                term_preview = term,
                year_preview  = year,
                month_preview = month
                FROM income_and_expenditure
                WHERE income_and_expenditure.year =?
                AND income_and_expenditure.month = 'September'
                AND income_and_expenditure_previews.month_preview = 'September'""",
                        (self.ids.select_year_spinner.text,))
        october = c.execute("""UPDATE income_and_expenditure_previews
                SET
                income_preview = SUM(income),
                expenditure_preview = SUM(expenditure),
                p_l_preview = SUM(p_l),
                term_preview = term,
                year_preview  = year,
                month_preview = month
                FROM income_and_expenditure
                WHERE income_and_expenditure.year =?
                AND income_and_expenditure.month = 'october'
                AND income_and_expenditure_previews.month_preview = 'october'""",
                            (self.ids.select_year_spinner.text,))
        nov = c.execute("""UPDATE income_and_expenditure_previews
                SET
                income_preview = SUM(income),
                expenditure_preview = SUM(expenditure),
                p_l_preview = SUM(p_l),
                term_preview = term,
                year_preview  = year,
                month_preview = month
                FROM income_and_expenditure
                WHERE income_and_expenditure.year =?
                AND income_and_expenditure.month = 'November'
                AND income_and_expenditure_previews.month_preview = 'November'""",
                        (self.ids.select_year_spinner.text,))
        dec = c.execute("""UPDATE income_and_expenditure_previews
                SET
                income_preview = SUM(income),
                expenditure_preview = SUM(expenditure),
                p_l_preview = SUM(p_l),
                term_preview = term,
                year_preview  = year,
                month_preview = month
                FROM income_and_expenditure
                WHERE income_and_expenditure.year =?
                AND income_and_expenditure.month = 'December'
                AND income_and_expenditure_previews.month_preview = 'December'""",
                        (self.ids.select_year_spinner.text,))
        conn.commit()
        if self.ids.select_data_type_spinner.text == "Bar Chart":
            if self.ids.select_term_spinner.text == "Yearly":
                try:
                    months = [r[0] for r in c.execute(
                        """SELECT months FROM months""")]
                    months_position = np.arange(len(months))

                    income = [r[0] for r in c.execute("""SELECT income_preview
                                FROM income_and_expenditure_previews
                                WHERE income_and_expenditure_previews.year_preview =?""", (self.ids.select_year_spinner.text,))]
                    if len(income) != 12:
                        raise ValueError
                    plt.xlabel("Months")
                    plt.ylabel("Amount in GHC")
                    plt.bar(months_position, income, width=0.4, label="Income")
                    plt.xticks(months_position, months)
                    plt.style.use("seaborn")
                    plt.tight_layout()
                    plt.title(
                        f"{self.ids.select_year_spinner.text} Academic Calender - Yearly Income Analysis")
                    plt.show()
                    print(income)
                except ValueError:
                    self.empty_class_dialog = MDDialog(
                        title="Empty!",
                        text="Complete data for the selected timeline does not exit yet",
                        radius=[40, 7, 40, 7],
                        auto_dismiss=False,
                        buttons=[
                            MDRectangleFlatButton(
                                text="CLOSE", on_release=self.close_empty_class_dialog
                            ),
                        ],
                    )
                    self.empty_class_dialog.open()

            else:
                try:
                    months = [r[0] for r in c.execute(
                        """SELECT months FROM months WHERE months.month_term = ?""", (self.ids.select_term_spinner.text,))]
                    months_position = np.arange(len(months))
                    income = [r[0] for r in c.execute("""SELECT income_preview
                                FROM income_and_expenditure_previews
                                WHERE income_and_expenditure_previews.year_preview =?
                                AND income_and_expenditure_previews.term_preview = ?""",
                                                      (self.ids.select_year_spinner.text, self.ids.select_term_spinner.text,))]
                    if len(income) != 4:
                        raise ValueError
                    plt.xlabel("Months")
                    plt.ylabel("Amount in GHC")
                    plt.bar(months_position, income, width=0.4, label="Income")
                    plt.xticks(months_position, months)
                    plt.style.use("seaborn")
                    plt.tight_layout()
                    plt.title(
                        f"{self.ids.select_term_spinner.text} Income Analysis - {self.ids.select_year_spinner.text}")
                    plt.show()
                except ValueError:
                    self.empty_class_dialog = MDDialog(
                        title="Empty!",
                        text="Complete data for the selected timeline does not exit yet",
                        radius=[40, 7, 40, 7],
                        auto_dismiss=False,
                        buttons=[
                            MDRectangleFlatButton(
                                text="CLOSE", on_release=self.close_empty_class_dialog
                            ),
                        ],
                    )
                    self.empty_class_dialog.open()

        elif self.ids.select_data_type_spinner.text == "Pie Chart" or self.ids.select_data_type_spinner.text == "Donut Chart":
            self.empty_class_dialog = MDDialog(
                title="Empty!",
                text="No Income data exist for Pie charts and Donut Charts",
                radius=[40, 7, 40, 7],
                auto_dismiss=False,
                buttons=[
                    MDRectangleFlatButton(
                        text="CLOSE", on_release=self.close_empty_class_dialog
                    ),
                ],
            )
            self.empty_class_dialog.open()
        else:
            self.empty_class_dialog = MDDialog(
                title="Empty!",
                text="No Data Exits",
                radius=[40, 7, 40, 7],
                auto_dismiss=False,
                buttons=[
                    MDRectangleFlatButton(
                        text="CLOSE", on_release=self.close_empty_class_dialog
                    ),
                ],
            )
            self.empty_class_dialog.open()

    def get_expenditure_graph(self):
        if self.ids.select_data_type_spinner.text == "Pie Chart":
            if self.ids.select_term_spinner.text == "Yearly":
                try:
                    conn = sqlite3.connect("school.db")
                    c = conn.cursor()
                    p_l = c.execute(
                        """UPDATE income_and_expenditure SET p_l = income - expenditure""")
                    conn.commit()

                    academic = [r[0] for r in c.execute("""SELECT SUM(expenditure_amt)
                                FROM expenditure
                                WHERE expenditure.purpose = 'Academic'
                                AND expenditure.year = ?""", (self.ids.select_year_spinner.text,))]
                    canteen = [r[0] for r in c.execute("""SELECT SUM(expenditure_amt)
                                FROM expenditure
                                WHERE expenditure.purpose = 'Canteen'
                                AND expenditure.year = ?""", (self.ids.select_year_spinner.text,))]
                    tax = [r[0] for r in c.execute("""SELECT SUM(expenditure_amt)
                                FROM expenditure
                                WHERE expenditure.purpose = 'Tax'
                                AND expenditure.year = ?""", (self.ids.select_year_spinner.text,))]
                    salary = [r[0] for r in c.execute("""SELECT SUM(expenditure_amt)
                                FROM expenditure
                                WHERE expenditure.purpose = 'Salary'
                                AND expenditure.year = ?""", (self.ids.select_year_spinner.text,))]
                    utility = [r[0] for r in c.execute("""SELECT SUM(expenditure_amt)
                                FROM expenditure
                                WHERE expenditure.purpose = 'Utility'
                                AND expenditure.year = ?""", (self.ids.select_year_spinner.text,))]
                    miscellaneous = [r[0] for r in c.execute("""SELECT SUM(expenditure_amt)
                                FROM expenditure
                                WHERE expenditure.purpose = 'Miscellaneous'
                                AND expenditure.year = ?""", (self.ids.select_year_spinner.text,))]
                    if academic == [None] or canteen == [None] or tax == [None] or salary == [None] or utility == [None] or miscellaneous == [None]:
                        raise ValueError
                    explode = (0, 0, 0, 0.02, 0, 0)
                    slices = [academic, canteen, tax,
                              salary, utility, miscellaneous, ]
                    labels = ['Academic', 'Canteen', "Tax",
                              'Salary', "Utility", "Miscellaneous"]
                    plt.pie(slices, labels=labels, autopct='%.2f%%',
                            explode=explode, startangle=90)
                    plt.title(
                        f"{self.ids.select_year_spinner.text} Academic Calender - Yearly Exenditure Analysis")
                    plt.style.use('ggplot')
                    plt.axis('equal')
                    plt.tight_layout()
                    plt.legend(loc='upper left')
                    plt.show()
                    print(slices)
                except ValueError:
                    self.empty_class_dialog = MDDialog(
                        title="Empty!",
                        text="Complete data for the selected timeline does not exit yet",
                        radius=[40, 7, 40, 7],
                        auto_dismiss=False,
                        buttons=[
                            MDRectangleFlatButton(
                                text="CLOSE", on_release=self.close_empty_class_dialog
                            ),
                        ],
                    )
                    self.empty_class_dialog.open()
            else:
                try:
                    conn = sqlite3.connect("school.db")
                    c = conn.cursor()
                    academic = [r[0] for r in c.execute("""SELECT SUM(expenditure_amt)
                                FROM expenditure
                                WHERE expenditure.purpose = 'Academic'
                                AND expenditure.year = ?
                                AND expenditure.term = ?
                                """, (self.ids.select_year_spinner.text, self.ids.select_term_spinner.text,))]
                    canteen = [r[0] for r in c.execute("""SELECT SUM(expenditure_amt)
                                FROM expenditure
                                WHERE expenditure.purpose = 'Canteen'
                                AND expenditure.year = ?
                                AND expenditure.term = ?""", (self.ids.select_year_spinner.text, self.ids.select_term_spinner.text,))]
                    tax = [r[0] for r in c.execute("""SELECT SUM(expenditure_amt)
                                FROM expenditure
                                WHERE expenditure.purpose = 'Tax'
                                AND expenditure.year = ?
                                AND expenditure.term = ?
                                """, (self.ids.select_year_spinner.text, self.ids.select_term_spinner.text,))]
                    salary = [r[0] for r in c.execute("""SELECT SUM(expenditure_amt)
                                FROM expenditure
                                WHERE expenditure.purpose = 'Salary'
                                AND expenditure.year = ?
                                AND expenditure.term = ?""", (self.ids.select_year_spinner.text, self.ids.select_term_spinner.text,))]
                    utility = [r[0] for r in c.execute("""SELECT SUM(expenditure_amt)
                                FROM expenditure
                                WHERE expenditure.purpose = 'Utility'
                                AND expenditure.year = ?
                                AND expenditure.term = ?""", (self.ids.select_year_spinner.text, self.ids.select_term_spinner.text,))]
                    miscellaneous = [r[0] for r in c.execute("""SELECT SUM(expenditure_amt)
                                FROM expenditure
                                WHERE expenditure.purpose = 'Miscellaneous'
                                AND expenditure.year = ?
                                AND expenditure.term = ?""", (self.ids.select_year_spinner.text, self.ids.select_term_spinner.text,))]
                    if academic == [None]:
                        academic = [0]
                    elif canteen == [None]:
                        canteen = [0]
                    elif tax == [None]:
                        tax = [0]
                    elif salary == [None]:
                        salary = [0]
                    elif utility == [None]:
                        utility = [0]
                    elif miscellaneous == [None]:
                        miscellaneous = [0]

                    explode = (0, 0, 0, 0.02, 0, 0)
                    labels = ['Academic', 'Canteen', "Tax",
                              'Salary', "Utility", "Miscellaneous"]
                    slices = [academic, canteen, tax,
                              salary, utility, miscellaneous]
                    plt.pie(slices, labels=labels, autopct='%.2f%%',
                            explode=explode, startangle=90)
                    plt.title(
                        f"{self.ids.select_term_spinner.text} Expenditure Analysis - {self.ids.select_year_spinner.text}")
                    plt.style.use('ggplot')
                    plt.axis('equal')
                    plt.tight_layout()
                    plt.legend(loc='upper left')
                    plt.show()
                except ValueError:
                    self.empty_class_dialog = MDDialog(
                        title="Notice!",
                        text="Complete data for the selected timeline does not exit yet",
                        radius=[40, 7, 40, 7],
                        auto_dismiss=False,
                        buttons=[
                            MDRectangleFlatButton(
                                text="CLOSE", on_release=self.close_empty_class_dialog
                            ),
                        ],
                    )
                    self.empty_class_dialog.open()
        elif self.ids.select_data_type_spinner.text == "Donut Chart":
            if self.ids.select_term_spinner.text == "Yearly":
                try:
                    conn = sqlite3.connect("school.db")
                    c = conn.cursor()
                    p_l = c.execute(
                        """UPDATE income_and_expenditure SET p_l = income - expenditure""")
                    conn.commit()

                    academic = [r[0] for r in c.execute("""SELECT SUM(expenditure_amt)
                                FROM expenditure
                                WHERE expenditure.purpose = 'Academic'
                                AND expenditure.year = ?""", (self.ids.select_year_spinner.text,))]
                    canteen = [r[0] for r in c.execute("""SELECT SUM(expenditure_amt)
                                FROM expenditure
                                WHERE expenditure.purpose = 'Canteen'
                                AND expenditure.year = ?""", (self.ids.select_year_spinner.text,))]
                    tax = [r[0] for r in c.execute("""SELECT SUM(expenditure_amt)
                                FROM expenditure
                                WHERE expenditure.purpose = 'Tax'
                                AND expenditure.year = ?""", (self.ids.select_year_spinner.text,))]
                    salary = [r[0] for r in c.execute("""SELECT SUM(expenditure_amt)
                                FROM expenditure
                                WHERE expenditure.purpose = 'Salary'
                                AND expenditure.year = ?""", (self.ids.select_year_spinner.text,))]
                    utility = [r[0] for r in c.execute("""SELECT SUM(expenditure_amt)
                                FROM expenditure
                                WHERE expenditure.purpose = 'Utility'
                                AND expenditure.year = ?""", (self.ids.select_year_spinner.text,))]
                    miscellaneous = [r[0] for r in c.execute("""SELECT SUM(expenditure_amt)
                                FROM expenditure
                                WHERE expenditure.purpose = 'Miscellaneous'
                                AND expenditure.year = ?""", (self.ids.select_year_spinner.text,))]
                    if academic == [None] or canteen == [None] or tax == [None] or salary == [None] or utility == [None] or miscellaneous == [None]:
                        raise ValueError
                    slices = [academic, canteen, tax,
                              salary, utility, miscellaneous, ]
                    labels = ['Academic', 'Canteen', "Tax",
                              'Salary', "Utility", "Miscellaneous"]
                    plt.pie(slices, labels=labels,
                            autopct='%.1f%%', shadow=True, startangle=90)
                    plt.title(
                        "{self.ids.select_year_spinner.text} Academic Calender - Yearly Exenditure Analysis")
                    plt.style.use('ggplot')
                    plt.axis('equal')
                    plt.tight_layout()
                    plt.legend(loc='upper left')
                    circle = plt.Circle(
                        xy=[0, 0], radius=.75, facecolor='white')
                    plt.gca().add_artist(circle)
                    plt.show()
                    print(slices)
                except ValueError:
                    self.empty_class_dialog = MDDialog(
                        title="Empty!",
                        text="Data for the selected timeline may not exit yet",
                        radius=[40, 7, 40, 7],
                        auto_dismiss=False,
                        buttons=[
                            MDRectangleFlatButton(
                                text="CLOSE", on_release=self.close_empty_class_dialog
                            ),
                        ],
                    )
                    self.empty_class_dialog.open()
            else:
                try:
                    conn = sqlite3.connect("school.db")
                    c = conn.cursor()
                    academic = [r[0] for r in c.execute("""SELECT SUM(expenditure_amt)
                                FROM expenditure
                                WHERE expenditure.purpose = 'Academic'
                                AND expenditure.year = ?
                                AND expenditure.term = ?
                                """, (self.ids.select_year_spinner.text, self.ids.select_term_spinner.text,))]
                    canteen = [r[0] for r in c.execute("""SELECT SUM(expenditure_amt)
                                FROM expenditure
                                WHERE expenditure.purpose = 'Canteen'
                                AND expenditure.year = ?
                                AND expenditure.term = ?""", (self.ids.select_year_spinner.text, self.ids.select_term_spinner.text,))]
                    tax = [r[0] for r in c.execute("""SELECT SUM(expenditure_amt)
                                FROM expenditure
                                WHERE expenditure.purpose = 'Tax'
                                AND expenditure.year = ?
                                AND expenditure.term = ?
                                """, (self.ids.select_year_spinner.text, self.ids.select_term_spinner.text,))]
                    salary = [r[0] for r in c.execute("""SELECT SUM(expenditure_amt)
                                FROM expenditure
                                WHERE expenditure.purpose = 'Salary'
                                AND expenditure.year = ?
                                AND expenditure.term = ?""", (self.ids.select_year_spinner.text, self.ids.select_term_spinner.text,))]
                    utility = [r[0] for r in c.execute("""SELECT SUM(expenditure_amt)
                                FROM expenditure
                                WHERE expenditure.purpose = 'Utility'
                                AND expenditure.year = ?
                                AND expenditure.term = ?""", (self.ids.select_year_spinner.text, self.ids.select_term_spinner.text,))]
                    miscellaneous = [r[0] for r in c.execute("""SELECT SUM(expenditure_amt)
                                FROM expenditure
                                WHERE expenditure.purpose = 'Miscellaneous'
                                AND expenditure.year = ?
                                AND expenditure.term = ?""", (self.ids.select_year_spinner.text, self.ids.select_term_spinner.text,))]
                    if academic == [None]:
                        academic = [0]
                    elif canteen == [None]:
                        canteen = [0]
                    elif tax == [None]:
                        tax = [0]
                    elif salary == [None]:
                        salary = [0]
                    elif utility == [None]:
                        utility = [0]
                    elif miscellaneous == [None]:
                        miscellaneous = [0]
                    explode = (0, 0, 0, 0.02, 0, 0)
                    labels = ['Academic', 'Canteen', "Tax",
                              'Salary', "Utility", "Miscellaneous"]
                    slices = [academic, canteen, tax,
                              salary, utility, miscellaneous]
                    plt.pie(slices, labels=labels,
                            autopct='%.2f%%', shadow=True, startangle=90)
                    plt.title(
                        f"{self.ids.select_term_spinner.text} Expenditure Analysis - {self.ids.select_year_spinner.text}")
                    plt.style.use('ggplot')
                    plt.axis('equal')
                    plt.tight_layout()
                    plt.legend(loc='upper left')
                    circle = plt.Circle(
                        xy=[0, 0], radius=.75, facecolor='white')
                    plt.gca().add_artist(circle)
                    plt.show()
                except ValueError:
                    self.empty_class_dialog = MDDialog(
                        title="Error",
                        text="Complete data for the selected timeline does not exit yet",
                        radius=[40, 7, 40, 7],
                        auto_dismiss=False,
                        buttons=[
                            MDRectangleFlatButton(
                                text="CLOSE", on_release=self.close_empty_class_dialog
                            ),
                        ],
                    )
                    self.empty_class_dialog.open()

                    labels = ["Income", "Expenditure"]
                    colors = ["green", "red"]
                    plt.pie(slices, labels=labels, autopct='%.2f%%',
                            colors=colors, shadow=True, startangle=90)
                    plt.title("Yearly Exenditure Analysis")
                    plt.style.use('ggplot')
                    plt.tight_layout()
                    plt.axis('equal')
                    plt.axis('equal')

                    plt.legend(loc='upper left')

                    circle = plt.Circle(
                        xy=[0, 0], radius=.75, facecolor='white')
                    plt.gca().add_artist(circle)
                    plt.show()

        elif self.ids.select_data_type_spinner.text == "Bar Chart":
            if self.ids.select_term_spinner.text == "Yearly":
                try:
                    conn = sqlite3.connect("school.db")
                    c = conn.cursor()
                    academic = [r[0] for r in c.execute("""SELECT SUM(expenditure_amt)
                                FROM expenditure
                                WHERE expenditure.purpose = 'Academic'
                                AND expenditure.year = ?""", (self.ids.select_year_spinner.text,))]
                    canteen = [r[0] for r in c.execute("""SELECT SUM(expenditure_amt)
                                FROM expenditure
                                WHERE expenditure.purpose = 'Canteen'
                                AND expenditure.year = ?""", (self.ids.select_year_spinner.text,))]
                    tax = [r[0] for r in c.execute("""SELECT SUM(expenditure_amt)
                                FROM expenditure
                                WHERE expenditure.purpose = 'Tax'
                                AND expenditure.year = ?""", (self.ids.select_year_spinner.text,))]
                    salary = [r[0] for r in c.execute("""SELECT SUM(expenditure_amt)
                                FROM expenditure
                                WHERE expenditure.purpose = 'Salary'
                                AND expenditure.year = ?""", (self.ids.select_year_spinner.text,))]
                    utility = [r[0] for r in c.execute("""SELECT SUM(expenditure_amt)
                                FROM expenditure
                                WHERE expenditure.purpose = 'Utility'
                                AND expenditure.year = ?""", (self.ids.select_year_spinner.text,))]
                    miscellaneous = [r[0] for r in c.execute("""SELECT SUM(expenditure_amt)
                                FROM expenditure
                                WHERE expenditure.purpose = 'Miscellaneous'
                                AND expenditure.year = ?""", (self.ids.select_year_spinner.text,))]
                    c.execute(
                        """UPDATE expenditure_barchart
                                    SET
                                    expense_amt = ?  WHERE expense_name = 'Academic'""", academic)
                    c.execute(
                        """UPDATE expenditure_barchart
                                    SET
                                    expense_amt = ?  WHERE expense_name = 'Canteen'""", canteen)
                    c.execute(
                        """UPDATE expenditure_barchart
                                    SET
                                    expense_amt = ?  WHERE expense_name = 'Tax'""", tax)
                    c.execute(
                        """UPDATE expenditure_barchart
                                    SET
                                    expense_amt = ?  WHERE expense_name = 'Salary'""", salary)
                    c.execute(
                        """UPDATE expenditure_barchart
                                    SET
                                    expense_amt = ?  WHERE expense_name = 'Utility'""", utility)
                    c.execute(
                        """UPDATE expenditure_barchart
                                    SET
                                    expense_amt = ?  WHERE expense_name = 'Miscellaneous'""", miscellaneous)

                    conn.commit()
                    the_bar = [r[0] for r in c.execute(
                        """SELECT  expense_amt FROM expenditure_barchart""")]

                    expenditure_type = ['Academic', 'Canteen', 'Tax',
                                        'Salary', 'Utility', 'Miscellaneous']
                    xposition = np.arange(len(expenditure_type))

                    plt.xlabel("Expenditure Breakdown")
                    plt.ylabel("Amount in GHC")
                    plt.bar(xposition, the_bar, width=0.4)
                    plt.xticks(xposition, expenditure_type)
                    plt.style.use("seaborn")
                    plt.tight_layout()
                    plt.title(
                        f"{self.ids.select_year_spinner.text} Academic Calender - Yearly Expenditure Analysis")
                    plt.show()

                except (ValueError, TypeError):
                    self.empty_class_dialog = MDDialog(
                        title="Empty!",
                        text="Complete data for the selected timeline does not exit yet",
                        radius=[40, 7, 40, 7],
                        auto_dismiss=False,
                        buttons=[
                            MDRectangleFlatButton(
                                text="CLOSE", on_release=self.close_empty_class_dialog
                            ),
                        ],
                    )
                    self.empty_class_dialog.open()

            else:
                try:
                    conn = sqlite3.connect("school.db")
                    c = conn.cursor()
                    conn = sqlite3.connect("school.db")
                    c = conn.cursor()
                    academic = [r[0] for r in c.execute("""SELECT SUM(expenditure_amt)
                                FROM expenditure
                                WHERE expenditure.purpose = 'Academic'
                                AND expenditure.year = ?
                                AND expenditure.term = ? """,
                                                        (self.ids.select_year_spinner.text, self.ids.select_term_spinner.text))]
                    canteen = [r[0] for r in c.execute("""SELECT SUM(expenditure_amt)
                                FROM expenditure
                                WHERE expenditure.purpose = 'Canteen'
                                AND expenditure.year = ?
                                AND expenditure.term = ? """,
                                                       (self.ids.select_year_spinner.text, self.ids.select_term_spinner.text))]
                    tax = [r[0] for r in c.execute("""SELECT SUM(expenditure_amt)
                                FROM expenditure
                                WHERE expenditure.purpose = 'Tax'
                                AND expenditure.year = ?
                                AND expenditure.term = ? """,
                                                   (self.ids.select_year_spinner.text, self.ids.select_term_spinner.text))]
                    salary = [r[0] for r in c.execute("""SELECT SUM(expenditure_amt)
                                FROM expenditure
                                WHERE expenditure.purpose = 'Salary'
                                AND expenditure.year = ?
                                AND expenditure.term = ? """,
                                                      (self.ids.select_year_spinner.text, self.ids.select_term_spinner.text))]
                    utility = [r[0] for r in c.execute("""SELECT SUM(expenditure_amt)
                                FROM expenditure
                                WHERE expenditure.purpose = 'Utility'
                                AND expenditure.year = ?
                                AND expenditure.term = ? """,
                                                       (self.ids.select_year_spinner.text, self.ids.select_term_spinner.text))]
                    miscellaneous = [r[0] for r in c.execute("""SELECT SUM(expenditure_amt)
                                FROM expenditure
                                WHERE expenditure.purpose = 'Miscellaneous'
                                AND expenditure.year = ?
                                AND expenditure.term = ? """,
                                                             (self.ids.select_year_spinner.text, self.ids.select_term_spinner.text))]
                    if academic == [None]:
                        academic = [0]
                    elif canteen == [None]:
                        canteen = [0]
                    elif tax == [None]:
                        tax = [0]
                    elif salary == [None]:
                        salary = [0]
                    elif utility == [None]:
                        utility = [0]
                    elif miscellaneous == [None]:
                        miscellaneous = [0]
                    c.execute(
                        """UPDATE expenditure_barchart
                                    SET
                                    expense_amt = ?  WHERE expense_name = 'Academic'""", academic)
                    c.execute(
                        """UPDATE expenditure_barchart
                                    SET
                                    expense_amt = ?  WHERE expense_name = 'Canteen'""", canteen)
                    c.execute(
                        """UPDATE expenditure_barchart
                                    SET
                                    expense_amt = ?  WHERE expense_name = 'Tax'""", tax)
                    c.execute(
                        """UPDATE expenditure_barchart
                                    SET
                                    expense_amt = ?  WHERE expense_name = 'Salary'""", salary)
                    c.execute(
                        """UPDATE expenditure_barchart
                                    SET
                                    expense_amt = ?  WHERE expense_name = 'Utility'""", utility)
                    c.execute(
                        """UPDATE expenditure_barchart
                                    SET
                                    expense_amt = ?  WHERE expense_name = 'Miscellaneous'""", miscellaneous)

                    conn.commit()
                    the_bar = [r[0] for r in c.execute(
                        """SELECT  expense_amt FROM expenditure_barchart""")]

                    expenditure_type = ['Academic', 'Canteen', 'Tax',
                                        'Salary', 'Utility', 'Miscellaneous']
                    xposition = np.arange(len(expenditure_type))

                    plt.xlabel("Expenditure Breakdown")
                    plt.ylabel("Amount in GHC")
                    plt.bar(xposition, the_bar, width=0.4)
                    plt.xticks(xposition, expenditure_type)
                    plt.style.use("seaborn")
                    plt.tight_layout()
                    plt.title(
                        f"{self.ids.select_term_spinner.text} Expenditure Analysis - {self.ids.select_year_spinner.text}")
                    plt.show()

                except (ValueError, TypeError):
                    self.empty_class_dialog = MDDialog(
                        title="Empty!",
                        text="Complete data for the selected timeline does not exit yet",
                        radius=[40, 7, 40, 7],
                        auto_dismiss=False,
                        buttons=[
                            MDRectangleFlatButton(
                                text="CLOSE", on_release=self.close_empty_class_dialog
                            ),
                        ],
                    )
                    self.empty_class_dialog.open()
        else:
            self.empty_class_dialog = MDDialog(
                title="Empty!",
                text="No Data Exits",
                radius=[25, 7, 25, 7],
                auto_dismiss=False,
                buttons=[
                    MDRectangleFlatButton(
                        text="CLOSE", on_release=self.close_empty_class_dialog
                    ),
                ],
            )
            self.empty_class_dialog.open()

    def del_spinner_choices(self):
        self.ids.select_year_spinner.text = "Select Year"
        self.ids.select_year_spinner.background_color = .7, 0, 0, .9

        self.ids.select_term_spinner.text = "Select Term"
        self.ids.select_term_spinner.background_color = .7, 0, 0, .9

        self.ids.select_data_type_spinner.text = "Select Graph Type"
        self.ids.select_data_type_spinner.background_color = .7, 0, 0, .9

    def close_empty_class_dialog(self, obj):
        self.empty_class_dialog.dismiss()

    def spinner_clicked(self, value):
        self.ids.text = value
        return value

    def logout(self):
        self.empty_class_dialog = MDDialog(
            title="Logging out...",
            text="Are you sure you want to log out?",
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


class IncomeExpenditureAnalytics(Screen):
    conn = sqlite3.connect("school.db")
    c = conn.cursor()
    values = [r[0]
              for r in c.execute("SELECT available_years FROM years")]
    years = values

    def spinner_clicked(self, value):
        self.ids.text = value
        return value

    def logout(self):
        self.empty_class_dialog = MDDialog(
            title="Logging out...",
            text="Are you sure you want to log out?",
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
