import sqlite3
from Module import Student, StudentCreate


def create_connection():
    """Creates a connection to the SQLite database."""
    connection = sqlite3.connect("student.db")
    connection.row_factory = sqlite3.Row
    return connection


def create_table():
    """Creates the books table in the database if it doesn't exist."""
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Student_grade (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            st.name TEXT NOT NULL,
            st.grade TEXT NOT NULL,
            st.teacher TEXT not Null,
            st.subject TEXT not NUll
        )
    """)
    connection.commit()
    connection.close()


create_table()


def create_book(Student: StudentCreate) -> int:
    """Adds a new book to the database."""
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO Student (st.name, st.grade, st.teacher, st.subject) VALUES (?, ?, ?, ?)", (Student.st.name, Student.st.grade, Student.st.teacher, Student.st.subject))
    connection.commit()
    Student_id = cursor.lastrowid
    connection.close()
    return Student_id


def read_Student():
    """Retrieves all books from the database."""
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Student_grade")
    rows = cursor.fetchall()
    connection.close()
    Students = [Student(id=row[0], name=row[1], grade=row[2], teacher=row[3], subject=row[4]) for row in rows]
    return Students


def read_book(Student_id: int):
    """Retrieves a single book from the database by its ID."""
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Student_grade WHERE id = ?", (Student_id,))
    row = cursor.fetchone()
    connection.close()
    if row is None:
        return None
    return Student(id=row["id"], name=row["name"], grade=row["grade"], teacher=row["teacher"], subject=row["subject"])


def update_book(Student_id: int, Student: StudentCreate) -> bool:
    """Updates an existing book in the database."""
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("UPDATE Student_grade SET title = ?, author = ?, grade = ?, teacher = ?, subject = ? WHERE id = ?", (Student.name, Student.grade, Student.id, Student.teacher, Student.subject))
    connection.commit()
    updated = cursor.rowcount
    connection.close()
    return updated > 0


def delete_book(Student_id: int) -> bool:
    """Deletes a book from the database by its ID."""
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM Student_grade WHERE id = ?", (Student_id,))
    connection.commit()
    deleted = cursor.rowcount
    connection.close()
    return deleted > 0
