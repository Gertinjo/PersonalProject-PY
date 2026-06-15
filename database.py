import sqlite3
from Module import student, studentCreate, attendance, attendanceCreate


def create_connection():
    connection = sqlite3.connect('student.db')
    connection.row_factory = sqlite3.Row
    return connection


def create_table():
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
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Attendance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                present INTEGER NOT NULL,
                FOREIGN KEY (student_id) REFERENCES Student_grade(id)
            )
        ''')
        connection.commit()


create_table()


# ── Student CRUD ─────────────────────────────────────────────────────────────

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
    with create_connection() as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Student_grade")
        rows = cursor.fetchall()
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
    with create_connection() as connection:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM Student_grade WHERE id = ?", (student_id,))
        connection.commit()
        return cursor.rowcount > 0


# ── Attendance CRUD ───────────────────────────────────────────────────────────

def create_attendance(data: attendanceCreate) -> int:
    with create_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO Attendance (student_id, present) VALUES (?, ?)",
            (data.student_id, int(data.present))
        )
        connection.commit()
        return cursor.lastrowid


def read_attendances():
    with create_connection() as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Attendance")
        rows = cursor.fetchall()
        return [
            attendance(id=row['id'], student_id=row['student_id'], present=bool(row['present']))
            for row in rows
        ]


def read_attendance(attendance_id: int):
    with create_connection() as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Attendance WHERE id = ?", (attendance_id,))
        row = cursor.fetchone()
        if row is None:
            return None
        return attendance(id=row['id'], student_id=row['student_id'], present=bool(row['present']))


def update_attendance(attendance_id: int, data: attendanceCreate) -> bool:
    with create_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE Attendance SET student_id = ?, present = ? WHERE id = ?",
            (data.student_id, int(data.present), attendance_id)
        )
        connection.commit()
        return cursor.rowcount > 0


def delete_attendance(attendance_id: int) -> bool:
    with create_connection() as connection:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM Attendance WHERE id = ?", (attendance_id,))
        connection.commit()
        return cursor.rowcount > 0
