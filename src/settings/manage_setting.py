import sqlite3
import datetime
import src.exceptions.exceptions as exceptions
from kivy.uix.screenmanager import Screen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRectangleFlatButton, MDFlatButton
from kivymd.uix.pickers import MDDatePicker


class Manage(Screen):
    def logout(self):
        self.empty_class_dialog = MDDialog(
            title="Logging out...",
            text="Are you sure you want to log out?",
            
            buttons=[
                MDRectangleFlatButton(
                    text="YES", on_release=self.close_dialog_and_logout
                ),
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


class Set(Screen):
    def confirmation_of_promotion_dialog(self):
        self.confirmation_promotion_dialog = MDDialog(
            title="Confirm promotion?!",
            text="""Confirm promotion? Clicking 'YES' will move all students to the next grade. Grade 9 students will be removed from the fees list. They can be added back using the 'Reverse Promotion' only once!""",
            radius=[40, 7, 40, 7],
            auto_dismiss=False,
            buttons=[
                MDRectangleFlatButton(
                    text="YES", on_release=self.promote_students, on_press=self.close_confirmation_promotion_dialog
                ),
                MDFlatButton(
                    text="NO", on_release=self.close_confirmation_promotion_dialog
                ),
            ],
        )
        self.confirmation_promotion_dialog.open()

    def close_confirmation_promotion_dialog(self, obj):
        self.confirmation_promotion_dialog.dismiss()

    def promote_students(self, obj):
        try:
            completed_date = datetime.date.today()
            self.completed_year = completed_date.year
            conn = sqlite3.connect("school.db")
            c = conn.cursor()
            c.execute("UPDATE completed_students SET completed_year = ?",
                      (self.completed_year,))
            c.execute(
                "UPDATE completed_students SET completion_level = '#'")
            conn.commit()
            conn.close()
            conn = sqlite3.connect("school.db")
            c = conn.cursor()
            c.execute(
                """INSERT OR IGNORE INTO completed_students(full_name, registration_number,
                    grade, grade_and_category, status, arrears)
                    SELECT full_name, registration_number,
                    grade, grade_and_category, status, balance FROM fees_payable
                    WHERE grade = 'Grade 9'
                    """)
            c.execute(
                "UPDATE completed_students SET completed_year = ? WHERE completion_level = 'o'",
                (self.completed_year,))
            conn.commit()
            conn.close()

            conn = sqlite3.connect("school.db")
            c = conn.cursor()
            c.execute(
                "UPDATE completed_students SET completion_level = 'o' WHERE completion_level = 'o'")
            conn.commit()
            conn.close()

            conn = sqlite3.connect("school.db")
            c = conn.cursor()
            c.execute(
                "UPDATE completed_students SET completion_level = 'c' WHERE completion_level = 'o'")
            conn.commit()
            conn.close()

            conn = sqlite3.connect("school.db")
            c = conn.cursor()
            c.execute(
                """UPDATE students
                    SET completion_level = 'c'
                    FROM completed_students
                    WHERE completed_students.registration_number = students.registration_number
                    """)
            conn.commit()
            conn.close()

            conn = sqlite3.connect("school.db")
            c = conn.cursor()
            c.execute(
                """UPDATE students
                    SET completed_arrear = arrears
                    FROM completed_students
                    WHERE completed_students.registration_number = students.registration_number
                    """)
            conn.commit()
            conn.close()

            conn = sqlite3.connect("school.db")
            c = conn.cursor()
            c.execute(
                """DELETE FROM fees_payable WHERE grade = 'Grade 9'""")
            c.execute("""UPDATE fees_paid
            SET grade_and_category = 'Completed A' WHERE grade_and_category = 'Grade 9A'""")
            c.execute("""UPDATE fees_paid
            SET grade_and_category = 'Completed B' WHERE grade_and_category = 'Grade 9B'""")
            c.execute("""UPDATE students
            SET current_class = ? WHERE current_class = 'Grade 9A'""", (self.completed_year,))
            c.execute("""UPDATE students
            SET current_class = ? WHERE current_class = 'Grade 9B'""", (self.completed_year,))
            conn.commit()
            conn.close()

            conn = sqlite3.connect("school.db")
            c = conn.cursor()
            c.execute("""UPDATE fees_payable
            SET grade = 'Grade 9' WHERE grade = 'Grade 8'""")
            c.execute("""UPDATE fees_payable
            SET grade_and_category = 'Grade 9A' WHERE grade_and_category = 'Grade 8A'""")
            c.execute("""UPDATE fees_payable
            SET grade_and_category = 'Grade 9B' WHERE grade_and_category = 'Grade 8B'""")
            c.execute("""UPDATE fees_paid
            SET current_grade = 'Grade 9A' WHERE current_grade = 'Grade 8A'""")
            c.execute("""UPDATE fees_paid
            SET current_grade = 'Grade 9B' WHERE current_grade = 'Grade 8B'""")
            c.execute("""UPDATE students
            SET current_class = 'Grade 9A' WHERE current_class = 'Grade 8A'""")
            c.execute("""UPDATE students
            SET current_class = 'Grade 9B' WHERE current_class = 'Grade 8B'""")
            c.execute("""UPDATE students
            SET grade = 'Grade 9' WHERE grade = 'Grade 8'""")
            # c.execute("""UPDATE students
            # SET grade = 'Grade 3' WHERE grade = 'Grade 2'""")
            # # c.execute("""UPDATE students
            # SET current_class = 'Grade 9B' WHERE current_class = 'Grade 8B'""")
            conn.commit()
            conn.close()

            conn = sqlite3.connect("school.db")
            c = conn.cursor()
            c.execute("""UPDATE fees_payable
                SET grade = 'Grade 8' WHERE grade = 'Grade 7'""")
            c.execute("""UPDATE fees_payable
            SET grade_and_category = 'Grade 8A' WHERE grade_and_category = 'Grade 7A'""")
            c.execute("""UPDATE fees_payable
            SET grade_and_category = 'Grade 8B' WHERE grade_and_category = 'Grade 7B'""")
            c.execute("""UPDATE fees_paid
            SET current_grade = 'Grade 8A' WHERE current_grade = 'Grade 7A'""")
            c.execute("""UPDATE fees_paid
            SET current_grade = 'Grade 8B' WHERE current_grade = 'Grade 7B'""")
            c.execute("""UPDATE students
            SET current_class = 'Grade 8A' WHERE current_class = 'Grade 7A'""")
            c.execute("""UPDATE students
            SET current_class = 'Grade 8B' WHERE current_class = 'Grade 7B'""")
            c.execute("""UPDATE students
            SET grade = 'Grade 8' WHERE grade = 'Grade 7'""")
            conn.commit()
            conn.close()

            conn = sqlite3.connect("school.db")
            c = conn.cursor()
            c.execute("""UPDATE fees_payable
                SET grade = 'Grade 7' WHERE grade = 'Grade 6'""")
            c.execute("""UPDATE fees_payable
            SET grade_and_category = 'Grade 7A' WHERE grade_and_category = 'Grade 6A'""")
            c.execute("""UPDATE fees_payable
            SET grade_and_category = 'Grade 7B' WHERE grade_and_category = 'Grade 6B'""")
            c.execute("""UPDATE fees_paid
            SET current_grade = 'Grade 7A' WHERE current_grade = 'Grade 6A'""")
            c.execute("""UPDATE fees_paid
            SET current_grade = 'Grade 7B' WHERE current_grade = 'Grade 6B'""")
            c.execute("""UPDATE students
            SET current_class = 'Grade 7A' WHERE current_class = 'Grade 6A'""")
            c.execute("""UPDATE students
            SET current_class = 'Grade 7B' WHERE current_class = 'Grade 6B'""")
            c.execute("""UPDATE students
            SET grade = 'Grade 7' WHERE grade = 'Grade 6'""")
            conn.commit()
            conn.close()

            conn = sqlite3.connect("school.db")
            c = conn.cursor()
            c.execute("""UPDATE fees_payable
                SET grade = 'Grade 6' WHERE grade = 'Grade 5'""")
            c.execute("""UPDATE fees_payable
            SET grade_and_category = 'Grade 6A' WHERE grade_and_category = 'Grade 5A'""")
            c.execute("""UPDATE fees_payable
            SET grade_and_category = 'Grade 6B' WHERE grade_and_category = 'Grade 5B'""")
            c.execute("""UPDATE fees_paid
            SET current_grade = 'Grade 6A' WHERE current_grade = 'Grade 5A'""")
            c.execute("""UPDATE fees_paid
            SET current_grade = 'Grade 6B' WHERE current_grade = 'Grade 5B'""")
            c.execute("""UPDATE students
            SET current_class = 'Grade 6A' WHERE current_class = 'Grade 5A'""")
            c.execute("""UPDATE students
            SET current_class = 'Grade 6B' WHERE current_class = 'Grade 5B'""")
            c.execute("""UPDATE students
            SET grade = 'Grade 6' WHERE grade = 'Grade 5'""")
            conn.commit()
            conn.close()

            conn = sqlite3.connect("school.db")
            c = conn.cursor()
            c.execute("""UPDATE fees_payable
                SET grade = 'Grade 5' WHERE grade = 'Grade 4'""")
            c.execute("""UPDATE fees_payable
            SET grade_and_category = 'Grade 5A' WHERE grade_and_category = 'Grade 4A'""")
            c.execute("""UPDATE fees_payable
            SET grade_and_category = 'Grade 5B' WHERE grade_and_category = 'Grade 4B'""")
            c.execute("""UPDATE fees_paid
            SET current_grade = 'Grade 5A' WHERE current_grade = 'Grade 4A'""")
            c.execute("""UPDATE fees_paid
            SET current_grade = 'Grade 5B' WHERE current_grade = 'Grade 4B'""")
            c.execute("""UPDATE students
            SET current_class = 'Grade 5A' WHERE current_class = 'Grade 4A'""")
            c.execute("""UPDATE students
            SET current_class = 'Grade 5B' WHERE current_class = 'Grade 4B'""")
            c.execute("""UPDATE students
            SET grade = 'Grade 5' WHERE grade = 'Grade 4'""")
            conn.commit()
            conn.close()

            conn = sqlite3.connect("school.db")
            c = conn.cursor()
            c.execute("""UPDATE fees_payable
                    SET grade = 'Grade 4' WHERE grade = 'Grade 3'""")
            c.execute("""UPDATE fees_payable
            SET grade_and_category = 'Grade 4A' WHERE grade_and_category = 'Grade 3A'""")
            c.execute("""UPDATE fees_payable
            SET grade_and_category = 'Grade 4B' WHERE grade_and_category = 'Grade 3B'""")
            c.execute("""UPDATE fees_paid
            SET current_grade = 'Grade 4A' WHERE current_grade = 'Grade 3A'""")
            c.execute("""UPDATE fees_paid
            SET current_grade = 'Grade 4B' WHERE current_grade = 'Grade 3B'""")
            c.execute("""UPDATE students
            SET current_class = 'Grade 4A' WHERE current_class = 'Grade 3A'""")
            c.execute("""UPDATE students
            SET current_class = 'Grade 4B' WHERE current_class = 'Grade 3B'""")
            c.execute("""UPDATE students
            SET grade = 'Grade 4' WHERE grade = 'Grade 3'""")
            conn.commit()
            conn.close()

            conn = sqlite3.connect("school.db")
            c = conn.cursor()
            c.execute("""UPDATE fees_payable
                SET grade = 'Grade 3' WHERE grade = 'Grade 2'""")
            c.execute("""UPDATE fees_payable
            SET grade_and_category = 'Grade 3A' WHERE grade_and_category = 'Grade 2A'""")
            c.execute("""UPDATE fees_payable
            SET grade_and_category = 'Grade 3B' WHERE grade_and_category = 'Grade 2B'""")
            c.execute("""UPDATE fees_paid
            SET current_grade = 'Grade 3A' WHERE current_grade = 'Grade 2A'""")
            c.execute("""UPDATE fees_paid
            SET current_grade = 'Grade 3B' WHERE current_grade = 'Grade 2B'""")
            c.execute("""UPDATE students
            SET current_class = 'Grade 3A' WHERE current_class = 'Grade 2A'""")
            c.execute("""UPDATE students
            SET current_class = 'Grade 3B' WHERE current_class = 'Grade 2B'""")
            c.execute("""UPDATE students
            SET grade = 'Grade 3' WHERE grade = 'Grade 2'""")
            conn.commit()
            conn.close()

            conn = sqlite3.connect("school.db")
            c = conn.cursor()
            c.execute("""UPDATE fees_payable
                SET grade = 'Grade 2' WHERE grade = 'Grade 1'""")
            c.execute("""UPDATE fees_payable
            SET grade_and_category = 'Grade 2A' WHERE grade_and_category = 'Grade 1A'""")
            c.execute("""UPDATE fees_payable
            SET grade_and_category = 'Grade 2B' WHERE grade_and_category = 'Grade 1B'""")
            c.execute("""UPDATE fees_paid
            SET current_grade = 'Grade 2A' WHERE current_grade = 'Grade 1A'""")
            c.execute("""UPDATE fees_paid
            SET current_grade = 'Grade 2B' WHERE current_grade = 'Grade 1B'""")
            c.execute("""UPDATE students
            SET current_class = 'Grade 2A' WHERE current_class = 'Grade 1A'""")
            c.execute("""UPDATE students
            SET current_class = 'Grade 2B' WHERE current_class = 'Grade 1B'""")
            c.execute("""UPDATE students
            SET grade = 'Grade 2' WHERE grade = 'Grade 1'""")
            conn.commit()
            conn.close()

            conn = sqlite3.connect("school.db")
            c = conn.cursor()
            c.execute("""UPDATE fees_payable
                SET grade = 'Grade 1' WHERE grade = 'KG 2'""")
            c.execute("""UPDATE fees_payable
            SET grade_and_category = 'Grade 1A' WHERE grade_and_category = 'KG 2A'""")
            c.execute("""UPDATE fees_payable
            SET grade_and_category = 'Grade 1B' WHERE grade_and_category = 'KG 2B'""")
            c.execute("""UPDATE fees_paid
            SET current_grade = 'Grade 1A' WHERE current_grade = 'KG 2A'""")
            c.execute("""UPDATE fees_paid
            SET current_grade = 'Grade 1B' WHERE current_grade = 'KG 2B'""")
            c.execute("""UPDATE students
            SET current_class = 'Grade 1A' WHERE current_class = 'KG 2A'""")
            c.execute("""UPDATE students
            SET current_class = 'Grade 1B' WHERE current_class = 'KG 2B'""")
            c.execute("""UPDATE students
            SET grade = 'Grade 1' WHERE grade = 'KG 2'""")
            # c.execute("""UPDATE students
            # SET grade = 'Grade 1' WHERE current_class = 'KG 2B'""")
            conn.commit()
            conn.close()

            conn = sqlite3.connect("school.db")
            c = conn.cursor()
            c.execute(
                """UPDATE fees_payable SET grade = 'KG 2' WHERE grade = 'KG 1'""")
            c.execute("""UPDATE fees_payable
            SET grade_and_category = 'KG 2A' WHERE grade_and_category = 'KG 1A'""")
            c.execute("""UPDATE fees_payable
            SET grade_and_category = 'KG 2B' WHERE grade_and_category = 'KG 1B'""")
            c.execute("""UPDATE fees_paid
            SET current_grade = 'KG 2A' WHERE current_grade = 'KG 1A'""")
            c.execute("""UPDATE fees_paid
            SET current_grade = 'KG 2B' WHERE current_grade = 'KG 1B'""")
            c.execute("""UPDATE students
            SET current_class = 'KG 2A' WHERE current_class = 'KG 1A'""")
            c.execute("""UPDATE students
            SET current_class = 'KG 2B' WHERE current_class = 'KG 1B'""")
            c.execute("""UPDATE students
            SET grade = 'KG 2' WHERE grade = 'KG 1'""")
            conn.commit()
            conn.commit()
            conn.close()

            conn = sqlite3.connect("school.db")
            c = conn.cursor()
            c.execute("""UPDATE fees_payable
                    SET grade = 'KG 1' WHERE grade = 'Nursery 2'""")
            c.execute("""UPDATE fees_payable
            SET grade_and_category = 'KG 1A' WHERE grade_and_category = 'Nursery 2A'""")
            c.execute("""UPDATE fees_payable
            SET grade_and_category = 'KG 1B' WHERE grade_and_category = 'Nursery 2B'""")
            c.execute("""UPDATE fees_paid
            SET current_grade = 'KG 1A' WHERE current_grade = 'Nursery 2A'""")
            c.execute("""UPDATE fees_paid
            SET current_grade = 'KG 1B' WHERE current_grade = 'Nursery 2B'""")
            c.execute("""UPDATE students
            SET current_class = 'KG 1A' WHERE current_class = 'Nursery 2A'""")
            c.execute("""UPDATE students
            SET current_class = 'KG 1B' WHERE current_class = 'Nursery 2B'""")
            c.execute("""UPDATE students
            SET grade = 'KG 1' WHERE grade = 'Nursery 2'""")
            # c.execute("""UPDATE students
            # SET grade = 'KG 1B' WHERE grade = 'Nursery 2B'""")

            conn.commit()
            conn.close()

            conn = sqlite3.connect("school.db")
            c = conn.cursor()
            c.execute("""UPDATE fees_payable
            SET grade = 'Nursery 2' WHERE grade = 'Nursery 1'""")
            c.execute("""UPDATE fees_payable
            SET grade_and_category = 'Nursery 2A' WHERE grade_and_category = 'Nursery 1A'""")
            c.execute("""UPDATE fees_payable
            SET grade_and_category = 'Nursery 2B' WHERE grade_and_category = 'Nursery 1B'""")
            c.execute("""UPDATE fees_paid
            SET current_grade = 'Nursery 2A' WHERE current_grade = 'Nursery 1A'""")
            c.execute("""UPDATE fees_paid
            SET current_grade = 'Nursery 2B' WHERE current_grade = 'Nursery 1B'""")
            c.execute("""UPDATE students
            SET current_class = 'Nursery 2A' WHERE current_class = 'Nursery 1A'""")
            c.execute("""UPDATE students
            SET current_class = 'Nursery 2B' WHERE current_class = 'Nursery 1B'""")
            c.execute("""UPDATE students
            SET grade = 'Nursery 2' WHERE grade = 'Nursery 1'""")

            conn.commit()
            conn.close()
        finally:
            self.successful_promotion_dialog = MDDialog(
                title="Successful Promotion!",
                text="All students have been successfully promoted to the next class",
                radius=[40, 7, 40, 7],
                auto_dismiss=False,
                buttons=[
                    MDRectangleFlatButton(
                        text="CLOSE", on_release=self.close_successful_promotion_dialog
                    ),
                ],
            )
            self.successful_promotion_dialog.open()

    def close_successful_promotion_dialog(self, obj):
        self.successful_promotion_dialog.dismiss()

    def confirmation_of_demotion_dialog(self):
        self.confirmation_demotion_dialog = MDDialog(
            title="Warning!",
            text="Clicking 'YES' will move all students a grade back",
            radius=[25, 7, 25, 7],
            auto_dismiss=False,
            buttons=[
                MDRectangleFlatButton(
                    text="YES", on_release=self.reverse_promotion, on_press=self.close_successful_demotion_dialog
                ),
                MDRectangleFlatButton(
                    text="NO", on_release=self.close_successful_demotion_dialog
                ),
            ],
        )
        self.confirmation_demotion_dialog.open()

    def close_successful_demotion_dialog(self, obj):
        self.confirmation_demotion_dialog.dismiss()

    def reverse_promotion(self, obj):
        try:
            conn = sqlite3.connect("school.db")
            c = conn.cursor()
            c.execute(
                """UPDATE fees_payable SET grade = 'Nursery 1' WHERE grade = 'Nursery 2'""")
            c.execute("""UPDATE fees_payable
            SET grade_and_category = 'Nursery 1A' WHERE grade_and_category = 'Nursery 2A'""")
            c.execute("""UPDATE fees_payable
            SET grade_and_category = 'Nursery 1B' WHERE grade_and_category = 'Nursery 2B'""")
            c.execute("""UPDATE fees_paid
            SET current_grade = 'Nursery 1A' WHERE current_grade = 'Nursery 2A'""")
            c.execute("""UPDATE fees_paid
            SET current_grade = 'Nursery 1B' WHERE current_grade = 'Nursery 2B'""")
            c.execute("""UPDATE students
            SET current_class = 'Nursery 1A' WHERE current_class = 'Nursery 2A'""")
            c.execute("""UPDATE students
            SET current_class = 'Nursery 1B' WHERE current_class = 'Nursery 2B'""")
            c.execute("""UPDATE students
            SET grade = 'Nursery 1' WHERE grade = 'Nursery 2'""")
            conn.commit()
            conn.close()

            conn = sqlite3.connect("school.db")
            c = conn.cursor()
            c.execute("""UPDATE fees_payable
                    SET grade = 'Nursery 2' WHERE grade = 'KG 1'""")
            c.execute("""UPDATE fees_payable
            SET grade_and_category = 'Nursery 2A' WHERE grade_and_category = 'KG 1A'""")
            c.execute("""UPDATE fees_payable
            SET grade_and_category = 'Nursery 2B' WHERE grade_and_category = 'KG 1B'""")
            c.execute("""UPDATE fees_paid
            SET current_grade = 'Nursery 2A' WHERE current_grade = 'KG 1A'""")
            c.execute("""UPDATE fees_paid
            SET current_grade = 'Nursery 2B' WHERE current_grade = 'KG 1B'""")
            c.execute("""UPDATE students
            SET current_class = 'Nursery 2A' WHERE current_class = 'KG 1A'""")
            c.execute("""UPDATE students
            SET current_class = 'Nursery 2B' WHERE current_class = 'KG 1B'""")
            c.execute("""UPDATE students
            SET grade = 'Nursery 2' WHERE grade = 'KG 1'""")
            conn.commit()
            conn.close()

            conn = sqlite3.connect("school.db")
            c = conn.cursor()
            c.execute(
                """UPDATE fees_payable SET grade = 'KG 1' WHERE grade = 'KG 2'""")
            c.execute("""UPDATE fees_payable
            SET grade_and_category = 'KG 1A' WHERE grade_and_category = 'KG 2A'""")
            c.execute("""UPDATE fees_payable
            SET grade_and_category = 'KG 1B' WHERE grade_and_category = 'KG 2B'""")
            c.execute("""UPDATE fees_paid
            SET current_grade = 'KG 1A' WHERE current_grade = 'KG 2A'""")
            c.execute("""UPDATE fees_paid
            SET current_grade = 'KG 1B' WHERE current_grade = 'KG 2B'""")
            c.execute("""UPDATE students
            SET current_class = 'KG 1A' WHERE current_class = 'KG 2A'""")
            c.execute("""UPDATE students
            SET current_class = 'KG 1B' WHERE current_class = 'KG 2B'""")
            c.execute("""UPDATE students
            SET grade = 'KG 1' WHERE grade = 'KG 2'""")
            conn.commit()
            conn.close()

            conn = sqlite3.connect("school.db")
            c = conn.cursor()
            c.execute("""UPDATE fees_payable
                SET grade = 'KG 2' WHERE grade = 'Grade 1'""")
            c.execute("""UPDATE fees_payable
            SET grade_and_category = 'KG 2A' WHERE grade_and_category = 'Grade 1A'""")
            c.execute("""UPDATE fees_payable
            SET grade_and_category = 'KG 2B' WHERE grade_and_category = 'Grade 1B'""")
            c.execute("""UPDATE fees_paid
            SET current_grade = 'KG 2A' WHERE current_grade = 'Grade 1A'""")
            c.execute("""UPDATE fees_paid
            SET current_grade = 'KG 2B' WHERE current_grade = 'Grade 1B'""")
            c.execute("""UPDATE students
            SET current_class = 'KG 2A' WHERE current_class = 'Grade 1A'""")
            c.execute("""UPDATE students
            SET current_class = 'KG 2B' WHERE current_class = 'Grade 1B'""")
            c.execute("""UPDATE students
            SET grade = 'KG 2' WHERE grade = 'Grade 1'""")
            conn.commit()
            conn.close()

            conn = sqlite3.connect("school.db")
            c = conn.cursor()
            c.execute("""UPDATE fees_payable
                SET grade = 'Grade 1' WHERE grade = 'Grade 2'""")
            c.execute("""UPDATE fees_payable
            SET grade_and_category = 'Grade 1A' WHERE grade_and_category = 'Grade 2A'""")
            c.execute("""UPDATE fees_payable
            SET grade_and_category = 'Grade 1B' WHERE grade_and_category = 'Grade 2B'""")
            c.execute("""UPDATE fees_paid
            SET current_grade = 'Grade 1A' WHERE current_grade = 'Grade 2A'""")
            c.execute("""UPDATE fees_paid
            SET current_grade = 'Grade 1B' WHERE current_grade = 'Grade 2B'""")
            c.execute("""UPDATE students
            SET current_class = 'Grade 1A' WHERE current_class = 'Grade 2A'""")
            c.execute("""UPDATE students
            SET current_class = 'Grade 1B' WHERE current_class = 'Grade 2B'""")
            c.execute("""UPDATE students
            SET grade = 'Grade 1' WHERE grade = 'Grade 2'""")
            conn.commit()
            conn.close()

            conn = sqlite3.connect("school.db")
            c = conn.cursor()
            c.execute("""UPDATE fees_payable
                SET grade = 'Grade 2' WHERE grade = 'Grade 3'""")
            c.execute("""UPDATE fees_payable
            SET grade_and_category = 'Grade 2A' WHERE grade_and_category = 'Grade 3A'""")
            c.execute("""UPDATE fees_payable
            SET grade_and_category = 'Grade 2B' WHERE grade_and_category = 'Grade 3B'""")
            c.execute("""UPDATE fees_paid
            SET current_grade = 'Grade 2A' WHERE current_grade = 'Grade 3A'""")
            c.execute("""UPDATE fees_paid
            SET current_grade = 'Grade 2B' WHERE current_grade = 'Grade 3B'""")
            c.execute("""UPDATE students
            SET current_class = 'Grade 2A' WHERE current_class = 'Grade 3A'""")
            c.execute("""UPDATE students
            SET current_class = 'Grade 2B' WHERE current_class = 'Grade 3B'""")
            c.execute("""UPDATE students
            SET grade = 'Grade 2' WHERE grade = 'Grade 3'""")
            conn.commit()
            conn.close()

            conn = sqlite3.connect("school.db")
            c = conn.cursor()
            c.execute("""UPDATE fees_payable
                    SET grade = 'Grade 3' WHERE grade = 'Grade 4'""")
            c.execute("""UPDATE fees_payable
            SET grade_and_category = 'Grade 3A' WHERE grade_and_category = 'Grade 4A'""")
            c.execute("""UPDATE fees_payable
            SET grade_and_category = 'Grade 3B' WHERE grade_and_category = 'Grade 4B'""")
            c.execute("""UPDATE fees_paid
            SET current_grade = 'Grade 3A' WHERE current_grade = 'Grade 4A'""")
            c.execute("""UPDATE fees_paid
            SET current_grade = 'Grade 3B' WHERE current_grade = 'Grade 4B'""")
            c.execute("""UPDATE students
            SET current_class = 'Grade 3A' WHERE current_class = 'Grade 4A'""")
            c.execute("""UPDATE students
            SET current_class = 'Grade 3B' WHERE current_class = 'Grade 4B'""")
            c.execute("""UPDATE students
            SET grade = 'Grade 3' WHERE grade = 'Grade 4'""")
            conn.commit()
            conn.close()

            conn = sqlite3.connect("school.db")
            c = conn.cursor()
            c.execute("""UPDATE fees_payable
                    SET grade = 'Grade 4' WHERE grade = 'Grade 5'""")
            c.execute("""UPDATE fees_payable
            SET grade_and_category = 'Grade 4A' WHERE grade_and_category = 'Grade 5A'""")
            c.execute("""UPDATE fees_payable
            SET grade_and_category = 'Grade 4B' WHERE grade_and_category = 'Grade 5B'""")
            c.execute("""UPDATE fees_paid
            SET current_grade = 'Grade 4A' WHERE current_grade = 'Grade 5A'""")
            c.execute("""UPDATE fees_paid
            SET current_grade = 'Grade 4B' WHERE current_grade = 'Grade 5B'""")
            c.execute("""UPDATE students
            SET current_class = 'Grade 4A' WHERE current_class = 'Grade 5A'""")
            c.execute("""UPDATE students
            SET current_class = 'Grade 4B' WHERE current_class = 'Grade 5B'""")
            c.execute("""UPDATE students
            SET grade = 'Grade 4' WHERE grade = 'Grade 5'""")
            conn.commit()
            conn.close()

            conn = sqlite3.connect("school.db")
            c = conn.cursor()
            c.execute("""UPDATE fees_payable
                SET grade = 'Grade 5' WHERE grade = 'Grade 6'""")
            c.execute("""UPDATE fees_payable
            SET grade_and_category = 'Grade 5A' WHERE grade_and_category = 'Grade 6A'""")
            c.execute("""UPDATE fees_payable
            SET grade_and_category = 'Grade 5B' WHERE grade_and_category = 'Grade 6B'""")
            c.execute("""UPDATE fees_paid
            SET current_grade = 'Grade 5A' WHERE current_grade = 'Grade 6A'""")
            c.execute("""UPDATE fees_paid
            SET current_grade = 'Grade 5B' WHERE current_grade = 'Grade 6B'""")
            c.execute("""UPDATE students
            SET current_class = 'Grade 5A' WHERE current_class = 'Grade 6A'""")
            c.execute("""UPDATE students
            SET current_class = 'Grade 5B' WHERE current_class = 'Grade 6B'""")
            c.execute("""UPDATE students
            SET grade = 'Grade 5' WHERE grade = 'Grade 6'""")
            conn.commit()
            conn.close()

            conn = sqlite3.connect("school.db")
            c = conn.cursor()
            c.execute("""UPDATE fees_payable
                SET grade = 'Grade 6' WHERE grade = 'Grade 7'""")
            c.execute("""UPDATE fees_payable
            SET grade_and_category = 'Grade 6A' WHERE grade_and_category = 'Grade 7A'""")
            c.execute("""UPDATE fees_payable
            SET grade_and_category = 'Grade 6B' WHERE grade_and_category = 'Grade 7B'""")
            c.execute("""UPDATE fees_paid
            SET current_grade = 'Grade 6A' WHERE current_grade = 'Grade 7A'""")
            c.execute("""UPDATE fees_paid
            SET current_grade = 'Grade 6B' WHERE current_grade = 'Grade 7B'""")
            c.execute("""UPDATE students
            SET current_class = 'Grade 6A' WHERE current_class = 'Grade 7A'""")
            c.execute("""UPDATE students
            SET current_class = 'Grade 6B' WHERE current_class = 'Grade 7B'""")
            c.execute("""UPDATE students
            SET grade = 'Grade 6' WHERE grade = 'Grade 7'""")
            conn.commit()
            conn.close()

            conn = sqlite3.connect("school.db")
            c = conn.cursor()
            c.execute("""UPDATE fees_payable
                SET grade = 'Grade 7' WHERE grade = 'Grade 8'""")
            c.execute("""UPDATE fees_payable
            SET grade_and_category = 'Grade 7A' WHERE grade_and_category = 'Grade 8A'""")
            c.execute("""UPDATE fees_payable
            SET grade_and_category = 'Grade 7B' WHERE grade_and_category = 'Grade 8B'""")
            c.execute("""UPDATE fees_paid
            SET current_grade = 'Grade 7A' WHERE current_grade = 'Grade 8A'""")
            c.execute("""UPDATE fees_paid
            SET current_grade = 'Grade 7B' WHERE current_grade = 'Grade 8B'""")
            c.execute("""UPDATE students
            SET current_class = 'Grade 7A' WHERE current_class = 'Grade 8A'""")
            c.execute("""UPDATE students
            SET current_class = 'Grade 7B' WHERE current_class = 'Grade 8B'""")
            c.execute("""UPDATE students
            SET grade = 'Grade 7' WHERE grade = 'Grade 8'""")
            conn.commit()
            conn.close()

            conn = sqlite3.connect("school.db")
            c = conn.cursor()
            c.execute("""UPDATE fees_payable
            SET grade = 'Grade 8' WHERE grade = 'Grade 9'""")
            c.execute("""UPDATE fees_payable
            SET grade_and_category = 'Grade 8A' WHERE grade_and_category = 'Grade 9A'""")
            c.execute("""UPDATE fees_payable
            SET grade_and_category = 'Grade 8B' WHERE grade_and_category = 'Grade 9B'""")
            c.execute("""UPDATE fees_paid
            SET current_grade = 'Grade 8A' WHERE current_grade = 'Grade 9A'""")
            c.execute("""UPDATE fees_paid
            SET current_grade = 'Grade 8B' WHERE current_grade = 'Grade 9B'""")
            c.execute("""UPDATE students
            SET current_class = 'Grade 8A' WHERE current_class = 'Grade 9A'""")
            c.execute("""UPDATE students
            SET current_class = 'Grade 8B' WHERE current_class = 'Grade 9B'""")
            c.execute("""UPDATE students
            SET grade = 'Grade 8' WHERE grade = 'Grade 9'""")
            conn.commit()
            conn.close()

            conn = sqlite3.connect("school.db")
            c = conn.cursor()
            c.execute("""UPDATE fees_paid
            SET current_grade = 'Grade 9A' WHERE current_grade = 'Completed A'""")
            c.execute("""UPDATE fees_paid
            SET current_grade = 'Grade 9B' WHERE current_grade = 'Completed B'""")
            c.execute(
                """INSERT OR IGNORE INTO fees_payable(full_name, registration_number, grade, grade_and_category,
                        status, balance)
                    SELECT full_name, registration_number, grade, grade_and_category, status, arrears
                    FROM completed_students
                    WHERE completed_students.completion_level = 'c'""")
            conn.commit()
            conn.close()

            conn = sqlite3.connect("school.db")
            c = conn.cursor()
            c.execute(
                """DELETE FROM completed_students WHERE completed_students.completion_level = 'c'""")
            conn.commit()
            conn.close()

        finally:
            self.successful_promotion_dialog = MDDialog(
                title="Successful Demoted Students!",
                text="All students have been successfully moved to the previous class.",
                radius=[40, 7, 40, 7],
                auto_dismiss=False,
                buttons=[
                    MDRectangleFlatButton(
                        text="CLOSE", on_release=self.close_successful_promotion_dialog
                    ),
                ],
            )
            self.successful_promotion_dialog.open()

    def close_successful_promotion_dialog(self, obj):
        self.successful_promotion_dialog.dismiss()


    def logout(self):
        self.empty_class_dialog = MDDialog(
            title="Logging out...",
            text="Are you sure you want to log out?",
            buttons=[
                MDRectangleFlatButton(
                    text="YES", on_release=self.close_dialog_and_logout
                ),
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


class SetSecuritykey(Screen):
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


class SetTerm(Screen):
    def on_save_start(self, instance, value, date_range):
        self.ids.start_date_of_term.text = str(value)

    def on_cancel_start(self, instance, value):
        self.ids.start_date_of_term.text = "Start of term date not selected"

    def show_start_date(self):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_save_start,
                         on_cancel=self.on_cancel_start)
        date_dialog.open()

    def on_save_end(self, instance, value, date_range):
        self.ids.end_date_of_term.text = str(value)

    def on_cancel_end(self, instance, value):
        self.ids.end_date_of_term.text = "End of term date not selected"

    def show_end_date(self):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_save_end,
                         on_cancel=self.on_cancel_end)
        date_dialog.open()

    def set_term(self):
        try:
            if self.ids.start_date_of_term.text == "Start of Term" or self.ids.end_date_of_term.text == "  End of Term  ":
                raise exceptions.EmptyFieldError
            if self.ids.select_term_spinner.text == "Select Term":
                raise exceptions.EmptyClassSpinnerError
            conn = sqlite3.connect("school.db")
            c = conn.cursor()

            c.execute(
                """UPDATE set_fees
                    SET
                    start_of_term = ?,
                    end_of_term = ?
                    """, (self.ids.start_date_of_term.text, self.ids.end_date_of_term.text,))
            c.execute(
                """UPDATE fees_payable
                    SET
                    start_term = ?,
                    end_term = ?
                    """, (self.ids.start_date_of_term.text, self.ids.end_date_of_term.text,))

        except exceptions.EmptyFieldError:
            self.term_selection_dialog = MDDialog(
                title="Warning!",
                text="Start of term and end of term must be selected.",
                radius=[40, 7, 40, 7],
                buttons=[
                    MDRectangleFlatButton(
                        text="OK", on_release=self.close_term_selection_dialog,
                    ),
                ],
            )
            self.term_selection_dialog.open()
        except exceptions.EmptyClassSpinnerError:
            self.term_selection_dialog = MDDialog(
                title="Empty!",
                text="Please select the term to proceed",
                radius=[40, 7, 40, 7],
                buttons=[
                    MDRectangleFlatButton(
                        text="OK", on_release=self.close_term_selection_dialog,
                    ),
                ],
            )
            self.term_selection_dialog.open()
        else:
            conn.commit()
            self.success_term_selection_dialog = MDDialog(
                title="Success!",
                text=f"You have selected {self.ids.start_date_of_term.text} to {self.ids.end_date_of_term.text} as term dates",
                radius=[40, 7, 40, 7],
                buttons=[
                    MDRectangleFlatButton(
                        text="NEXT", on_release=self.close_success_term_selection_dialog,
                    ),
                ],
            )
            self.success_term_selection_dialog.open()

    def close_term_selection_dialog(self, obj):
        self.term_selection_dialog.dismiss()

    def close_success_term_selection_dialog(self, obj):
        self.success_term_selection_dialog.dismiss()
        self.manager.current = "set"

    def set_term_dialog(self):
        self.term_dialog = MDDialog(
            title="Confirm",
            text="Are you sure you want to set term?",
            radius=[25, 7, 25, 7],
            auto_dismiss=False,
            buttons=[
                MDRectangleFlatButton(
                    text="YES", on_release=self.set_term, on_press=self.close_term_dialog
                ),
            ],
        )
        self.term_dialog.open()

    def close_term_dialog(self, obj):
        self.term_dialog.dismiss()

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


class SetFeesClassSelection(Screen):
    # grade_spinner = Spinner()
    conn = sqlite3.connect("school.db")
    c = conn.cursor()
    values = [r[0]
              for r in c.execute("SELECT available_grades FROM grades")]
    grades = values

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


class DifferentiatedSalary(Screen):
    def show_staff_names(self, value):
        conn = sqlite3.connect("school.db")
        c = conn.cursor()
        names = [r[0] for r in c.execute(
            "SELECT full_name FROM differentiated_salary_payable")]
        if self.ids.reset_staff_name_spinner.text == "Yes":
            self.ids.select_staff_name_spinner.values = names
        else:
            self.ids.select_staff_name_spinner.values = ["Select Staff Name"]

    def set_differentiated_salary_dialog(self):
        self.differentiated_salary_dialog = MDDialog(
            title="Confirm",
            text="Are you sure you want to set salary?",
            buttons=[
                MDRectangleFlatButton(
                    text="close", on_release=self.set_differentiated_salary
                ),
            ],
        )
        self.differentiated_salary_dialog.open()

    def close_differentiated_salary_dialog(self, obj):
        self.differentiated_salary_dialog.dismiss()

    def set_differentiated_salary(self):
        try:
            the_date = datetime.datetime.today()
            self.date = the_date.replace(microsecond=0)
            if self.ids.reset_staff_name_spinner.text == "Reset Differentiated Salary":
                raise exceptions.EmptyFieldError
            if self.ids.select_staff_name_spinner.text == "Select Staff Name":
                raise exceptions.EmptyFieldError
            conn = sqlite3.connect("school.db")
            c = conn.cursor()

            c.execute(
                """UPDATE differentiated_salary_payable
                    SET
                    date_set = ?,
                    base_salary = ?,
                    studies = ?,
                    honourarium = ?,
                    motivation = ?,
                    bonus = ?,
                    ssnit_contibution = ?,
                    income_tax = ?,
                    welfare = ?,
                    total_salary = ?
                    WHERE differentiated_salary_payable.full_name=?
                    """, (self.date, self.ids.base_salary.text,
                          self.ids.staff_studies.text, self.ids.honourarium.text,
                          self.ids.staff_motivation.text, self.ids.bonus.text,
                          self.ids.ssnit_contibution.text, self.ids.income_tax.text,
                          self.ids.staff_welfare.text, 0, self.ids.select_staff_name_spinner.text,))
            c.execute(
                """UPDATE differentiated_salary_payable
                    SET total_salary = base_salary + studies + honourarium +
                    motivation + bonus - ssnit_contibution - income_tax + welfare
                """)
            c.execute(
                """UPDATE salary_payable
                    SET salary = total_salary
                    FROM differentiated_salary_payable
                    WHERE differentiated_salary_payable.full_name = salary_payable.staff_full_name
                """)

        except exceptions.EmptyFieldError:
            self.incomplete_dialog = MDDialog(
                title="Empty Fields",
                text="Select a reset option, and name of the differentiated staff member",
                buttons=[
                    MDRectangleFlatButton(
                        text="Edit", on_release=self.close_incomplete_dialog
                    ),
                    MDFlatButton(
                        text="CANCEL", on_release=self.close_incomplete_dialog
                    ),
                ],
            )
            self.incomplete_dialog.open()

        else:
            conn.commit()
            self.ids.base_salary.text = ""
            self.ids.staff_studies.text = ""
            self.ids.honourarium.text = ""
            self.ids.staff_motivation.text = ""
            self.ids.bonus.text = ""
            self.ids.ssnit_contibution.text = ""
            self.ids.income_tax.text = ""
            self.ids.staff_welfare.text = ""
            self.ids.reset_staff_name_spinner.text = "Reset Differentiated Salary"
            self.ids.reset_staff_name_spinner.background_color = .7, 0, 0, .9
            self.ids.select_staff_name_spinner.text = "Select Staff Name"
            self.ids.select_staff_name_spinner.background_color = .7, 0, 0, .9
            self.ids.previous_total.text = "Previous total salary shows here"
            self.ids.current_total.text = "Current total salary shows here"
            self.successful_transaction_dialog = MDDialog(
                title="Success!",
                text=f"You have set a new salary for {self.ids.select_staff_name_spinner.text}",
                radius=[40, 7, 40, 7],
                auto_dismiss=False,
                buttons=[
                    MDRectangleFlatButton(
                        text="CLOSE", on_release=self.close_successful_transaction_dialog)
                ],
            )

            self.successful_transaction_dialog.open()

    def close_successful_transaction_dialog(self, obj):
        self.successful_transaction_dialog.dismiss()

    def show_current_total(self):
        conn = sqlite3.connect("school.db")
        c = conn.cursor()

        c.execute(
            """UPDATE differentiated_salary_payable
                SET
                base_salary = ?,
                studies = ?,
                honourarium = ?,
                motivation = ?,
                bonus = ?,
                ssnit_contibution = ?,
                income_tax = ?,
                welfare = ?,
                total_salary = ?
                WHERE differentiated_salary_payable.full_name=?
                """, (self.ids.base_salary.text,
                      self.ids.staff_studies.text, self.ids.honourarium.text,
                      self.ids.staff_motivation.text, self.ids.bonus.text,
                      self.ids.ssnit_contibution.text, self.ids.income_tax.text,
                      self.ids.staff_welfare.text, 0, self.ids.select_staff_name_spinner.text,))
        c.execute(
            """UPDATE differentiated_salary_payable
                SET total_salary = base_salary + studies + honourarium +
                motivation + bonus - ssnit_contibution - income_tax + welfare
            """)
        parameter_search = c.execute(
            """SELECT total_salary FROM differentiated_salary_payable WHERE full_name=?
                """, (self.ids.select_staff_name_spinner.text,))
        for row in parameter_search:
            self.ids.current_total.text = f"GHC{row[0]}"
        conn.close()

    def show_previous_total(self):
        the_date = datetime.datetime.today()
        self.date = the_date.replace(microsecond=0)
        conn = sqlite3.connect("school.db")
        c = conn.cursor()

        parameter_search = c.execute(
            """SELECT total_salary FROM differentiated_salary_payable WHERE full_name=?
                """, (self.ids.select_staff_name_spinner.text,))
        for row in parameter_search:
            self.ids.previous_total.text = f"GHC{row[0]}"
        conn.close()

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


class FeesBreakdown(Screen):
    # grade_spinner = Spinner()
    conn = sqlite3.connect("school.db")
    c = conn.cursor()
    values = [r[0]
              for r in c.execute("SELECT available_grades FROM grades")]
    grades = values

    def show_previous_fees_total(self):
        conn = sqlite3.connect("school.db")
        c = conn.cursor()
        parameter_search = c.execute(
            """SELECT total_with_boarding FROM set_fees WHERE grade=?
                """, (self.ids.select_level_grade_spinner.text,))
        for row in parameter_search:
            self.ids.previous_fees_total.text = f"GHC{row[0]}"
        conn.close()

    def show_previous_fees_w_o_total(self):
        conn = sqlite3.connect("school.db")
        c = conn.cursor()
        parameter_search = c.execute(
            """SELECT total_without_boarding FROM set_fees WHERE grade=?
                """, (self.ids.select_level_grade_spinner.text,))
        for row in parameter_search:
            self.ids.previous_fees_w_o_boarding_total.text = f"GHC{row[0]}"
        conn.close()

    def show_current_fees_total(self):
        conn = sqlite3.connect("school.db")
        c = conn.cursor()
        c.execute(
            """UPDATE set_fees
                SET
                tuition = ?,
                studies = ?,
                pta_levy = ?,
                printing = ?,
                maintenance = ?,
                motivation = ?,
                library = ?,
                canteen = ?,
                sanitation = ?,
                sports = ?,
                boarding_fees = ?
                WHERE set_fees.grade=?
                """, (self.ids.tuition.text, self.ids.studies.text, self.ids.pta_levy.text,
                      self.ids.printing.text, self.ids.maintenance.text, self.ids.motivation.text,
                      self.ids.library.text, self.ids.can_teen.text, self.ids.sanitation.text,
                      self.ids.sports.text, self.ids.boarding_fees.text,
                      self.ids.select_level_grade_spinner.text,))

        c.execute(
            """UPDATE set_fees
                SET total_with_boarding = tuition + studies + pta_levy + printing +
                maintenance + motivation + library + canteen + sanitation + sports +
                boarding_fees""")

        parameter_search = c.execute(
            """SELECT total_with_boarding FROM set_fees WHERE grade=?
                """, (self.ids.select_level_grade_spinner.text,))
        for row in parameter_search:
            self.ids.current_fee_total.text = f"GHC{row[0]}"
        conn.close()

    def show_current_fees_w_o_total(self):
        conn = sqlite3.connect("school.db")
        c = conn.cursor()
        c.execute(
            """UPDATE set_fees
                SET
                tuition = ?,
                studies = ?,
                pta_levy = ?,
                printing = ?,
                maintenance = ?,
                motivation = ?,
                library = ?,
                canteen = ?,
                sanitation = ?,
                sports = ?,
                boarding_fees = ?
                WHERE set_fees.grade=?
                """, (self.ids.tuition.text, self.ids.studies.text, self.ids.pta_levy.text,
                      self.ids.printing.text, self.ids.maintenance.text, self.ids.motivation.text,
                      self.ids.library.text, self.ids.can_teen.text, self.ids.sanitation.text,
                      self.ids.sports.text, self.ids.boarding_fees.text,
                      self.ids.select_level_grade_spinner.text,))

        c.execute(
            """UPDATE set_fees
                SET total_without_boarding = tuition + studies + pta_levy +
                printing + maintenance + motivation + library + canteen +
                sanitation + sports
            """)

        parameter_search = c.execute(
            """SELECT total_without_boarding FROM set_fees WHERE grade=?
                """, (self.ids.select_level_grade_spinner.text,))
        for row in parameter_search:
            self.ids.current_fee_w_o_boarding_total.text = f"GHC{row[0]}"
        conn.close()

    def spinner_clicked(self, value):
        self.ids.text = value
        return value

    def taking_fees_to_(self):
        pass

    def confirm_set_fees(self):
        self.confirm_set_fees_dialog = MDDialog(
            title="Confirmation!",
            text=f"Do you want to set fees for {self.ids.select_level_grade_spinner.text}?",
            radius=[40, 7, 40, 7],
            auto_dismiss=False,
            buttons=[
                MDRectangleFlatButton(
                    text="YES", on_press=self.set_fees, on_release=self.close_confirm_set_fees_dialog
                ),
                MDFlatButton(
                    text="NO", on_release=self.close_confirm_set_fees_dialog
                )
            ],
        )

        self.confirm_set_fees_dialog.open()

    def close_confirm_set_fees_dialog(self, obj):
        self.confirm_set_fees_dialog.dismiss()

    def set_fees(self, obj):
        the_date = datetime.datetime.today()
        self.date = the_date.replace(microsecond=0)
        conn = sqlite3.connect("school.db")
        c = conn.cursor()
        c.execute(
            """UPDATE set_fees SET total_without_boarding = 0.0, total_with_boarding = 0.0
                WHERE set_fees.term != ?""", (self.ids.select_term_spinner.text,))
        conn.commit()
        total_without_boarding = [r[0] for r in c.execute("""SELECT total_without_boarding FROM set_fees
                WHERE grade =?""", (self.ids.select_level_grade_spinner.text,))]
        total_with_boarding = [r[0] for r in c.execute("""SELECT total_with_boarding FROM set_fees
                WHERE grade =?""", (self.ids.select_level_grade_spinner.text,))]
        try:
            # if total_without_boarding != 0.0 and total_with_boarding != 0.0:
            #     raise DuplicateFeesError
            c.execute(
                """UPDATE set_fees
                    SET
                    tuition = ?,
                    studies = ?,
                    pta_levy = ?,
                    printing = ?,
                    maintenance = ?,
                    motivation = ?,
                    library = ?,
                    canteen = ?,
                    sanitation = ?,
                    sports = ?,
                    boarding_fees = ?,
                    time_set = ?
                    WHERE set_fees.grade=?
                    """, (self.ids.tuition.text,
                          self.ids.studies.text, self.ids.pta_levy.text, self.ids.printing.text,
                          self.ids.maintenance.text, self.ids.motivation.text, self.ids.library.text,
                          self.ids.can_teen.text, self.ids.sanitation.text, self.ids.sports.text,
                          self.ids.boarding_fees.text, self.date,
                          self.ids.select_level_grade_spinner.text))

            c.execute(
                """UPDATE set_fees
                    SET total_without_boarding = tuition + studies + pta_levy +
                    printing + maintenance + motivation + library + canteen +
                    sanitation + sports
                """)

            c.execute(
                """UPDATE set_fees
                    SET total_with_boarding = tuition + studies + pta_levy + printing +
                    maintenance + motivation + library + canteen + sanitation + sports +
                    boarding_fees""")

            c.execute("""
                    UPDATE fees_payable
                    SET balance = balance + set_fees.total_without_boarding
                    FROM set_fees
                    WHERE set_fees.grade = fees_payable.grade
                    AND fees_payable.grade = ?
                    AND fees_payable.status = 'Day'""",
                      (self.ids.select_level_grade_spinner.text,))

            c.execute("""
                    UPDATE fees_payable
                    SET balance = balance + set_fees.total_with_boarding
                    FROM set_fees
                    WHERE set_fees.grade = fees_payable.grade
                    AND fees_payable.grade = ?
                    AND fees_payable.status = 'Boarding'""",
                      (self.ids.select_level_grade_spinner.text,))
            c.execute(
                """INSERT INTO set_fees_history VALUES (:time_set, :term, :grade, :tuition,
                :studies, :pta_levy, :printing, :maintenance, :motivation, :library, :canteen,
                :sanitation, :sports, :boarding_fees, :total_without_boarding,
                :total_with_boarding)""",
                {
                    'time_set': self.date,
                    'term': self.ids.select_term_spinner.text,
                    'grade': self.ids.select_level_grade_spinner.text,
                    'tuition': self.ids.tuition.text,
                    'studies': self.ids.studies.text,
                    'pta_levy': self.ids.pta_levy.text,
                    'printing': self.ids.printing.text,
                    'maintenance': self.ids.maintenance.text,
                    'motivation': self.ids.motivation.text,
                    'library': self.ids.library.text,
                    'canteen': self.ids.can_teen.text,
                    'sanitation': self.ids.sanitation.text,
                    'sports': self.ids.sports.text,
                    'boarding_fees': self.ids.boarding_fees.text,
                    'total_without_boarding': "",
                    'total_with_boarding': "",



                })

            c.execute(
                """UPDATE set_fees_history
                    SET total_without_boarding = tuition + studies + pta_levy +
                    printing + maintenance + motivation + library + canteen +
                    sanitation + sports
                """)

            c.execute(
                """UPDATE set_fees_history
                    SET total_with_boarding = tuition + studies + pta_levy + printing +
                    maintenance + motivation + library + canteen + sanitation + sports +
            boarding_fees""")

        except exceptions.DuplicateFeesError:
            self.duplicate_fees_dialog = MDDialog(
                title="Warning!",
                text=f"You have already set fees for {self.ids.select_level_grade_spinner.text} ",
                radius=[40, 7, 40, 7],
                auto_dismiss=False,
                buttons=[
                    MDRectangleFlatButton(
                        text="CLOSE", on_release=self.close_duplicate_fees_dialog
                    )
                ],
            )

            self.duplicate_fees_dialog.open()
        else:
            conn.commit()
            self.successful_fees_setting_dialog = MDDialog(
                title="Success!",
                text=f"You have successfully set fees for {self.ids.select_level_grade_spinner.text} ",
                radius=[40, 7, 40, 7],
                auto_dismiss=False,
                buttons=[
                    MDRectangleFlatButton(
                        text="CLOSE", on_release=self.close_successful_fees_setting_dialog
                    )
                ],
            )

            self.successful_fees_setting_dialog.open()

    def close_successful_fees_setting_dialog(self, obj):
        self.successful_fees_setting_dialog.dismiss()

    def close_duplicate_fees_dialog(self, obj):
        self.duplicate_fees_dialog.dismiss()
        # print(self.ids.select_term_spinner.text)
    #     c.execute(
    #         """UPDATE set_fees SET total_without_boarding = 0.0, total_with_boarding = 0.0
    #             WHERE set_fees.term != ?""", (self.ids.select_term_spinner.text,))
    #     conn.commit()
    #     total_without_boarding = [r[0] for r in c.execute("""SELECT total_without_boarding FROM set_fees
    #             WHERE grade =?""", (self.ids.select_level_grade_spinner.text,))]
    #     total_with_boarding = [r[0] for r in c.execute("""SELECT total_with_boarding FROM set_fees
    #             WHERE grade =?""", (self.ids.select_level_grade_spinner.text,))]
    #     try:
    #         if total_without_boarding != 0.0 and total_with_boarding != 0.0:
    #             raise exceptions.DuplicateFeesError
    #         c.execute(
    #             """UPDATE set_fees
    #                 SET
    #                 tuition = ?,
    #                 studies = ?,
    #                 pta_levy = ?,
    #                 printing = ?,
    #                 maintenance = ?,
    #                 motivation = ?,
    #                 library = ?,
    #                 canteen = ?,
    #                 sanitation = ?,
    #                 sports = ?,
    #                 boarding_fees = ?,
    #                 time_set = ?
    #                 WHERE set_fees.grade=?
    #                 """, (self.ids.tuition.text,
    #                       self.ids.studies.text, self.ids.pta_levy.text, self.ids.printing.text,
    #                       self.ids.maintenance.text, self.ids.motivation.text, self.ids.library.text,
    #                       self.ids.can_teen.text, self.ids.sanitation.text, self.ids.sports.text,
    #                       self.ids.boarding_fees.text, self.date,
    #                       self.ids.select_level_grade_spinner.text, self.ids.select_term_spinner.text))

    #         c.execute(
    #             """UPDATE set_fees
    #                 SET total_without_boarding = tuition + studies + pta_levy +
    #                 printing + maintenance + motivation + library + canteen +
    #                 sanitation + sports
    #             """)

    #         c.execute(
    #             """UPDATE set_fees
    #                 SET total_with_boarding = tuition + studies + pta_levy + printing +
    #                 maintenance + motivation + library + canteen + sanitation + sports +
    #                 boarding_fees""")

    #         c.execute("""
    #                 UPDATE fees_payable
    #                 SET balance = balance + set_fees.total_without_boarding
    #                 FROM set_fees
    #                 WHERE set_fees.grade = fees_payable.grade
    #                 AND fees_payable.grade = ?
    #                 AND fees_payable.status = 'Day'""",
    #                   (self.ids.select_level_grade_spinner.text,))

    #         c.execute("""
    #                 UPDATE fees_payable
    #                 SET balance = balance + set_fees.total_with_boarding
    #                 FROM set_fees
    #                 WHERE set_fees.grade = fees_payable.grade
    #                 AND fees_payable.grade = ?
    #                 AND fees_payable.status = 'Boarding'""",
    #                   (self.ids.select_level_grade_spinner.text,))
    #         c.execute(
    #             """INSERT INTO set_fees_history VALUES (:time_set, :term, :grade, :tuition,
    #             :studies, :pta_levy, :printing, :maintenance, :motivation, :library, :canteen,
    #             :sanitation, :sports, :boarding_fees, :total_without_boarding,
    #             :total_with_boarding)""",
    #             {
    #                 'time_set': self.date,
    #                 'term': self.ids.select_term_spinner.text,
    #                 'grade': self.ids.select_level_grade_spinner.text,
    #                 'tuition': self.ids.tuition.text,
    #                 'studies': self.ids.studies.text,
    #                 'pta_levy': self.ids.pta_levy.text,
    #                 'printing': self.ids.printing.text,
    #                 'maintenance': self.ids.maintenance.text,
    #                 'motivation': self.ids.motivation.text,
    #                 'library': self.ids.library.text,
    #                 'canteen': self.ids.can_teen.text,
    #                 'sanitation': self.ids.sanitation.text,
    #                 'sports': self.ids.sports.text,
    #                 'boarding_fees': self.ids.boarding_fees.text,
    #                 'total_without_boarding': "",
    #                 'total_with_boarding': "",

    #             })

    #         c.execute(
    #             """UPDATE set_fees_history
    #                 SET total_without_boarding = tuition + studies + pta_levy +
    #                 printing + maintenance + motivation + library + canteen +
    #                 sanitation + sports
    #             """)

    #         c.execute(
    #             """UPDATE set_fees_history
    #                 SET total_with_boarding = tuition + studies + pta_levy + printing +
    #                 maintenance + motivation + library + canteen + sanitation + sports +
    #         boarding_fees""")

    #     except exceptions.DuplicateFeesError:
    #         self.duplicate_fees_dialog = MDDialog(
    #             title="Warning!",
    #             text=f"You have already set fees for {self.ids.select_level_grade_spinner.text} ",
    #             radius=[40, 7, 40, 7],
    #             auto_dismiss=False,
    #             buttons=[
    #                 MDRectangleFlatButton(
    #                     text="CLOSE", on_release=self.close_duplicate_fees_dialog
    #                 )
    #             ],
    #         )

    #         self.duplicate_fees_dialog.open()
    #     else:
    #         conn.commit()
    #         self.successful_fees_setting_dialog = MDDialog(
    #             title="Success!",
    #             text=f"You have successfully set fees for {self.ids.select_level_grade_spinner.text} ",
    #             radius=[40, 7, 40, 7],
    #             auto_dismiss=False,
    #             buttons=[
    #                 MDRectangleFlatButton(
    #                     text="CLOSE", on_release=self.close_successful_fees_setting_dialog
    #                 )
    #             ],
    #         )

    #         self.successful_fees_setting_dialog.open()

    # def close_successful_fees_setting_dialog(self, obj):
    #     self.successful_fees_setting_dialog.dismiss()

    # def close_duplicate_fees_dialog(self, obj):
    #     self.duplicate_fees_dialog.dismiss()

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


class SetSalaryForm(Screen):
    def spinner_clicked(self, value):
        self.ids.text = value
        return value

    def set_staff_salary(self):
        the_date = datetime.datetime.today()
        self.date = the_date.replace(microsecond=0)

        conn = sqlite3.connect("school.db")
        c = conn.cursor()
        c.execute(
            """UPDATE set_salary
                SET
                date_set= ?,
                base_salary= ?,
                studies= ?,
                honourarium= ?,
                motivation= ?,
                bonus= ?,
                ssnit_contibution= ?,
                income_tax= ?,
                welfare= ?,
                total_salary= ?
                WHERE set_salary.salary_grade=?
                """, (self.date, self.ids.base_salary.text,
                      self.ids.staff_studies.text, self.ids.honourarium.text,
                      self.ids.staff_motivation.text, self.ids.bonus.text,
                      self.ids.ssnit_contibution.text, self.ids.income_tax.text,
                      self.ids.staff_welfare.text, "", self.ids.select_salary_grade_spinner.text,))

        c.execute(
            """UPDATE set_salary
                SET total_salary=base_salary + studies + honourarium +
                motivation + bonus + ssnit_contibution + income_tax + welfare
            """)

        c.execute("""
                UPDATE salary_payable
                SET salary=total_salary
                FROM set_salary
                WHERE set_salary.salary_grade=salary_payable.salary_grade
                 """)
        c.execute("""
                UPDATE staff
                SET current_salary=total_salary
                FROM set_salary
                WHERE set_salary.salary_grade=staff.salary_grade
                 """)

        conn.commit()
        conn.close()

    def show_previous_total(self):
        conn = sqlite3.connect("school.db")
        c = conn.cursor()
        search = c.execute(
            """SELECT total_salary FROM set_salary WHERE salary_grade=?
                """, (self.ids.select_salary_grade_spinner.text,))
        for row in search:
            self.ids.current_total.text = f"Current Total Salary is {row[0]}"
        conn.close()

    def show_current_total(self):
        conn = sqlite3.connect("school.db")
        c = conn.cursor()
        c.execute(
            """UPDATE set_salary
                SET
                base_salary= ?,
                studies= ?,
                honourarium= ?,
                motivation= ?,
                bonus= ?,
                ssnit_contibution= ?,
                income_tax= ?,
                welfare= ?,
                total_salary= ?
                WHERE set_salary.salary_grade=?
                """, (self.ids.base_salary.text,
                      self.ids.staff_studies.text, self.ids.honourarium.text,
                      self.ids.staff_motivation.text, self.ids.bonus.text,
                      self.ids.ssnit_contibution.text, self.ids.income_tax.text,
                      self.ids.staff_welfare.text, 0, self.ids.select_salary_grade_spinner.text,))
        c.execute(
            """UPDATE set_salary
                SET total_salary=base_salary + studies + honourarium +
                motivation + bonus + ssnit_contibution + income_tax + welfare
            """)
        search = c.execute(
            """SELECT total_salary FROM set_salary WHERE salary_grade=?
                """, (self.ids.select_salary_grade_spinner.text,))
        for row in search:
            self.ids.current_total.text = f"Current Total Salary is {row[0]}"
        conn.close()

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
