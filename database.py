import sqlite3
# Assuming student and studentCreate are Pydantic models or classes in Module.py
from Module import student, studentCreate


def create_connection():
    connection = sqlite3.connect('student.db')
    connection.row_factory = sqlite3.Row
    return connection


def create_table():
    """Creates the student table in the database if it doesn't exist."""
    with create_connection() as connection:
        cursor = connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Student_grade (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                st_name TEXT NOT NULL,
                st_grade TEXT NOT NULL,
                st_teacher TEXT NOT NULL,
                st_subject TEXT NOT NULL
            )
        ''')
        connection.commit()


create_table()


def create_student(student_data: studentCreate) -> int:
    with create_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO Student_grade (st_name, st_grade, st_teacher, st_subject) VALUES (?, ?, ?, ?)",
            (student_data.name, student_data.grade, student_data.teacher, student_data.subject)
        )
        connection.commit()
        return cursor.lastrowid


def read_students():
    """Retrieves all students from the database."""
    with create_connection() as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Student_grade")
        rows = cursor.fetchall()

        # SQLite Row objects allow dictionary-like access using the exact column names
        return [
            student(
                id=row['id'],
                name=row['st_name'],
                grade=row['st_grade'],
                teacher=row['st_teacher'],
                subject=row['st_subject']
            ) for row in rows
        ]


def read_student(student_id: int):
    """Retrieves a single student from the database by its ID."""
    with create_connection() as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Student_grade WHERE id = ?", (student_id,))
        row = cursor.fetchone()

        if row is None:
            return None

        return student(
            id=row['id'],
            name=row['st_name'],
            grade=row['st_grade'],
            teacher=row['st_teacher'],
            subject=row['st_subject']
        )


def update_student(student_id: int, student_data: studentCreate) -> bool:
    """Updates an existing student in the database."""
    with create_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(
            """
            UPDATE Student_grade 
            SET st_name = ?, st_grade = ?, st_teacher = ?, st_subject = ? 
            WHERE id = ?
            """,
            (student_data.name, student_data.grade, student_data.teacher, student_data.subject, student_id)
        )
        connection.commit()
        return cursor.rowcount > 0


def delete_student(student_id: int) -> bool:
    """Deletes a student from the database by its ID."""
    with create_connection() as connection:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM Student_grade WHERE id = ?", (student_id,))
        connection.commit()
        return cursor.rowcount > 0
