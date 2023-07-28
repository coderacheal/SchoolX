import sqlite3
import math
import src.exceptions.exceptions as exceptions
from kivy.uix.screenmanager import Screen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRectangleFlatButton, MDFlatButton
from kivy.metrics import dp
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.pickers import MDDatePicker


class Staff(Screen):
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
        self.manager.current = "authorization"


class RegisterStaffSecurity(Screen):
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
        self.manager.current = "authorization"


class StaffRegistrationForms(Screen):
    def spinner_clicked(self, value):
        self.ids.text = value
        return value

    def selected(self, file_name):
        try:
            self.ids.certificate_image.source = file_name[0]
        except:
            pass

    # def select_path(self, path):
    #     print(path)
    #     self.exit_manager()

    # def open_file_manager(self):
    #     self.file_manager_obj.show('/')

    # def exit_manager(self):
    #     self.file_manager_obj.close()

    # staff appointment dae
    def save_appointment_date(self, instance, value, date_range):
        self.ids.date_appointed.text = str(value)

    def cancel_appointment_date(self, instance, value):
        self.ids.date_appointed.text = "No date selected yet"

    def show_appointment_date(self):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.save_appointment_date,
                         on_cancel=self.cancel_appointment_date)
        date_dialog.open()

    # staff date of birth picker

    def on_save_dob(self, instance, value, date_range):
        self.ids.staff_dob.text = str(value)

    def on_cancel_dob(self, instance, value):
        self.ids.staff_dob.text = "No date selected yet"

    def show_staff_dob(self):
        date_dialog = MDDatePicker(year=1990, month=1, day=1)
        date_dialog.bind(on_save=self.on_save_dob,
                         on_cancel=self.on_cancel_dob)
        date_dialog.open()

    def register_staff(self):
        try:
            conn = sqlite3.connect("school.db")
            c = conn.cursor()
            c.execute("""INSERT INTO staff VALUES(:staff_first_name, :staff_surname,
                            :staff_full_name, :staff_gender, :staff_id, :date_of_birth,
                            :qualification, :name_of_school, :position_assigned, :staff_phone_number,
                            :staff_email, :staff_type, :salary_grade, :current_salary, :date_appointed, :upload_certificate)""",
                      {
                          'staff_first_name': self.ids.staff_first_name.text,
                          'staff_surname': self.ids.staff_surname.text,
                          'staff_full_name': self.ids.staff_first_name.text + " " + self.ids.staff_surname.text,
                          'staff_gender': self.ids.staff_gender.text,
                          'staff_id': self.ids.staff_id.text,
                          'date_of_birth': self.ids.staff_dob.text,
                          'qualification': self.ids.qualification.text,
                          'name_of_school': self.ids.name_of_school.text,
                          'position_assigned': self.ids.position_assigned.text,
                          'staff_phone_number': self.ids.staff_phone_number.text,
                          'staff_email': self.ids.staff_email.text,
                          'staff_type': self.ids.staff_type_spinner.text,
                          'salary_grade': self.ids.salary_grade_spinner.text,
                          "current_salary": "",
                          'date_appointed': self.ids.date_appointed.text,
                          'upload_certificate': "",

                      })

            c.execute(
                """INSERT OR IGNORE INTO salary_payable(staff_full_name, staff_id, salary_grade)
                    SELECT staff_full_name, staff_id, salary_grade FROM staff
                    """)
            c.execute(
                """INSERT OR IGNORE INTO differentiated_salary_payable(full_name, staff_id)
                    SELECT staff_full_name, staff_id FROM staff
                    WHERE staff.salary_grade='Differentiated'""")
            c.execute("""
                    UPDATE salary_payable
                    SET salary=total_salary
                    FROM set_salary
                    WHERE set_salary.salary_grade=salary_payable.salary_grade
                    AND salary_payable.salary_grade= ? """,
                      (self.ids.salary_grade_spinner.text,))

            if self.ids.staff_first_name.text == '':
                raise exceptions.EmptyFieldError
            if self.ids.staff_surname.text == '':
                raise exceptions.EmptyFieldError
            elif self.ids.staff_gender.text == 'Gender':
                raise exceptions.EmptyFieldError
            elif self.ids.staff_id.text == '':
                raise sqlite3.IntegrityError
            elif self.ids.staff_dob.text == '':
                raise exceptions.EmptyFieldError
            elif self.ids.qualification.text == '':
                raise exceptions.EmptyFieldError
            elif self.ids.salary_grade_spinner.text == 'Select salary grade':
                raise exceptions.EmptyFieldError
            elif self.ids.position_assigned.text == "":
                raise exceptions.EmptyFieldError
            elif self.ids.staff_email.text == "":
                raise exceptions.EmptyFieldError
            elif self.ids.staff_phone_number.text == "":
                raise exceptions.EmptyFieldError
            elif self.ids.date_appointed.text == "":
                raise exceptions.EmptyFieldError

        except sqlite3.IntegrityError:
            self.duplicate_dialog = MDDialog(
                title="Staff Id Duplicate",
                text="Staff Id already exists",
                radius=[25, 7, 25, 7],
                auto_dismiss=False,
                buttons=[
                    MDRectangleFlatButton(
                        text="CLOSE", on_release=self.close_duplicate_dialog, on_press=self.empty_staff_id
                    ),
                    MDRectangleFlatButton(
                        text="EDIT", on_release=self.close_duplicate_dialog, on_press=self.empty_staff_id
                    ),
                ],
            )
            self.duplicate_dialog.open()
        except exceptions.EmptyFieldError:
            self.imcomplete_dialog = MDDialog(
                title="Incomplete Registration!",
                radius=[25, 7, 25, 7],
                text="All fields are required",
                buttons=[
                    MDRectangleFlatButton(
                        text="CLOSE", on_release=self.close_imcomplete_dialog,
                    ),
                ],
            )
            self.imcomplete_dialog.open()
        else:
            conn.commit()
            self.successful_staff_regis_dialog = MDDialog(
                title="Success!",
                radius=[40, 7, 40, 7],
                text="Staff member has been successfully entered on to the payroll",
                auto_dismiss=False,
                buttons=[
                    MDRectangleFlatButton(
                        text="CLOSE", on_release=self.close_successful_staff_regis_dialog,
                    ),
                ],
            )
            self.successful_staff_regis_dialog.open()
            self.ids.staff_first_name.text = ''
            self.ids.staff_surname.text = ''
            self.ids.staff_gender.text = 'Gender'
            self.ids.staff_gender.background_color = .7, 0, 0, .9
            self.ids.staff_id.text = ''
            self.ids.staff_dob.text = ''
            self.ids.name_of_school.text = ""
            self.ids.qualification.text = ''
            self.ids.salary_grade_spinner.text = 'Select salary grade'
            self.ids.salary_grade_spinner.background_color = .7, 0, 0, .9
            self.ids.staff_type_spinner.text = "Select staff type"
            self.ids.staff_type_spinner.background_color = .7, 0, 0, .9
            self.ids.position_assigned.text = ""
            self.ids.staff_email.text = ""
            self.ids.staff_phone_number.text = ""
            self.ids.date_appointed.text = ""

        finally:
            conn.close()

    def close_duplicate_dialog(self, obj):
        self.duplicate_dialog.dismiss()

    def empty_staff_id(self, obj):
        self.ids.staff_id.text = " "
        self.ids.staff_id.required = True

    def close_successful_staff_regis_dialog(self, obj):
        self.successful_staff_regis_dialog.dismiss()

    def close_imcomplete_dialog(self, obj):
        self.imcomplete_dialog.dismiss()

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
        self.manager.current = "authorization"


class EditStaffSecurity(Screen):
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
        self.manager.current = "authorization"


class EditStaffDetails(Screen):
    conn = sqlite3.connect("school.db")
    c = conn.cursor()
    values = [r[0]
              for r in c.execute("SELECT staff_type FROM staff_type")]
    the_staff_type = values

    def update_names_spinner(self, value):
        conn = sqlite3.connect("school.db")
        c = conn.cursor()
        names = [r[0]
                 for r in c.execute("""SELECT staff_full_name FROM staff WHERE staff_type= ?""",
                                    (self.ids.select_staff_type_spinner.text,))]
        staff_names = names
        if self.ids.select_staff_type_spinner.text == self.ids.select_staff_type_spinner.text:
            self.ids.select_staff_name_spinner.values = staff_names

    def show_data_to_be_edited(self):
        conn = sqlite3.connect("school.db")
        c = conn.cursor()

        first_name = [r[0] for r in c.execute("""SELECT  staff_first_name FROM staff WHERE
            staff.staff_type = ? AND staff.staff_full_name =?""", (self.ids.select_staff_type_spinner.text, self.ids.select_staff_name_spinner.text))]

        surname = [r[0] for r in c.execute("""SELECT  staff_surname FROM staff WHERE
            staff.staff_type = ? AND staff.staff_full_name = ?""", (self.ids.select_staff_type_spinner.text,
                                                                    self.ids.select_staff_name_spinner.text,))]
        gender = [r[0] for r in c.execute("""SELECT  staff_gender FROM staff WHERE
            staff.staff_type = ? AND staff.staff_full_name = ? """, (self.ids.select_staff_type_spinner.text, self.ids.select_staff_name_spinner.text,))]
        dob = [r[0] for r in c.execute("""SELECT  date_of_birth FROM staff WHERE
            staff.staff_type = ? AND staff.staff_full_name = ? """, (self.ids.select_staff_type_spinner.text, self.ids.select_staff_name_spinner.text,))]
        staff_qualification = [r[0] for r in c.execute("""SELECT  certification FROM staff WHERE
            staff.staff_type= ? AND staff.staff_full_name= ? """, (self.ids.select_staff_type_spinner.text, self.ids.select_staff_name_spinner.text,))]
        school = [r[0] for r in c.execute("""SELECT  name_of_school FROM staff WHERE
            staff.staff_type = ? AND staff.staff_full_name = ? """, (self.ids.select_staff_type_spinner.text, self.ids.select_staff_name_spinner.text,))]
        position = [r[0] for r in c.execute("""SELECT  position_assigned FROM staff WHERE
            staff.staff_type= ? AND staff.staff_full_name= ? """, (self.ids.select_staff_type_spinner.text, self.ids.select_staff_name_spinner.text,))]
        phone = [r[0] for r in c.execute("""SELECT  staff_phone_number FROM staff WHERE
            staff.staff_type = ? AND staff.staff_full_name = ?""", (self.ids.select_staff_type_spinner.text, self.ids.select_staff_name_spinner.text,))]
        email = [r[0] for r in c.execute("""SELECT  staff_email FROM staff WHERE
            staff.staff_type= ? AND staff.staff_full_name= ? """, (self.ids.select_staff_type_spinner.text, self.ids.select_staff_name_spinner.text,))]
        salary_category = [r[0] for r in c.execute("""SELECT  salary_grade FROM staff WHERE
            staff.staff_type= ? AND staff.staff_full_name= ?""", (self.ids.select_staff_type_spinner.text, self.ids.select_staff_name_spinner.text,))]

        for row in first_name:
            self.ids.staff_first_name.text = str(first_name[0])
        for row in surname:
            self.ids.staff_surname.text = str(surname[0])
        for row in gender:
            self.ids.staff_gender_spinner.text = str(gender[0])
        for row in dob:
            self.ids.staff_dob.text = str(dob[0])
        for row in staff_qualification:
            self.ids.qualification.text = str(staff_qualification[0])
        for row in school:
            self.ids.name_of_school.text = str(school[0])
        for row in position:
            self.ids.position_assigned.text = str(position[0])
        for row in phone:
            self.ids.staff_phone_number.text = str(phone[0])
        for row in email:
            self.ids.staff_email.text = str(email[0])
        for row in salary_category:
            self.ids.salary_grade_spinner.text = str(salary_category[0])

    def save_edited_info(self):
        conn = sqlite3.connect("school.db")
        c = conn.cursor()

        c.execute("""
                    UPDATE staff
                    SET
                    staff_first_name=?,
                    staff_surname=?,
                    staff_full_name=?,
                    staff_gender=?,
                    date_of_birth=?,
                    certification=?,
                    name_of_school=?,
                    position_assigned=?,
                    staff_phone_number=?,
                    staff_email=?,
                    salary_grade=?
                    WHERE staff.staff_type =? AND staff.staff_full_name= ?
                    """, (self.ids.staff_first_name.text,  self.ids.staff_surname.text, self.ids.staff_first_name.text + " " +
                          self.ids.staff_surname.text, self.ids.staff_gender_spinner.text, self.ids.staff_dob.text,
                          self.ids.qualification.text, self.ids.name_of_school.text,
                          self.ids.position_assigned.text, self.ids.staff_phone_number.text, self.ids.staff_email.text,
                          self.ids.salary_grade_spinner.text, self.ids.select_staff_type_spinner.text,
                          self.ids.select_staff_name_spinner.text))
        conn.commit()
        self.ids.staff_first_name.text = ''
        self.ids.staff_surname.text = ''
        self.ids.staff_dob.text = ''
        self.ids.qualification.text = ''
        self.ids.name_of_school.text = ''
        self.ids.position_assigned.text = ''
        self.ids.staff_phone_number.text = ''
        self.ids.staff_email.text = ''
        self.ids.staff_gender_spinner.text = 'Select Gender'
        self.ids.salary_grade_spinner.text = "Select Salary Grade"
        self.ids.select_staff_type_spinner.text = "Select Staff Type"
        self.ids.select_staff_name_spinner.text = "Select Staff Name"
        self.ids.select_staff_name_spinner.background_color = .7, 0, 0, .9
        self.ids.salary_grade_spinner.background_color = .7, 0, 0, .9
        self.ids.staff_gender_spinner.background_color = .7, 0, 0, .9
        self.ids.select_staff_type_spinner.background_color = .7, 0, 0, .9

    def spinner_clicked(self, value):
        self.ids.text = value
        return value

    def on_save(self, instance, value, date_range):
        self.ids.staff_dob.text = str(value)

    def update_calendar(self, year, month, day):
        self.ids.staff_dob.text = str(year)

    def on_cancel(self, instance, value):
        self.ids.staff_dob.text = "Select date"

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
        self.manager.current = "authorization"


class ViewStaffDetails(Screen):
    staff_preview = None
    conn = sqlite3.connect("school.db")
    c = conn.cursor()
    values = [r[0]
              for r in c.execute("SELECT staff_type FROM staff_type")]
    the_staff_type = values

    def update_names_spinner(self, value):
        conn = sqlite3.connect("school.db")
        c = conn.cursor()
        names = [r[0]
                 for r in c.execute("""SELECT staff_full_name FROM staff WHERE staff_type= ?""",
                                    (self.ids.select_staff_type_spinner.text,))]
        staff_names = names
        if self.ids.select_staff_type_spinner.text == self.ids.select_staff_type_spinner.text:
            self.ids.select_staff_name_spinner.values = staff_names

    def spinner_clicked(self, value):
        self.ids.text = value
        return value

    def view_staff(self):
        try:
            if self.ids.select_staff_name_spinner.text == "Select Staff Name":
                raise exceptions.EmptyClassSpinnerError
            conn = sqlite3.connect("school.db")
            c = conn.cursor()

            c.execute("""
                UPDATE staff_preview SET staff_data=staff_full_name FROM staff WHERE staff_preview.Data='Name'
                AND staff.staff_full_name=? """,
                      (self.ids.select_staff_name_spinner.text,))
            c.execute("""
                UPDATE staff_preview SET staff_data=staff_gender FROM staff WHERE staff_preview.Data="Gender"
                AND staff.staff_full_name=?""",
                      (self.ids.select_staff_name_spinner.text, ))
            c.execute("""
                UPDATE staff_preview SET staff_data=staff_id FROM staff WHERE staff_preview.Data="Staff ID"
                AND staff.staff_full_name=?""",
                      (self.ids.select_staff_name_spinner.text,))

            c.execute("""
                UPDATE staff_preview SET staff_data=date_of_birth FROM staff WHERE staff_preview.Data="Date of Birth"
                AND staff.staff_full_name=?""",
                      (self.ids.select_staff_name_spinner.text,))
            c.execute("""
                UPDATE staff_preview SET staff_data=certification FROM staff WHERE staff_preview.Data="Qualification"
                AND staff.staff_full_name=?""",
                      (self.ids.select_staff_name_spinner.text,))
            c.execute("""
                UPDATE staff_preview SET staff_data=name_of_school FROM staff WHERE staff_preview.Data="Name of Institution Attended"
                AND staff.staff_full_name=?""",
                      (self.ids.select_staff_name_spinner.text,))
            c.execute("""
                UPDATE staff_preview SET staff_data=position_assigned FROM staff WHERE staff_preview.Data="Position Assigned"
                AND staff.staff_full_name=?""",
                      (self.ids.select_staff_name_spinner.text,))
            c.execute("""
                UPDATE staff_preview SET staff_data=staff_phone_number FROM staff WHERE staff_preview.Data="Phone Number"
                AND staff.staff_full_name=?""",
                      (self.ids.select_staff_name_spinner.text,))
            c.execute("""
                UPDATE staff_preview SET staff_data=staff_email FROM staff WHERE staff_preview.Data="Email"
                 AND staff.staff_full_name=?""",
                      (self.ids.select_staff_name_spinner.text,))
            c.execute("""
                UPDATE staff_preview SET staff_data=salary_grade FROM staff WHERE staff_preview.Data="Salary Grade"
                AND staff.staff_full_name=?""",
                      (self.ids.select_staff_name_spinner.text,))
            c.execute("""
                UPDATE staff_preview SET staff_data=current_salary FROM staff WHERE staff_preview.Data="Current Salary GHC"
                AND staff.staff_full_name=?""",
                      (self.ids.select_staff_name_spinner.text,))
            c.execute("""
                UPDATE staff_preview SET staff_data=date_appointed FROM staff WHERE staff_preview.Data="Date Appointed"
                AND staff.staff_full_name=?""",
                      (self.ids.select_staff_name_spinner.text,))

            conn.commit()

            data = [r[0:16] for r in c.execute("SELECT * FROM staff_preview")]
            values = data

            if not self.staff_preview:
                self.staff_preview = MDDataTable(
                    size_hint=(0.8, 0.9),
                    size=(500, 500),
                    pos_hint={"center_x": .5, "center_y": .5},
                    use_pagination=True,
                    rows_num=9,
                    column_data=[
                        ("Data Type", dp(50)),
                        ('Staff Info', dp(90)),
                    ],
                )
                self.staff_preview.row_data = values
                self.ids.box.add_widget(self.staff_preview)
            if not not self.staff_preview:
                self.staff_preview.row_data = values
            else:
                self.ids.box.add_widget(self.staff_preview)

            self.ids.select_staff_type_spinner.text = "Select Staff Type"
            self.ids.select_staff_name_spinner.text = "Select Staff Name"

        except exceptions.EmptyClassSpinnerError:
            self.empty_class_dialog = MDDialog(
                title="Empty fields!",
                text="Please select staff's category and staff's name to continue",
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
        self.manager.current = "authorization"
