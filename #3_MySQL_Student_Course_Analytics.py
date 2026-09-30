"""Q3: Import CSV student/registration data and query a MySQL database.

Install: python -m pip install mysql-connector-python
CSV headers:
students.csv: student_id,name,spi
registration.csv: student_id,course_id
"""
import csv
import getpass
import sys

try:
    import mysql.connector
    from mysql.connector import Error
except ImportError:
    mysql = None
    Error = Exception


def read_csv(path):
    with open(path, newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def main():
    if "mysql" not in globals() or mysql is None:
        print("Missing dependency. Install mysql-connector-python.")
        return
    host = input("MySQL host [localhost]: ").strip() or "localhost"
    user = input("MySQL user: ").strip()
    password = getpass.getpass("MySQL password: ")
    database = input("Database name: ").strip()
    student_csv = input("Student CSV path: ").strip()
    registration_csv = input("Registration CSV path: ").strip()
    course_id = input("Course ID: ").strip()
    try:
        threshold = float(input("SPI threshold: "))
        if not 0 <= threshold <= 10:
            raise ValueError
        students = read_csv(student_csv)
        registrations = read_csv(registration_csv)
    except (ValueError, OSError) as exc:
        print(f"Input error: {exc}")
        return

    connection = None
    try:
        connection = mysql.connector.connect(host=host, user=user, password=password, database=database)
        cursor = connection.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS Student (
            student_id VARCHAR(40) PRIMARY KEY,
            name VARCHAR(200) NOT NULL,
            spi DECIMAL(4,2) NOT NULL
        )""")
        cursor.execute("""CREATE TABLE IF NOT EXISTS CourseRegistration (
            student_id VARCHAR(40) NOT NULL,
            course_id VARCHAR(40) NOT NULL,
            PRIMARY KEY (student_id, course_id),
            FOREIGN KEY (student_id) REFERENCES Student(student_id)
        )""")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_registration_course ON CourseRegistration(course_id)")
        cursor.executemany(
            "INSERT INTO Student(student_id,name,spi) VALUES(%s,%s,%s) "
            "ON DUPLICATE KEY UPDATE name=VALUES(name), spi=VALUES(spi)",
            [(r["student_id"], r["name"], float(r["spi"])) for r in students],
        )
        cursor.executemany(
            "INSERT IGNORE INTO CourseRegistration(student_id,course_id) VALUES(%s,%s)",
            [(r["student_id"], r["course_id"]) for r in registrations],
        )
        connection.commit()
        cursor.execute(
            """SELECT s.student_id, s.name, s.spi, r.course_id
               FROM Student s JOIN CourseRegistration r ON r.student_id=s.student_id
               WHERE r.course_id=%s AND s.spi>%s
               ORDER BY s.spi DESC, s.student_id ASC""",
            (course_id, threshold),
        )
        for row in cursor.fetchall():
            print(*row)
        cursor.close()
    except Error as exc:
        if connection:
            connection.rollback()
        print(f"Database error: {exc}")
    finally:
        if connection and connection.is_connected():
            connection.close()


if __name__ == "__main__":
    main()
