from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
import sqlite3
import sys

# use .ui file without converting to .py
main_window, _ = loadUiType('main.ui')


# database for application
class Database:
    def __init__(self):
        # connect to sqlite3 database
        self.connection = sqlite3.connect('school.db')
        self.cursor = self.connection.cursor()

        # create admin table
        self.cursor.execute("""create table if not exists 'admin' (
                            admin_id integer primary key autoincrement not null,
                            username text,
                            password text)""")

        # create student table
        self.cursor.execute("""create table if not exists 'student' (
                            student_id integer primary key autoincrement not null,
                            student_name text,
                            student_last_name text,
                            student_phone text,
                            student_email text,
                            student_address text,
                            student_gender text,
                            student_courses text,
                            student_grade text)""")

        # create instructor table
        self.cursor.execute("""create table if not exists 'instructor' (
                            instructor_id integer primary key autoincrement not null,
                            instructor_name text,
                            instructor_last_name text,
                            instructor_phone text,
                            instructor_email text,
                            instructor_address text,
                            instructor_gender text,
                            instructor_courses text)""")

        # add admin data into admin table
        self.cursor.execute("select * from admin")
        if self.cursor.fetchone() is None:
            self.cursor.execute("""insert into 'admin'
                                (username, password) values ('admin', 'admin')""")
            self.connection.commit()

        # reset primary_key counter if there is no data
        self.cursor.execute("select * from student")
        if self.cursor.fetchone() is None:
            self.cursor.execute("update sqlite_sequence set seq=0 where name='student'")
            self.connection.commit()

        # reset primary_key counter if there is no data
        self.cursor.execute("select * from instructor")
        if self.cursor.fetchone() is None:
            self.cursor.execute("update sqlite_sequence set seq=0 where name='instructor'")
            self.connection.commit()

    # add student to the database
    def add_student(self, name, last_name, phone, email, address, gender, courses, grade):
        data = [name, last_name, phone, email, address, gender, courses, grade]
        query = """insert into student (
                    student_name,
                    student_last_name,
                    student_phone,
                    student_email,
                    student_address,
                    student_gender,
                    student_courses,
                    student_grade)
                    values (?, ?, ?, ?, ?, ?, ?, ?)"""
        self.cursor.execute(query, data)
        self.connection.commit()

    # add instructor to the database
    def add_instructor(self, name, last_name, phone, email, address, gender, courses):
        data = [name, last_name, phone, email, address, gender, courses]
        query = """insert into instructor (
                    instructor_name,
                    instructor_last_name,
                    instructor_phone,
                    instructor_email,
                    instructor_address,
                    instructor_gender,
                    instructor_courses)
                    values (?, ?, ?, ?, ?, ?, ?)"""
        self.cursor.execute(query, data)
        self.connection.commit()

    # delete an item from a table in database
    def delete(self, primary_key, table_name):
        if table_name == 'student':
            query = "delete from student where student_id = ?"
            self.cursor.execute(query, (primary_key,))
            self.connection.commit()
        elif table_name == 'instructor':
            query = "delete from instructor where instructor_id = ?"
            self.cursor.execute(query, (primary_key,))
            self.connection.commit()

    def update(self, primary_key, table_name, data):
        if table_name == 'student':
            query = """update student set
                        student_name = ?,
                        student_last_name = ?,
                        student_phone = ?,
                        student_email = ?,
                        student_address = ?,
                        student_gender = ?,
                        student_courses = ?,
                        student_grade = ?
                        where student_id = """ + str(primary_key)
        elif table_name == 'instructor':
            query = """update instructor set
                        instructor_name = ?,
                        instructor_last_name = ?,
                        instructor_phone = ?,
                        instructor_email = ?,
                        instructor_address = ?,
                        instructor_gender = ?,
                        instructor_courses = ?
                        where instructor_id = """ + str(primary_key)

        self.cursor.execute(query, data)
        self.connection.commit()

    def get_password(self):
        password = ''
        self.cursor.execute("select * from admin")
        for index, row in enumerate(self.cursor.fetchone()):
            if index == 2:
                password = row
        return password

    def get_username(self):
        username = ''
        self.cursor.execute("select * from admin")
        for index, row in enumerate(self.cursor.fetchone()):
            if index == 1:
                username = row
        return username


# creating instance of database
db = Database()


# main application class
class MainApp(QMainWindow, main_window):
    def __init__(self):
        # call the parent constructor
        QMainWindow.__init__(self)

        # setup the user interface
        self.setupUi(self)

        # center the window
        self.center_window()

        # handle button actions
        self.button_handler()

        # handle switch between pages
        self.page_handler()

        # make sure the login page is default
        self.logout()

    # position application window in center
    def center_window(self):
        # geometry of the main window
        frame_geometry = self.frameGeometry()

        # center point of screen
        center_point = QDesktopWidget().availableGeometry().center()

        # move rectangle's center point to screen's center point
        frame_geometry.moveCenter(center_point)

        # top left of rectangle becomes top left of window centering it
        self.move(frame_geometry.topLeft())

    # switch between pages
    def page_handler(self):
        # instructor portal page
        self.instructorPortalButton1.clicked.connect(lambda: self.page('instructorPortal'))
        self.instructorPortalButton2.clicked.connect(lambda: self.page('instructorPortal'))

        # student portal page
        self.studentPortalButton1.clicked.connect(lambda: self.page('studentPortal'))
        self.studentPortalButton2.clicked.connect(lambda: self.page('studentPortal'))

        # go to home page
        self.homeButton1.clicked.connect(lambda: self.page('home'))
        self.homeButton2.clicked.connect(lambda: self.page('home'))

        # add instructor page
        self.addInstructorButton.clicked.connect(lambda: self.page('addInstructor'))

        # view instructor information page
        self.viewInstructorButton.clicked.connect(lambda: self.page('viewInstructor'))

        # add student page
        self.addStudentButton.clicked.connect(lambda: self.page('addStudent'))

        # view student information page
        self.viewStudentButton.clicked.connect(lambda: self.page('viewStudent'))

    # handle actions for each button
    def button_handler(self):
        # login when button is pressed
        self.loginButton.clicked.connect(self.login)

        # logout when button is pressed
        self.logoutButton1.clicked.connect(self.logout)
        self.logoutButton2.clicked.connect(self.logout)
        self.logoutButton3.clicked.connect(self.logout)

        # save new instructor/student to database
        self.saveInstructor.clicked.connect(self.add_instructor)
        self.saveStudent.clicked.connect(self.add_student)

        # delete selected row from database
        self.deleteInstructor.clicked.connect(lambda: self.delete('instructor'))
        self.deleteStudent.clicked.connect(lambda: self.delete('student'))

        # update selected row into database
        self.saveInstructorData.clicked.connect(lambda: self.update_data('instructor'))
        self.saveStudentData.clicked.connect(lambda: self.update_data('student'))

        # search instructor/student in database
        self.searchInstructor.clicked.connect(lambda: self.search('instructor'))
        self.searchStudent.clicked.connect(lambda: self.search('student'))

        # reset input values when reset button is pressed
        self.resetInstructor.clicked.connect(lambda: self.reset('addInstructor'))
        self.resetInstructorTable.clicked.connect(lambda: self.reset('viewInstructor'))
        self.resetStudent.clicked.connect(lambda: self.reset('addStudent'))
        self.resetStudentTable.clicked.connect(lambda: self.reset('viewStudent'))

    # login when correct username and password is entered
    def login(self):
        # get username and password from user input
        entered_username = self.usernameInput.text()
        entered_password = self.passwordInput.text()

        # get username and password form database
        username = db.get_username()
        password = db.get_password()

        # evaluate input username and password
        if username == entered_username and password == entered_password:
            # set home page as current page
            self.page('home')

            # clear the username and password input fields
            self.usernameInput.clear()
            self.passwordInput.clear()
        else:
            # clear the input fields and say try again
            self.usernameInput.clear()
            self.passwordInput.clear()
            self.loginButton.setText('Try again')

    # logout from account and go to login page
    def logout(self):
        # clear the input fields and say try again
        self.usernameInput.clear()
        self.passwordInput.clear()

        # set login page as current page
        self.page('login')
        self.loginButton.setText('Login')

    # show data from database into instructor table
    def view_instructor(self):
        db.cursor.execute('select * from instructor')
        self.view(self.instructorTable)

    # show data from database into student table
    def view_student(self):
        db.cursor.execute('select * from student')
        self.view(self.studentTable)

    # view data in table
    @staticmethod
    def view(widget_name):
        widget_name.setRowCount(0)

        for row_index, row_data in enumerate(db.cursor.fetchall()):
            widget_name.insertRow(row_index)
            for column_index, column_data in enumerate(row_data):
                widget_name.setItem(row_index, column_index, QTableWidgetItem(str(column_data)))

    # get input values for instructor and add to database
    def add_instructor(self):
        # get user input
        name = self.instructorNameInput.text()
        last_name = self.instructorLastnameInput.text()
        phone = self.instructorPhoneInput.text()
        email = self.instructorEmailInput.text()
        address = self.instructorAddressInput.text()
        gender = self.instructorGenderInput.currentText()
        courses = self.instructorCoursesInput.text()

        # add input values into database
        db.add_instructor(name, last_name, phone, email, address, gender, courses)

        # clear the old values
        self.reset('addInstructor')

    # get input values for student and add to database
    def add_student(self):
        # get user input
        name = self.studentNameInput.text()
        last_name = self.studentLastnameInput.text()
        phone = self.studentPhoneInput.text()
        email = self.studentEmailInput.text()
        address = self.studentAddressInput.text()
        gender = self.studentGenderInput.currentText()
        courses = self.studentCoursesInput.text()
        grade = self.studentGradeInput.text()

        # add input values into database
        db.add_student(name, last_name, phone, email, address, gender, courses, grade)

        # clear the old values
        self.reset('addStudent')

    # search in database and show it in its table
    def search(self, table_name):
        if table_name == 'instructor':
            search_item = self.searchInstructorInput.text()
            current_index = self.instructorSearchType.currentIndex()
            widget_name = self.instructorTable
        elif table_name == 'student':
            search_item = self.searchStudentInput.text()
            current_index = self.studentSearchType.currentIndex()
            widget_name = self.studentTable

        if current_index == 0:
            query = "select * from " + table_name + " where " + table_name + "_name like ?"
            db.cursor.execute(query, ("%" + str(search_item) + "%",))
        if current_index == 1:
            query = "select * from " + table_name + " where " + table_name + "_id = ?"
            db.cursor.execute(query, (search_item,))

        self.view(widget_name)

    # delete selected row from database
    def delete(self, table_name):
        if table_name == 'instructor':
            widget_name = self.instructorTable
            reset_name = 'viewInstructor'
        elif table_name == 'student':
            widget_name = self.studentTable
            reset_name = 'viewStudent'

        # get input values from application
        selected_item = widget_name.currentRow()
        primary_key = widget_name.item(selected_item, 0).text()

        # delete item from database
        db.delete(primary_key, table_name)

        # reset current window
        self.reset(reset_name)

    def reset(self, name):
        if name == 'addInstructor':
            self.instructorNameInput.clear()
            self.instructorLastnameInput.clear()
            self.instructorPhoneInput.clear()
            self.instructorEmailInput.clear()
            self.instructorAddressInput.clear()
            self.instructorCoursesInput.clear()
        elif name == 'addStudent':
            self.studentNameInput.clear()
            self.studentLastnameInput.clear()
            self.studentPhoneInput.clear()
            self.studentEmailInput.clear()
            self.studentAddressInput.clear()
            self.studentCoursesInput.clear()
            self.studentGradeInput.clear()
        elif name == 'viewStudent':
            self.searchStudentInput.clear()
            self.view_student()
        elif name == 'viewInstructor':
            self.searchInstructorInput.clear()
            self.view_instructor()
        else:
            print('wrong input values or object names')

    # update an edited row value in database
    def update_data(self, table_name):
        if table_name == 'instructor':
            widget_name = self.instructorTable
            reset_name = 'viewInstructor'
        elif table_name == 'student':
            widget_name = self.studentTable
            reset_name = 'viewStudent'

        # get input values from application
        selected_item = widget_name.currentRow()
        column_count = widget_name.columnCount()
        primary_key = ''
        data = []
        for column in range(0, column_count):
            if column == 0:
                primary_key = widget_name.item(selected_item, column).text()
            else:
                data.append(widget_name.item(selected_item, column).text())

        # update item from database
        db.update(primary_key, table_name, data)

        # reset current window
        self.reset(reset_name)

    def page(self, name):
        if name == 'home':
            self.mainWindows.setCurrentWidget(self.homePage)
        elif name == 'login':
            self.mainWindows.setCurrentWidget(self.loginPage)
        elif name == 'instructorPortal':
            self.mainWindows.setCurrentWidget(self.instructorPortal)
            self.instructorPortalWindows.setCurrentWidget(self.instructorHome)
        elif name == 'addInstructor':
            self.instructorPortalWindows.setCurrentWidget(self.addInstructor)
        elif name == 'viewInstructor':
            self.instructorPortalWindows.setCurrentWidget(self.viewInstructor)
            self.view_instructor()
        elif name == 'studentPortal':
            self.mainWindows.setCurrentWidget(self.studentPortal)
            self.studentPortalWindows.setCurrentWidget(self.studentHome)
        elif name == 'addStudent':
            self.studentPortalWindows.setCurrentWidget(self.addStudent)
        elif name == 'viewStudent':
            self.studentPortalWindows.setCurrentWidget(self.viewStudent)
            self.view_student()
        else:
            print('wrong input name or object name')


def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
