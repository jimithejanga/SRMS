from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table, DateTime, Boolean, Float, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime

Base = declarative_base()

# Association table for student-course enrollment
enrollment = Table(
    'enrollment',
    Base.metadata,
    Column('student_id', Integer, ForeignKey('students.id'), primary_key=True),
    Column('course_id', Integer, ForeignKey('courses.id'), primary_key=True),
    Column('enrollment_date', DateTime, default=datetime.utcnow),
    Column('is_active', Boolean, default=True)
)

class Grade(Base):
    __tablename__ = 'grades'
    
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)
    course_id = Column(Integer, ForeignKey('courses.id'), nullable=False)
    semester = Column(String(20), nullable=False)  # e.g., "Fall 2024"
    grade_point = Column(Float, nullable=False)  # e.g., 4.0, 3.7, etc.
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    student = relationship("Student", back_populates="grades")
    course = relationship("Course", back_populates="grades")
    
    def __repr__(self):
        return f"<Grade - Student: {self.student_id}, Course: {self.course_id}, GP: {self.grade_point}>"

class Student(Base):
    __tablename__ = 'students'
    
    id = Column(Integer, primary_key=True)
    student_number = Column(String(10), unique=True, nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    date_of_birth = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    courses = relationship('Course', secondary=enrollment, back_populates='students')
    grades = relationship('Grade', back_populates='student')
    
    def __repr__(self):
        return f"<Student {self.student_number}: {self.first_name} {self.last_name}>"
    
    def calculate_cgpa(self, session):
        """Calculate CGPA for the student across all courses"""
        total_credits = 0
        weighted_sum = 0
        
        for grade in self.grades:
            course = grade.course
            weighted_sum += grade.grade_point * course.credits
            total_credits += course.credits
            
        if total_credits == 0:
            return 0.0
        
        return round(weighted_sum / total_credits, 2)
    
    def calculate_semester_gpa(self, session, semester):
        """Calculate GPA for a specific semester"""
        total_credits = 0
        weighted_sum = 0
        
        semester_grades = session.query(Grade).filter(
            Grade.student_id == self.id,
            Grade.semester == semester
        ).all()
        
        for grade in semester_grades:
            course = grade.course
            weighted_sum += grade.grade_point * course.credits
            total_credits += course.credits
            
        if total_credits == 0:
            return 0.0
        
        return round(weighted_sum / total_credits, 2)

class Course(Base):
    __tablename__ = 'courses'
    
    id = Column(Integer, primary_key=True)
    course_code = Column(String(10), unique=True, nullable=False)
    title = Column(String(100), nullable=False)
    description = Column(String(500))
    credits = Column(Integer, nullable=False)
    max_students = Column(Integer)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    students = relationship('Student', secondary=enrollment, back_populates='courses')
    grades = relationship('Grade', back_populates='course')
    
    def __repr__(self):
        return f"<Course {self.course_code}: {self.title}>"

# Create SQLite database engine
engine = create_engine('sqlite:///school.db', echo=True)

# Create all tables
Base.metadata.create_all(engine)

# Create session factory
Session = sessionmaker(bind=engine)