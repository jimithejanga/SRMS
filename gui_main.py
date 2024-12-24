# gui_main.py
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QTabWidget, 
                           QVBoxLayout, QHBoxLayout, QFormLayout, QPushButton, 
                           QLabel, QLineEdit, QMessageBox, QTableWidget, 
                           QTableWidgetItem, QComboBox, QSpinBox, QDoubleSpinBox)
from PyQt5.QtCore import Qt
import sys
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

# Import from models.py
from db_models import Base, Student, Course, Grade, enrollment

class SchoolManagementSystem(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("School Management System")
        self.setGeometry(100, 100, 800, 600)
        
        # Initialize database connection
        self.engine = create_engine('sqlite:///school.db', echo=True)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        
        # Create main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout()
        main_widget.setLayout(layout)
        
        # Create tab widget
        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)
        
        # Initialize UI elements as class attributes
        self.init_ui_elements()
        
        # Add tabs
        self.tabs.addTab(self.create_students_tab(), "Students")
        self.tabs.addTab(self.create_courses_tab(), "Courses")
        self.tabs.addTab(self.create_enrollment_tab(), "Enrollment")
        self.tabs.addTab(self.create_grades_tab(), "Grades")
        
        # Initial refresh of all data
        self.refresh_all_data()

    def init_ui_elements(self):
        # Student form elements
        self.student_number_input = QLineEdit()
        self.first_name_input = QLineEdit()
        self.last_name_input = QLineEdit()
        self.email_input = QLineEdit()
        
        # Course form elements
        self.course_code_input = QLineEdit()
        self.course_title_input = QLineEdit()
        self.credits_input = QSpinBox()
        self.max_students_input = QSpinBox()
        
        # Enrollment form elements
        self.student_select = QComboBox()
        self.course_select = QComboBox()
        
        # Grade form elements
        self.grade_student_select = QComboBox()
        self.grade_course_select = QComboBox()
        self.semester_input = QLineEdit()
        self.grade_point_input = QDoubleSpinBox()
        
        # Initialize tables
        self.students_table = QTableWidget()
        self.courses_table = QTableWidget()
        self.enrollments_table = QTableWidget()
        self.grades_table = QTableWidget()

    def create_students_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Form for adding students
        form_layout = QFormLayout()
        
        form_layout.addRow("Student Number:", self.student_number_input)
        form_layout.addRow("First Name:", self.first_name_input)
        form_layout.addRow("Last Name:", self.last_name_input)
        form_layout.addRow("Email:", self.email_input)
        
        add_button = QPushButton("Add Student")
        add_button.clicked.connect(self.add_student)
        
        layout.addLayout(form_layout)
        layout.addWidget(add_button)
        
        # Table setup
        self.students_table.setColumnCount(6)
        self.students_table.setHorizontalHeaderLabels(
            ["ID", "Student Number", "First Name", "Last Name", "Email", "CGPA"]
        )
        layout.addWidget(self.students_table)
        
        # Refresh button
        refresh_button = QPushButton("Refresh")
        refresh_button.clicked.connect(self.refresh_students)
        layout.addWidget(refresh_button)
        
        tab.setLayout(layout)
        return tab

    def create_courses_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Form for adding courses
        form_layout = QFormLayout()
        
        self.credits_input.setRange(1, 6)
        self.max_students_input.setRange(1, 200)
        
        form_layout.addRow("Course Code:", self.course_code_input)
        form_layout.addRow("Title:", self.course_title_input)
        form_layout.addRow("Credits:", self.credits_input)
        form_layout.addRow("Max Students:", self.max_students_input)
        
        add_button = QPushButton("Add Course")
        add_button.clicked.connect(self.add_course)
        
        layout.addLayout(form_layout)
        layout.addWidget(add_button)
        
        # Table setup
        self.courses_table.setColumnCount(5)
        self.courses_table.setHorizontalHeaderLabels(
            ["ID", "Code", "Title", "Credits", "Max Students"]
        )
        layout.addWidget(self.courses_table)
        
        refresh_button = QPushButton("Refresh")
        refresh_button.clicked.connect(self.refresh_courses)
        layout.addWidget(refresh_button)
        
        tab.setLayout(layout)
        return tab

    def create_enrollment_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        
        form_layout = QFormLayout()
        form_layout.addRow("Student:", self.student_select)
        form_layout.addRow("Course:", self.course_select)
        
        enroll_button = QPushButton("Enroll")
        enroll_button.clicked.connect(self.enroll_student_in_course)
        
        layout.addLayout(form_layout)
        layout.addWidget(enroll_button)
        
        # Table setup
        self.enrollments_table.setColumnCount(3)
        self.enrollments_table.setHorizontalHeaderLabels(
            ["Student", "Course", "Enrollment Date"]
        )
        layout.addWidget(self.enrollments_table)
        
        refresh_button = QPushButton("Refresh")
        refresh_button.clicked.connect(self.refresh_enrollments)
        layout.addWidget(refresh_button)
        
        tab.setLayout(layout)
        return tab

    def create_grades_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        
        form_layout = QFormLayout()
        
        self.grade_point_input.setRange(0, 4.0)
        self.grade_point_input.setDecimals(1)
        self.grade_point_input.setSingleStep(0.1)
        
        form_layout.addRow("Student:", self.grade_student_select)
        form_layout.addRow("Course:", self.grade_course_select)
        form_layout.addRow("Semester:", self.semester_input)
        form_layout.addRow("Grade Point:", self.grade_point_input)
        
        add_button = QPushButton("Add Grade")
        add_button.clicked.connect(self.add_grade_record)
        
        layout.addLayout(form_layout)
        layout.addWidget(add_button)
        
        # Table setup
        self.grades_table.setColumnCount(5)
        self.grades_table.setHorizontalHeaderLabels(
            ["Student", "Course", "Semester", "Grade", "Date"]
        )
        layout.addWidget(self.grades_table)
        
        refresh_button = QPushButton("Refresh")
        refresh_button.clicked.connect(self.refresh_grades)
        layout.addWidget(refresh_button)
        
        tab.setLayout(layout)
        return tab

    def add_student(self):
        try:
            student = Student(
                student_number=self.student_number_input.text(),
                first_name=self.first_name_input.text(),
                last_name=self.last_name_input.text(),
                email=self.email_input.text()
            )
            self.session.add(student)
            self.session.commit()
            
            self.refresh_students()
            self.clear_student_inputs()
            QMessageBox.information(self, "Success", "Student added successfully!")
        except SQLAlchemyError as e:
            self.session.rollback()
            QMessageBox.critical(self, "Error", str(e))

    def add_course(self):
        try:
            course = Course(
                course_code=self.course_code_input.text(),
                title=self.course_title_input.text(),
                credits=self.credits_input.value(),
                max_students=self.max_students_input.value()
            )
            self.session.add(course)
            self.session.commit()
            
            self.refresh_courses()
            self.clear_course_inputs()
            QMessageBox.information(self, "Success", "Course added successfully!")
        except SQLAlchemyError as e:
            self.session.rollback()
            QMessageBox.critical(self, "Error", str(e))

    def enroll_student_in_course(self):
        try:
            student_id = self.student_select.currentData()
            course_id = self.course_select.currentData()
            
            student = self.session.query(Student).get(student_id)
            course = self.session.query(Course).get(course_id)
            
            if not student or not course:
                raise ValueError("Student or course not found")
                
            if course not in student.courses:
                student.courses.append(course)
                self.session.commit()
                self.refresh_enrollments()
                QMessageBox.information(self, "Success", "Student enrolled successfully!")
            else:
                QMessageBox.warning(self, "Warning", "Student already enrolled in this course")
        except Exception as e:
            self.session.rollback()
            QMessageBox.critical(self, "Error", str(e))

    def add_grade_record(self):
        try:
            student_id = self.grade_student_select.currentData()
            course_id = self.grade_course_select.currentData()
            
            grade = Grade(
                student_id=student_id,
                course_id=course_id,
                semester=self.semester_input.text(),
                grade_point=self.grade_point_input.value()
            )
            self.session.add(grade)
            self.session.commit()
            
            self.refresh_grades()
            self.clear_grade_inputs()
            QMessageBox.information(self, "Success", "Grade added successfully!")
        except SQLAlchemyError as e:
            self.session.rollback()
            QMessageBox.critical(self, "Error", str(e))

    def refresh_all_data(self):
        self.refresh_students()
        self.refresh_courses()
        self.refresh_enrollments()
        self.refresh_grades()
        self.update_student_combos()
        self.update_course_combos()

    # [Include all the refresh and helper methods from the previous implementation]
    def refresh_students(self):
        students = self.session.query(Student).all()
        self.students_table.setRowCount(len(students))
        for i, student in enumerate(students):
            self.students_table.setItem(i, 0, QTableWidgetItem(str(student.id)))
            self.students_table.setItem(i, 1, QTableWidgetItem(student.student_number))
            self.students_table.setItem(i, 2, QTableWidgetItem(student.first_name))
            self.students_table.setItem(i, 3, QTableWidgetItem(student.last_name))
            self.students_table.setItem(i, 4, QTableWidgetItem(student.email))
            cgpa = student.calculate_cgpa(self.session)
            self.students_table.setItem(i, 5, QTableWidgetItem(f"{cgpa:.2f}"))

    def refresh_courses(self):
        courses = self.session.query(Course).filter_by(is_active=True).all()
        self.courses_table.setRowCount(len(courses))
        for i, course in enumerate(courses):
            self.courses_table.setItem(i, 0, QTableWidgetItem(str(course.id)))
            self.courses_table.setItem(i, 1, QTableWidgetItem(course.course_code))
            self.courses_table.setItem(i, 2, QTableWidgetItem(course.title))
            self.courses_table.setItem(i, 3, QTableWidgetItem(str(course.credits)))
            self.courses_table.setItem(i, 4, QTableWidgetItem(str(course.max_students)))

    def refresh_enrollments(self):
        enrollments = self.session.query(enrollment).all()
        self.enrollments_table.setRowCount(len(enrollments))
        for i, enroll in enumerate(enrollments):
            student = self.session.query(Student).get(enroll.student_id)
            course = self.session.query(Course).get(enroll.course_id)
            self.enrollments_table.setItem(i, 0, QTableWidgetItem(f"{student.first_name} {student.last_name}"))
            self.enrollments_table.setItem(i, 1, QTableWidgetItem(course.course_code))
            self.enrollments_table.setItem(i, 2, QTableWidgetItem(str(enroll.enrollment_date)))

    def refresh_grades(self):
        grades = self.session.query(Grade).all()
        self.grades_table.setRowCount(len(grades))
        for i, grade in enumerate(grades):
            student = grade.student
            course = grade.course
            self.grades_table.setItem(i, 0, QTableWidgetItem(f"{student.first_name} {student.last_name}"))
            self.grades_table.setItem(i, 1, QTableWidgetItem(course.course_code))
            self.grades_table.setItem(i, 2, QTableWidgetItem(grade.semester))
            self.grades_table.setItem(i, 3, QTableWidgetItem(str(grade.grade_point)))
            self.grades_table.setItem(i, 4, QTableWidgetItem(str(grade.created_at)))

    def update_student_combos(self):
        students = self.session.query(Student).all()
        self.student_select.clear()
        self.grade_student_select.clear()
        for student in students:
            text = f"{student.student_number} - {student.first_name} {student.last_name}"
            self.student_select.addItem(text, student.id)
            self.grade_student_select.addItem(text, student.id)

    def update_course_combos(self):
        courses = self.session.query(Course).filter_by(is_active=True).all()
        self.course_select.clear()
        self.grade_course_select.clear()
        for course in courses:
            text = f"{course.course_code} - {course.title}"
            self.course_select.addItem(text, course.id)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = SchoolManagementSystem()
    main_window.show()
    sys.exit(app.exec())  
