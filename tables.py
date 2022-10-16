import sqlite3


conn = sqlite3.connect("school.db")
c = conn.cursor()
c.execute("""CREATE TABLE if not exists students(
            first_name text,
            surname text,
            full_name text,
            student_gender text,
            registration_number integer UNIQUE,
            dob integer,
            special_health_condition text,
            father_name text,
            mother_name text,
            guardian_name text,
            parent_guardian_phone text,
            parent_guardian_email text,
            parent_guardian_occupation text,
            date_admitted blob,
            grade blob,
            grade_category text,
            grade_and_category_admitted_to text,
            current_class text,
            status text,
            completion_level text,
            completed_arrear real
        )""")


c.execute("CREATE TABLE if not exists grades(available_grades text)")

basic_grades = [("Nursery 1",), ('Nursery 2',), ('KG 1',), ('KG 2',), ("Grade 1",), ("Grade 2",),
                ("Grade 3",), ("Grade 4",), ("Grade 5",), ("Grade 6",), ("Grade 7",),
                ("Grade 8",), ("Grade 9",), ]


c.executemany("INSERT INTO grades VALUES(?)", basic_grades)

c.execute("CREATE TABLE if not exists years(available_years text)")

completed_years = [("2022",), ("2023",), ("2024",), ("2025",), ("2026",), ("2027",), ("2028",), ("2029",),
                   ("2030",), ("2031",), ("2032",), ("2033",), ("2034",), ("2035",)]

c.executemany("INSERT INTO years VALUES(?)", completed_years)
c.execute("""CREATE TABLE if not exists staff_type(staff_type text)""")

staff_type = [("Teaching",), ("Non-Teaching",), ]

c.executemany("INSERT INTO staff_type VALUES(?)", staff_type)

c.execute("""CREATE TABLE if not exists preview(
            Data text,
            Student_data text
            )""")

preview_particulars = [("Name", ""), ("Gender", ""), ("Class", ""), ("Registration No", ""),
                       ("Accomodation Status", ""),
                       ("Date of Birth", ""), ("Health Condition", ""),
                       ("Father's Name", ""), ("Mother's Name", ""),
                       ("Guardian's Name", ""), ("Parent/Guardian's Phone", ""),
                       ("Parent/Guardian's Email", ""),
                       ("Parent/Guardian's Occupation", ""),
                       ("Date Admitted", ""), ("Class Admitted to", ""),
                       ("Completion level", ""), ("Arrears", "")]

c.executemany("INSERT INTO preview VALUES(?, ?)", preview_particulars)

c.execute("""CREATE TABLE if not exists staff_preview(
            Data text,
            staff_data text
            )""")


staff_preview_particulars = [("Name", ""), ("Gender", ""), ("Staff ID", ""), ("Date of Birth", ""),
                             ("Qualification", ""), ("Name of Institution Attended", ""),
                             ("Position Assigned", ""), ("Phone Number", ""),
                             ("Email", ""), ("Salary Grade", ""),
                             ("Current Salary GHC", ""), ("Date Appointed", ""),
                             ]

c.executemany("INSERT INTO staff_preview VALUES(?, ?)",
              staff_preview_particulars)

c.execute("CREATE TABLE if not exists grade_and_category(g_and_c text)")

grades_and_category = [("Nursery 1A",), ("Nursery 1B",), ('Nursery 2A',), ('Nursery 2B',),
                       ('KG 1A',), ('KG 1B',),
                       ('KG 2A',), ('KG 2B',), ("Grade 1A",), ("Grade 1B",),
                       ("Grade 2A",), ("Grade 2B",), ("Grade 3A",), ("Grade 3B",),
                       ("Grade 4A",), ("Grade 4B",), ("Grade 5A",), ("Grade 5B",),
                       ("Grade 6A",), ("Grade 6B",), ("Grade 7A",), ("Grade 7B",),
                       ("Grade 8A",), ("Grade 8B",), ("Grade 9A",), ("Grade 9B",), ]

c.executemany("INSERT INTO grade_and_category VALUES(?)", grades_and_category)


c.execute("""CREATE TABLE if not exists set_fees(
            start_of_term text NOT NULL DEFAULT o,
            end_of_term text NOT NULL DEFAULT o,
            term text NOT NULL DEFAULT o,
            grade text NOT NULL DEFAULT o,
            tuition real NOT NULL DEFAULT 0,
            studies real NOT NULL DEFAULT 0,
            pta_levy real NOT NULL DEFAULT 0,
            printing real NOT NULL DEFAULT 0,
            maintenance real NOT NULL DEFAULT 0,
            motivation real NOT NULL DEFAULT 0,
            library real NOT NULL DEFAULT 0,
            canteen real NOT NULL DEFAULT 0,
            sanitation real NOT NULL DEFAULT 0,
            sports real NOT NULL DEFAULT 0,
            boarding_fees real NOT NULL DEFAULT 0,
            total_without_boarding real NOT NULL DEFAULT 0,
            total_with_boarding real NOT NULL DEFAULT 0,
            time_set text NOT NULL DEFAULT o
        )""")
class_set_list = [
    ("-", "-", "-", "Nursery 1", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, "-"),
    ("-", "-", "-", "Nursery 2", 0, 0, 0,
     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, "-"),
    ("-", "-", "-", "KG 1", 0, 0, 0, 0,
     0, 0, 0, 0, 0, 0, 0, 0, 0, "-"),
    ("-", "-", "-", "KG 2", 0, 0, 0, 0,
     0, 0, 0, 0, 0, 0, 0, 0, 0, "-"),
    ("-", "-", "-", "Grade 1", 0, 0, 0,
     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, "-"),
    ("-", "-", "-", "Grade 2", 0, 0, 0,
     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, "-"),
    ("-", "-", "-", "Grade 3", 0, 0, 0,
     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, "-"),
    ("-", "-", "-", "Grade 4", 0, 0, 0,
     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, "-"),
    ("-", "-", "-", "Grade 5", 0, 0, 0,
     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, "-"),
    ("-", "-", "-", "Grade 6", 0, 0, 0,
     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, "-"),
    ("-", "-", "-", "Grade 7", 0, 0, 0,
     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, "-"),
    ("-", "-", "-", "Grade 8", 0, 0, 0,
     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, "-"),
    ("-", "-", "-", "Grade 9", 0, 0, 0,
     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, "-")
]


c.executemany(
    "INSERT INTO set_fees VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", class_set_list)


c.execute("""CREATE TABLE if not exists set_fees_history(
            time_set text,
            term text,
            grade text,
            tuition real,
            studies real,
            pta_levy real,
            printing real,
            maintenance real,
            motivation real,
            library real,
            canteen real,
            sanitation real,
            sports real,
            boarding_fees real,
            total_without_boarding real,
            total_with_boarding real
        )""")


c.execute("""CREATE TABLE if not exists fees_payable(
            start_term text,
            end_term text,
            full_name text,
            registration_number integer UNIQUE,
            grade text,
            grade_and_category text,
            unique_id text,
            status text,
            balance real NOT NULL DEFAULT 0,
            last_payment real NOT NULL DEFAULT 0,
            date_of_last_payment text
        )""")

c.execute("""CREATE TABLE if not exists completed_students(
            full_name text,
            registration_number integer UNIQUE,
            grade text,
            grade_and_category text,
            status text,
            arrears real,
            completion_level text NOT NULL DEFAULT o,
            completed_year integer
            )""")
c.execute("""CREATE TABLE if not exists exited_students(
            full_name text,
            registration_number integer UNIQUE,
            grade text,
            grade_and_category text,
            status text,
            arrears real,
            completion_level text NOT NULL DEFAULT o,
            exited_year integer
            )""")

c.execute("""CREATE TABLE if not exists fees_paid(
            date_and_time text,
            year text,
            term text,
            grade_and_category text,
            full_name text,
            payee_type text,
            payment_type text,
            amt real,
            name_of_payee text,
            recept_no text,
            current_grade text
        )""")


c.execute("""CREATE TABLE if not exists expenditure(
            date text,
            year integer,
            term text,
            purpose text,
            expenditure_amt real,
            purpose_description text,
            Authorised_by text,
            Signitory_1 text,
            Signitory_2 text,
            Signitory_3 text
        )""")

c.execute("""CREATE TABLE if not exists staff(
            staff_first_name text,
            staff_surname text,
            staff_full_name text,
            staff_gender text,
            staff_id integer UNIQUE,
            date_of_birth text,
            certification text,
            name_of_school text,
            position_assigned text,
            staff_phone_number text,
            staff_email text,
            staff_type text,
            salary_grade text,
            current_salary float NOT NULL DEFAULT 0,
            date_appointed text,
            upload_certificate blob
        )""")

c.execute("""CREATE TABLE if not exists set_salary(
            date_set text,
            salary_grade text,
            base_salary real,
            studies real,
            honourarium real,
            motivation real,
            bonus real,
            ssnit_contibution real,
            income_tax real,
            welfare real,
            total_salary real
            )""")

salaries = [("-", "Grade A", 0, 0, 0, 0, 0, 0, 0, 0, 0,),
            ("-", "Grade B", 0, 0, 0, 0, 0, 0, 0, 0, 0,),
            ("-", "Grade C", 0, 0, 0, 0, 0, 0, 0, 0, 0,),
            ("-", "Management", 0, 0, 0, 0, 0, 0, 0, 0, 0,),

            ]

c.executemany(
    "INSERT INTO set_salary VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", salaries)

c.execute("""CREATE TABLE if not exists differentiated_salary_payable(
            date_set text,
            full_name text,
            staff_id integer UNIQUE,
            base_salary real,
            studies real,
            honourarium real,
            motivation real,
            bonus real,
            ssnit_contibution real,
            income_tax real,
            welfare real,
            total_salary real NOT NULL DEFAULT 0.0
            )""")

c.execute("""CREATE TABLE if not exists salary_payable(
            staff_full_name text,
            staff_id integer UNIQUE,
            salary_grade text,
            salary real,
            deductions real,
            salary_paid real
        )""")

c.execute("""CREATE TABLE if not exists users_account(
            first_name text,
            surname ext ,
            full_name text,
            staff_id integer UNIQUE,
            email text,
            user_name text,
            password text,
            reenter_password text,
            date_registered text,
            entered_password text,
            log_date text

        )""")

c.execute("""CREATE TABLE if not exists months(
                months text,
                month_term text)""")

months_and_term = [("Jan", "First Term"), ("Feb", "First Term"), ("Mar", "First Term"), ("Apr", "First Term"),
                   ("May", "Second Term"), ("Jun", "Second Term"),
                   ("Jul", "Second Term"), ("Aug", "Second Term"),
                   ("Sep", "Third Term"), ("Oct", "Third Term"), ("Nov", "Third Term"), ("Dec", "Third Term")]


c.executemany("INSERT INTO months VALUES(?, ?)", months_and_term)

c.execute("""CREATE TABLE if not exists income_and_expenditure(
                income real,
                expenditure real,
                p_l real,
                month text,
                term text,
                year text)
            """)
c.execute("""CREATE TABLE if not exists expenditure_barchart(
                expense_name text,
                expense_amt real
            )
            """)
expense = [("Academic", 0,),
           ("Canteen", 0,),
           ("Tax", 0,),
           ("Salary", 0, ),
           ("Utility", 0,),
           ("Miscellaneous", 0,)
           ]

c.executemany(
    "INSERT INTO expenditure_barchart VALUES(?, ?)", expense)

month_names_ie = [(0, 0, 0, "January", "", ''),
                  (0, 0, 0, "February", "", ''),
                  (0, 0, 0, "March", "", ''),
                  (0, 0, 0, "April", "", ''),
                  (0, 0, 0, "May", "", ''),
                  (0, 0, 0, "June", "", ''),
                  (0, 0, 0, "July", "", ''),
                  (0, 0, 0, "August", "", ''),
                  (0, 0, 0, "September", "", ''),
                  (0, 0, 0, "October", "", ''),
                  (0, 0, 0, "November", "", ''),
                  (0, 0, 0, "December", "", ''),



                  ]


c.execute("""CREATE TABLE if not exists income_and_expenditure_previews(
                income_preview real,
                expenditure_preview real,
                p_l_preview real,
                month_preview text,
                term_preview text,
                year_preview text
                )
            """)
c.executemany(
    "INSERT INTO income_and_expenditure_previews VALUES(?,?,?,?,?,?)", month_names_ie)
conn.commit()
conn.close()
