import kivy
import sqlite3
import datetime
import src.exceptions as exceptions
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRectangleFlatButton, MDFlatButton
from kivy.metrics import dp
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.pickers import MDDatePicker


class StudentsInformation(Screen):
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


class StudentRegistrationForm(Screen):
    # grade_spinner = Spinner()
    conn = sqlite3.connect("school.db")
    c = conn.cursor()
    values = [r[0]
              for r in c.execute("SELECT available_grades FROM grades")]
    grades = values

    def spinner_clicked(self, value):
        self.ids.text = value
        return value

    def register_student(self):
        try:
            the_date = datetime.datetime.today()
            self.date = the_date.replace(microsecond=0)

            conn = sqlite3.connect("school.db")
            c = conn.cursor()
            c.execute(
                """INSERT INTO students VALUES(:first_name, :surname, :full_name, :student_gender,
                        :registration_number, :dob, :special_health_condition, :father_name,
                        :mother_name, :guardian_name, :parent_guardian_phone, :parent_guardian_email,
                        :parent_guardian_occupation, :date_admitted, :grade, :grade_category,
                        :grade_and_category_admitted_to, :current_class, :status, :completion_level, :completed_arrear)""",
                {
                    'first_name': self.ids.first_name.text,
                    'surname': self.ids.surname.text,
                    'full_name': self.ids.first_name.text + " " + self.ids.surname.text,
                    'student_gender': self.ids.student_gender_spinner.text,
                    'registration_number': self.ids.registration_number.text,
                    'dob': self.ids.dob.text,
                    'special_health_condition': self.ids.special_health_condition.text,
                    'father_name': self.ids.father_name.text,
                    'mother_name': self.ids.mother_name.text,
                    'guardian_name': self.ids.guardian_name.text,
                    'parent_guardian_phone': self.ids.parent_guardian_phone.text,
                    'parent_guardian_email': self.ids.parent_guardian_email.text,
                    'parent_guardian_occupation': self.ids.parent_guardian_occupation.text,
                    'date_admitted': self.date,
                    'grade': self.ids.grade_spinner.text,
                    'grade_category': self.ids.grade_category_spinner.text,
                    'grade_and_category_admitted_to': self.ids.grade_spinner.text + self.ids.grade_category_spinner.text,
                    'current_class': self.ids.grade_spinner.text + self.ids.grade_category_spinner.text,
                    'status': self.ids.status_spinner.text,
                    'completion_level': '',
                    'completed_arrear': '',

                })

            c.execute(
                """INSERT OR IGNORE INTO fees_payable(full_name, registration_number,
                    grade, grade_and_category, status) SELECT full_name, registration_number,
                    grade, grade_and_category_admitted_to, status FROM students
                    WHERE completion_level != 'c'""")

            c.execute("""
                    UPDATE fees_payable SET unique_id=registration_number""")

            c.execute("""
                        UPDATE fees_payable
                        SET balance=set_fees.total_without_boarding
                        FROM set_fees
                        WHERE fees_payable.status='Day'
                        AND fees_payable.grade=set_fees.grade
                        AND fees_payable.registration_number= ?
                        """, (self.ids.registration_number.text,))

            c.execute("""
                        UPDATE fees_payable
                        SET balance=set_fees.total_with_boarding
                        FROM set_fees
                        WHERE fees_payable.status='Boarding'
                        AND fees_payable.grade=set_fees.grade
                        AND fees_payable.registration_number= ?
                        """, (self.ids.registration_number.text,))

            c.execute(
                """UPDATE fees_payable
                        SET
                        start_term=start_of_term FROM set_fees
                        """)

            c.execute(
                """UPDATE fees_payable
                        SET
                        end_term=end_of_term FROM set_fees
                        """)
            conn.commit()
            if self.ids.first_name.text == '' or self.ids.surname.text == '' or self.ids.student_gender_spinner.text == "Select Gender":
                raise exceptions.EmptyFieldError
            elif self.ids.registration_number.text == '' or self.ids.dob.text == '':
                raise exceptions.EmptyFieldError
            elif self.ids.special_health_condition.text == '' or self.ids.mother_name.text == '':
                raise exceptions.EmptyFieldError
            elif self.ids.father_name.text == '' and self.ids.guardian_name.text == '':
                raise exceptions.EmptyFieldError
            elif self.ids.parent_guardian_phone.text == '' or self.ids.parent_guardian_email.text == '':
                raise exceptions.EmptyFieldError
            elif self.ids.parent_guardian_occupation.text == "" or self.ids.grade_spinner.text == "Select class":
                raise exceptions.EmptyFieldError
            elif self.ids.grade_category_spinner.text == "Select grade category":
                raise exceptions.EmptyFieldError
            elif self.ids.status_spinner.text == "Select status":
                raise exceptions.EmptyFieldError

        except sqlite3.IntegrityError:
            self.duplicate_dialog = MDDialog(
                title="Registration Number Duplicate",
                text="Registration number already exists",
                radius=[40, 7, 40, 7],
                auto_dismiss=False,
                buttons=[
                    MDRectangleFlatButton(
                        text="Edit", on_release=self.close_duplicate_dialog
                    ),
                    MDFlatButton(
                        text="CANCEL", on_release=self.close_duplicate_dialog
                    ),
                ],
            )
            self.duplicate_dialog.open()

        except exceptions.EmptyFieldError:
            self.incomplete_dialog = MDDialog(
                title="Incomplete Registration",
                text="All fields are required",
                radius=[25, 7, 25, 7],
                auto_dismiss=False,
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
            self.sucessful_registration_dialog = MDDialog(
                title="Successful Registration",
                text="Student successfully registered",
                radius=[40, 7, 40, 7],
                auto_dismiss=False,
                buttons=[
                    MDRectangleFlatButton(
                        text="CLOSE", on_release=self.close_sucessful_registration_dialog
                    ),
                ],
            )
            self.sucessful_registration_dialog.open()

            self.ids.first_name.text = ''
            self.ids.surname.text = ''
            self.ids.student_gender_spinner.text = "Select Gender"
            self.ids.registration_number.text = ''
            self.ids.dob.text = ''
            self.ids.special_health_condition.text = ''
            self.ids.father_name.text = ''
            self.ids.mother_name.text = ''
            self.ids.guardian_name.text = ''
            self.ids.parent_guardian_phone.text = ''
            self.ids.parent_guardian_email.text = ''
            self.ids.parent_guardian_occupation.text = ""
            self.ids.grade_spinner.text = "Select class"
            self.ids.grade_category_spinner.text = "Select grade category"
            self.ids.status_spinner.text = "Select status"

    def close_incomplete_dialog(self, obj):
        self.incomplete_dialog.dismiss()

    def close_duplicate_dialog(self, obj):
        self.duplicate_dialog.dismiss()

    def close_sucessful_registration_dialog(self, obj):
        self.sucessful_registration_dialog.dismiss()

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


class ViewStudentDetails(Screen):
    student_preview = None
    # grade_spinner = Spinner()
    conn = sqlite3.connect("school.db")
    c = conn.cursor()
    values = [r[0]
              for r in c.execute("SELECT g_and_c FROM grade_and_category")]
    grades = values

    def update_names_spinner(self, value):
        conn = sqlite3.connect("school.db")
        c = conn.cursor()
        names = [r[0]
                 for r in c.execute("""SELECT full_name FROM students WHERE
               students.current_class= ?""", (self.ids.grade_and_category_spinner.text,))]
        all_names = names

        if self.ids.grade_and_category_spinner.text == self.ids.grade_and_category_spinner.text:
            self.ids.students_full_name_spinner.values = all_names

    def preview_students(self):
        try:
            if self.ids.grade_and_category_spinner.text == "Select Class" or self.ids.students_full_name_spinner.text == 'Select Name':
                raise exceptions.EmptyClassSpinnerError
            conn = sqlite3.connect("school.db")
            c = conn.cursor()

            c.execute("""
                UPDATE preview SET Student_data=full_name FROM students WHERE preview.Data='Name'
                AND students.current_class=? AND students.full_name=? """,
                      (self.ids.grade_and_category_spinner.text, self.ids.students_full_name_spinner.text,))
            c.execute("""
                UPDATE preview SET Student_data=student_gender FROM students WHERE preview.Data="Gender"
                AND  students.current_class=? AND students.full_name=?""",
                      (self.ids.grade_and_category_spinner.text, self.ids.students_full_name_spinner.text,))
            c.execute("""
                UPDATE preview SET Student_data=current_class FROM students WHERE preview.Data="Class"
                AND students.current_class=? AND students.full_name=?""",
                      (self.ids.grade_and_category_spinner.text, self.ids.students_full_name_spinner.text,))

            c.execute("""
                UPDATE preview SET Student_data=registration_number FROM students WHERE preview.Data="Registration No"
                AND students.current_class=? AND students.full_name=?""",
                      (self.ids.grade_and_category_spinner.text, self.ids.students_full_name_spinner.text,))
            c.execute("""
                UPDATE preview SET Student_data=status FROM students WHERE preview.Data="Accomodation Status"
                AND students.current_class=? AND students.full_name=?""",
                      (self.ids.grade_and_category_spinner.text, self.ids.students_full_name_spinner.text,))
            c.execute("""
                UPDATE preview SET Student_data=dob FROM students WHERE preview.Data="Date of Birth"
                AND students.current_class=? AND students.full_name=?""",
                      (self.ids.grade_and_category_spinner.text, self.ids.students_full_name_spinner.text,))
            c.execute("""
                UPDATE preview SET Student_data=special_health_condition FROM students WHERE preview.Data="Health Condition"
                AND  students.current_class=? AND students.full_name=?""",
                      (self.ids.grade_and_category_spinner.text, self.ids.students_full_name_spinner.text,))
            c.execute("""
                UPDATE preview SET Student_data=father_name FROM students WHERE preview.Data="Father's Name"
                AND  students.current_class=? AND students.full_name=?""",
                      (self.ids.grade_and_category_spinner.text, self.ids.students_full_name_spinner.text,))
            c.execute("""
                UPDATE preview SET Student_data=mother_name FROM students WHERE preview.Data="Mother's Name"
                AND  students.current_class=? AND students.full_name=?""",
                      (self.ids.grade_and_category_spinner.text, self.ids.students_full_name_spinner.text,))
            c.execute("""
                UPDATE preview SET Student_data=guardian_name FROM students WHERE preview.Data="Guardian's Name"
                AND  students.current_class=? AND students.full_name=?""",
                      (self.ids.grade_and_category_spinner.text, self.ids.students_full_name_spinner.text,))
            c.execute("""
                UPDATE preview SET Student_data=parent_guardian_phone FROM students WHERE preview.Data="Parent/Guardian's Phone"
                AND  students.current_class=? AND students.full_name=?""",
                      (self.ids.grade_and_category_spinner.text, self.ids.students_full_name_spinner.text,))
            c.execute("""
                UPDATE preview SET Student_data=parent_guardian_email FROM students WHERE preview.Data="Parent/Guardian's Email"
                AND  students.current_class=? AND students.full_name=?""",
                      (self.ids.grade_and_category_spinner.text, self.ids.students_full_name_spinner.text,))
            c.execute("""
                UPDATE preview SET Student_data=parent_guardian_occupation FROM students WHERE preview.Data="Parent/Guardian's Occupation"
                AND  students.current_class=? AND students.full_name=?""",
                      (self.ids.grade_and_category_spinner.text, self.ids.students_full_name_spinner.text,))
            c.execute("""
                UPDATE preview SET Student_data=date_admitted FROM students WHERE preview.Data="Date Admitted"
                AND  students.current_class=? AND students.full_name=?""",
                      (self.ids.grade_and_category_spinner.text, self.ids.students_full_name_spinner.text,))
            c.execute("""
                UPDATE preview SET Student_data='Completed' FROM students WHERE preview.Data="Completion level" AND students.completion_level='c'
                AND  students.current_class=? AND students.full_name=?""",
                      (self.ids.grade_and_category_spinner.text, self.ids.students_full_name_spinner.text,))
            c.execute("""
                UPDATE preview SET Student_data='Not Completed' FROM students WHERE preview.Data="Completion level" AND students.completion_level=''
                AND  students.current_class=? AND students.full_name=?""",
                      (self.ids.grade_and_category_spinner.text, self.ids.students_full_name_spinner.text,))
            c.execute("""
                UPDATE preview SET Student_data=grade_and_category_admitted_to FROM students WHERE preview.Data="Class Admitted to"
                AND  students.current_class=? AND students.full_name=?""",
                      (self.ids.grade_and_category_spinner.text, self.ids.students_full_name_spinner.text,))

            conn.commit()

            data = [r[0:16] for r in c.execute("SELECT * FROM preview")]
            values = data

            if not self.student_preview:
                self.student_preview = MDDataTable(
                    size_hint=(0.8, 0.9),
                    size=(500, 500),
                    pos_hint={"center_x": .5, "center_y": .5},
                    use_pagination=True,
                    rows_num=9,
                    column_data=[
                        ("Data Type", dp(50)),
                        ('Student Info', dp(90)),
                    ],
                )
                self.student_preview.row_data = values
                self.ids.box.add_widget(self.student_preview)
            if not not self.student_preview:
                self.student_preview.row_data = values

            else:
                self.ids.box.add_widget(self.student_preview)

            self.ids.grade_and_category_spinner.text = "Select Class"
            self.ids.grade_and_category_spinner.background_color = .7, 0, 0, .9

            self.ids.students_full_name_spinner.text = "Select Name"
            self.ids.students_full_name_spinner.background_color = .7, 0, 0, .9

        except exceptions.EmptyClassSpinnerError:
            self.empty_class_dialog = MDDialog(
                title="Empty fields!",
                text="Please select student's class and student's name to continue",
                radius=[25, 7, 25, 7],
                auto_dismiss=False,
                buttons=[
                    MDRectangleFlatButton(
                        text="OK", on_release=self.close_empty_class_dialog
                    ),
                ],
            )
            self.empty_class_dialog.open()

    def close_empty_class_dialog(self, obj):
        self.empty_class_dialog.dismiss()

    def close_table(self):
        if self.student_preview:
            self.ids.grade_and_category_spinner.text = "Select Class"
            self.ids.students_full_name_spinner.text = "Select Name"

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


class EditStudentsDetails(Screen):
    conn = sqlite3.connect("school.db")
    c = conn.cursor()
    values1 = [r[0]
               for r in c.execute("SELECT available_grades FROM grades")]
    grades = values1

    values2 = [r[0]
               for r in c.execute("SELECT g_and_c FROM grade_and_category")]
    grades_and_category = values2

    def update_names_spinner(self, value):
        conn = sqlite3.connect("school.db")
        c = conn.cursor()
        names = [r[0]
                 for r in c.execute("""SELECT full_name FROM students WHERE
               students.current_class= ? """, (self.ids.grade_and_category_spinner.text,))]
        names_by_class = names
        if self.ids.grade_and_category_spinner.text == self.ids.grade_and_category_spinner.text:
            self.ids.students_full_name_spinner.values = names_by_class

    def show_data_to_be_edited(self):
        conn = sqlite3.connect("school.db")
        c = conn.cursor()

        name = [r[0] for r in c.execute("""SELECT  first_name FROM students WHERE students.current_class= ?
                AND students.full_name= ?""", (self.ids.grade_and_category_spinner.text,
                                               self.ids.students_full_name_spinner.text))]

        surname = [r[0] for r in c.execute("""SELECT  surname FROM students WHERE students.current_class= ?
                AND students.full_name= ?""", (self.ids.grade_and_category_spinner.text,
                                               self.ids.students_full_name_spinner.text))]
        student_gender = [r[0] for r in c.execute("""SELECT  student_gender FROM students WHERE students.current_class= ?
                AND students.full_name= ?""", (self.ids.grade_and_category_spinner.text,
                                               self.ids.students_full_name_spinner.text))]
        dob = [r[0] for r in c.execute("""SELECT  dob FROM students WHERE students.current_class= ?
                AND students.full_name= ?""", (self.ids.grade_and_category_spinner.text,
                                               self.ids.students_full_name_spinner.text))]
        special_health_condition = [r[0] for r in c.execute("""SELECT  special_health_condition FROM students WHERE students.current_class= ?
                AND students.full_name= ?""", (self.ids.grade_and_category_spinner.text,
                                               self.ids.students_full_name_spinner.text))]
        father_name = [r[0] for r in c.execute("""SELECT  father_name FROM students WHERE students.current_class= ?
                AND students.full_name= ?""", (self.ids.grade_and_category_spinner.text,
                                               self.ids.students_full_name_spinner.text))]
        mother_name = [r[0] for r in c.execute("""SELECT  mother_name FROM students WHERE students.current_class= ?
                AND students.full_name= ?""", (self.ids.grade_and_category_spinner.text,
                                               self.ids.students_full_name_spinner.text))]
        guardian_name = [r[0] for r in c.execute("""SELECT  guardian_name FROM students WHERE students.current_class= ?
                AND students.full_name= ?""", (self.ids.grade_and_category_spinner.text,
                                               self.ids.students_full_name_spinner.text))]
        parent_guardian_phone = [r[0] for r in c.execute("""SELECT  parent_guardian_phone FROM students WHERE students.current_class= ?
                AND students.full_name= ?""", (self.ids.grade_and_category_spinner.text,
                                               self.ids.students_full_name_spinner.text))]
        parent_guardian_email = [r[0] for r in c.execute("""SELECT  parent_guardian_email FROM students WHERE students.current_class= ?
                AND students.full_name= ?""", (self.ids.grade_and_category_spinner.text,
                                               self.ids.students_full_name_spinner.text))]
        parent_guardian_occupation = [r[0] for r in c.execute("""SELECT  parent_guardian_occupation FROM students WHERE students.current_class= ?
                AND students.full_name= ?""", (self.ids.grade_and_category_spinner.text,
                                               self.ids.students_full_name_spinner.text))]
        grade = [r[0] for r in c.execute("""SELECT  grade FROM students WHERE students.current_class= ?
                AND students.full_name= ?""", (self.ids.grade_and_category_spinner.text,
                                               self.ids.students_full_name_spinner.text))]
        grade_category = [r[0] for r in c.execute("""SELECT  grade_category FROM students WHERE students.current_class= ?
                AND students.full_name= ?""", (self.ids.grade_and_category_spinner.text,
                                               self.ids.students_full_name_spinner.text))]
        status = [r[0] for r in c.execute("""SELECT  status FROM students WHERE students.current_class= ?
                AND students.full_name= ?""", (self.ids.grade_and_category_spinner.text,
                                               self.ids.students_full_name_spinner.text))]

        for row in name:
            self.ids.first_name.text = str(name[0])
        for row in surname:
            self.ids.surname.text = str(surname[0])
        for row in student_gender:
            self.ids.student_gender_spinner.text = str(student_gender[0])
        for row in dob:
            self.ids.dob.text = str(dob[0])
        for row in special_health_condition:
            self.ids.special_health_condition.text = str(
                special_health_condition[0])
        for row in father_name:
            self.ids.father_name.text = str(father_name[0])
        for row in mother_name:
            self.ids.mother_name.text = str(mother_name[0])
        for row in guardian_name:
            self.ids.guardian_name.text = str(guardian_name[0])
        for row in parent_guardian_phone:
            self.ids.parent_guardian_phone.text = str(parent_guardian_phone[0])
        for row in parent_guardian_email:
            self.ids.parent_guardian_email.text = str(parent_guardian_email[0])
        for row in parent_guardian_occupation:
            self.ids.parent_guardian_occupation.text = str(
                parent_guardian_occupation[0])
        for row in name:
            self.ids.grade_spinner.text = str(grade[0])
        for row in name:
            self.ids.grade_category_spinner.text = str(grade_category[0])
        for row in name:
            self.ids.status_spinner.text = str(status[0])

    def save_edited_info(self):
        conn = sqlite3.connect("school.db")
        c = conn.cursor()
        c.execute("""
                    UPDATE students
                    SET first_name = ?,
                    surname =?,
                    full_name = ?,
                    student_gender =?,
                    dob =?,
                    special_health_condition  =?,
                    father_name =?,
                    mother_name =?,
                    guardian_name =?,
                    parent_guardian_phone =?,
                    parent_guardian_email =?,
                    parent_guardian_occupation =?,
                    grade =?,
                    grade_category =?,
                    status =?,
                    current_class = ?
                    WHERE students.current_class= ? AND students.full_name =?
                    """, (self.ids.first_name.text,  self.ids.surname.text, self.ids.first_name.text + " " +
                          self.ids.surname.text, self.ids.student_gender_spinner.text, self.ids.dob.text,
                          self.ids.special_health_condition.text, self.ids.father_name.text,
                          self.ids.mother_name.text, self.ids.guardian_name.text, self.ids.parent_guardian_phone.text,
                          self.ids.parent_guardian_email.text, self.ids.parent_guardian_occupation.text,
                          self.ids.grade_spinner.text, self.ids.grade_category_spinner.text,
                          #   self.ids.grade_spinner.text + self.ids.grade_category_spinner.text,
                          self.ids.status_spinner.text, self.ids.grade_spinner.text +
                          self.ids.grade_category_spinner.text,
                          self.ids.grade_and_category_spinner.text, self.ids.students_full_name_spinner.text))
        c.execute("""
                    UPDATE fees_payable
                    SET full_name = ?,
                    grade = ?,
                    grade_and_category = ?  WHERE fees_payable.grade_and_category= ? AND fees_payable.full_name =? """,
                  (self.ids.first_name.text + " " + self.ids.surname.text, self.ids.grade_spinner.text,
                   self.ids.grade_spinner.text +
                   self.ids.grade_category_spinner.text, self.ids.grade_and_category_spinner.text,
                   self.ids.students_full_name_spinner.text))
        conn.commit()

        self.ids.first_name.required = False
        self.ids.first_name.text = ''
        self.ids.surname.text = ''
        self.ids.student_gender_spinner.text = 'Select Gender'
        self.ids.dob.text = ''
        self.ids.special_health_condition.text = ''
        self.ids.father_name.text = ''
        self.ids.mother_name.text = ''
        self.ids.guardian_name.text = ''
        self.ids.parent_guardian_phone.text = ''
        self.ids.parent_guardian_email.text = ''
        self.ids.parent_guardian_occupation.text = ''
        self.ids.grade_spinner.text = 'Select Grade'
        self.ids.grade_category_spinner.text = 'Select Grade Category'
        self.ids.status_spinner.text = 'Select Status'
        self.ids.grade_and_category_spinner.text = 'Select Class'
        self.ids.students_full_name_spinner.text = 'Select Name'
        self.ids.grade_and_category_spinner.background_color = .7, 0, 0, .9
        self.ids.students_full_name_spinner.background_color = .7, 0, 0, .9
        self.ids.status_spinner.background_color = .7, 0, 0, .9
        self.ids.grade_category_spinner.background_color = .7, 0, 0, .9
        self.ids.grade_spinner.background_color = .7, 0, 0, .9
        self.ids.student_gender_spinner.background_color = .7, 0, 0, .9

    def spinner_clicked(self, value):
        self.ids.text = value
        return value

    def on_save(self, instance, value, date_range):
        self.ids.dob.text = str(value)

    def update_calendar(self, year, month, day):
        self.ids.dob.text = str(year)

    def on_cancel(self, instance, value):
        self.ids.dob.text = "Select date"

    def show_calendar(self):
        date_dialog = MDDatePicker(month=1, day=1, min_year=2000)
        date_dialog.bind(on_save=self.on_save,
                         on_cancel=self.on_cancel)
        date_dialog.open()

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


class ExitedStudents(Screen):
    # grade_spinner = Spinner()
    # grade_spinner = Spinner()
    conn = sqlite3.connect("school.db")
    c = conn.cursor()
    year = [r[0]
            for r in c.execute("SELECT available_years FROM years")]
    # year_completed = values

    def update_exited_pupils(self, value):
        conn = sqlite3.connect("school.db")
        c = conn.cursor()
        completed_final_years = [r[0]
                                 for r in c.execute("""SELECT full_name FROM exited_students WHERE
               exited_students.exited_year = ?""", (self.ids.year_exited_spinner.text,))]
        form3_list = completed_final_years
        if self.ids.year_exited_spinner.text == self.ids.year_exited_spinner.text:
            self.ids.students_full_name_spinner.values = form3_list

    def preview_exited_students(self):
        pass


class CompletedStudents(Screen):
    student_preview = None
    # grade_spinner = Spinner()
    conn = sqlite3.connect("school.db")
    c = conn.cursor()
    values = [r[0]
              for r in c.execute("SELECT available_years FROM years")]
    year_completed = values

    def update_completed_pupils(self, value):
        conn = sqlite3.connect("school.db")
        c = conn.cursor()
        completed_final_years = [r[0]
                                 for r in c.execute("""SELECT full_name FROM completed_students WHERE
               completed_students.completed_year = ?""", (self.ids.year_completed_spinner.text,))]
        form3_list = completed_final_years
        if self.ids.year_completed_spinner.text == self.ids.year_completed_spinner.text:
            self.ids.students_full_name_spinner.values = form3_list

    def preview_completed_students(self):
        try:
            if self.ids.year_completed_spinner.text == "Select Year Completed" or self.ids.students_full_name_spinner.text == 'Select Name':
                raise exceptions.EmptyClassSpinnerError
            conn = sqlite3.connect("school.db")
            c = conn.cursor()

            c.execute("""
                UPDATE preview SET Student_data = full_name FROM students WHERE preview.Data = 'Name'
                AND students.current_class =? AND students.full_name=? """,
                      (self.ids.year_completed_spinner.text, self.ids.students_full_name_spinner.text,))
            c.execute("""
                UPDATE preview SET Student_data = student_gender FROM students WHERE preview.Data = "Gender"
                AND  students.current_class =? AND students.full_name=?""",
                      (self.ids.year_completed_spinner.text, self.ids.students_full_name_spinner.text,))
            c.execute("""
                UPDATE preview SET Student_data = current_class FROM students WHERE preview.Data = "Class"
                AND students.current_class =? AND students.full_name=?""",
                      (self.ids.year_completed_spinner.text, self.ids.students_full_name_spinner.text,))

            c.execute("""
                UPDATE preview SET Student_data = registration_number FROM students WHERE preview.Data = "Registration No"
                AND students.current_class =? AND students.full_name=?""",
                      (self.ids.year_completed_spinner.text, self.ids.students_full_name_spinner.text,))
            c.execute("""
                UPDATE preview SET Student_data = status FROM students WHERE preview.Data = "Accomodation Status"
                AND students.current_class =? AND students.full_name=?""",
                      (self.ids.year_completed_spinner.text, self.ids.students_full_name_spinner.text,))
            c.execute("""
                UPDATE preview SET Student_data = dob FROM students WHERE preview.Data = "Date of Birth"
                AND students.current_class =? AND students.full_name=?""",
                      (self.ids.year_completed_spinner.text, self.ids.students_full_name_spinner.text,))
            c.execute("""
                UPDATE preview SET Student_data = special_health_condition FROM students WHERE preview.Data = "Health Condition"
                AND  students.current_class =? AND students.full_name=?""",
                      (self.ids.year_completed_spinner.text, self.ids.students_full_name_spinner.text,))
            c.execute("""
                UPDATE preview SET Student_data = father_name FROM students WHERE preview.Data = "Father's Name"
                AND  students.current_class =? AND students.full_name=?""",
                      (self.ids.year_completed_spinner.text, self.ids.students_full_name_spinner.text,))
            c.execute("""
                UPDATE preview SET Student_data = mother_name FROM students WHERE preview.Data = "Mother's Name"
                AND  students.current_class =? AND students.full_name=?""",
                      (self.ids.year_completed_spinner.text, self.ids.students_full_name_spinner.text,))
            c.execute("""
                UPDATE preview SET Student_data = guardian_name FROM students WHERE preview.Data = "Guardian's Name"
                AND  students.current_class =? AND students.full_name=?""",
                      (self.ids.year_completed_spinner.text, self.ids.students_full_name_spinner.text,))
            c.execute("""
                UPDATE preview SET Student_data = parent_guardian_phone FROM students WHERE preview.Data = "Parent/Guardian's Phone"
                AND  students.current_class =? AND students.full_name=?""",
                      (self.ids.year_completed_spinner.text, self.ids.students_full_name_spinner.text,))
            c.execute("""
                UPDATE preview SET Student_data = parent_guardian_email FROM students WHERE preview.Data = "Parent/Guardian's Email"
                AND  students.current_class =? AND students.full_name=?""",
                      (self.ids.year_completed_spinner.text, self.ids.students_full_name_spinner.text,))
            c.execute("""
                UPDATE preview SET Student_data = parent_guardian_occupation FROM students WHERE preview.Data = "Parent/Guardian's Occupation"
                AND  students.current_class =? AND students.full_name=?""",
                      (self.ids.year_completed_spinner.text, self.ids.students_full_name_spinner.text,))
            c.execute("""
                UPDATE preview SET Student_data = date_admitted FROM students WHERE preview.Data = "Date Admitted"
                AND  students.current_class =? AND students.full_name=?""",
                      (self.ids.year_completed_spinner.text, self.ids.students_full_name_spinner.text,))
            c.execute("""
                UPDATE preview SET Student_data = 'Completed' FROM students WHERE preview.Data = "Completion level" AND students.completion_level = 'c'
                AND  students.current_class =? AND students.full_name=?""",
                      (self.ids.year_completed_spinner.text, self.ids.students_full_name_spinner.text,))
            c.execute("""
                UPDATE preview SET Student_data = grade_and_category FROM students WHERE preview.Data = "Class Admitted to"
                AND  students.current_class =? AND students.full_name=?""",
                      (self.ids.year_completed_spinner.text, self.ids.students_full_name_spinner.text,))
            c.execute("""
                UPDATE preview SET Student_data=completed_arrear FROM students WHERE preview.Data="Arrears"
                AND  students.current_class=? AND students.full_name=?""",
                      (self.ids.year_completed_spinner.text, self.ids.students_full_name_spinner.text,))
            conn.commit()

            data = [r[0:17] for r in c.execute("SELECT * FROM preview")]
            values = data

            if not self.student_preview:
                self.student_preview = MDDataTable(
                    size_hint=(0.8, 0.9),
                    size=(500, 500),
                    pos_hint={"center_x": .5, "center_y": .5},
                    use_pagination=True,
                    rows_num=9,
                    column_data=[
                        ("Data Type", dp(50)),
                        ('Student Info', dp(90)),
                    ],
                )
                self.student_preview.row_data = values
                self.ids.box.add_widget(self.student_preview)
            if not not self.student_preview:
                self.student_preview.row_data = values
                self.ids.students_full_name_spinner.text = "Select Name"
                self.ids.students_full_name_spinner.text = "Select Name"
            else:
                self.ids.box.add_widget(self.student_preview)

        except exceptions.EmptyClassSpinnerError:
            self.empty_class_dialog = MDDialog(
                title="Empty fields!",
                text="Please select student's class and student's name to continue",
                radius=[25, 7, 25, 7],
                auto_dismiss=False,
                buttons=[
                    MDRectangleFlatButton(
                        text="OK", on_release=self.close_empty_class_dialog
                    ),
                ],
            )
            self.empty_class_dialog.open()

    def close_empty_class_dialog(self, obj):
        self.empty_class_dialog.dismiss()

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
