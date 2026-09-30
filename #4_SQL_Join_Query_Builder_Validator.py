"""Q4: Whitelisted SQL join builder with parameterized filter values.

This program prints the generated SQL and parameters. Set up the documented
schema and enable the optional execution block if database execution is needed.
"""
import json
import re

TABLES = {
    "student": {"table": "Student", "columns": {"id": "student_id", "name": "name", "spi": "spi"}},
    "course": {"table": "Course", "columns": {"id": "course_id", "name": "name"}},
    "registration": {"table": "CourseRegistration", "columns": {"student_id": "student_id", "course_id": "course_id"}},
}
PROJECTIONS = {
    "student.id": "s.student_id", "student.name": "s.name", "student.spi": "s.spi",
    "course.id": "c.course_id", "course.name": "c.name",
    "registration.course_id": "r.course_id", "registration.student_id": "r.student_id",
}
FILTERS = {
    "student.id": "s.student_id", "student.name": "s.name", "student.spi": "s.spi",
    "course.id": "c.course_id", "course.name": "c.name",
    "registration.course_id": "r.course_id", "registration.student_id": "r.student_id",
}
OPERATORS = {"=", "!=", ">", ">=", "<", "<=", "LIKE", "BETWEEN"}


def build_query(spec):
    columns = spec.get("columns", [])
    if not columns or any(col not in PROJECTIONS for col in columns):
        raise ValueError("Invalid or empty projection list")
    sql_columns = ", ".join(PROJECTIONS[col] for col in columns)
    sql = (
        f"SELECT {sql_columns} FROM Student s "
        "JOIN CourseRegistration r ON r.student_id=s.student_id "
        "JOIN Course c ON c.course_id=r.course_id"
    )
    params = []
    conditions = []
    for item in spec.get("where", []):
        field, op, value = item.get("field"), item.get("op", "=").upper(), item.get("value")
        if field not in FILTERS or op not in OPERATORS:
            raise ValueError("Invalid filter field/operator")
        if op == "BETWEEN":
            if not isinstance(value, list) or len(value) != 2:
                raise ValueError("BETWEEN requires a two-item value list")
            conditions.append(f"{FILTERS[field]} BETWEEN %s AND %s")
            params.extend(value)
        else:
            conditions.append(f"{FILTERS[field]} {op} %s")
            params.append(value)
    if conditions:
        sql += " WHERE " + " AND ".join(conditions)

    order = spec.get("order_by")
    if order:
        field = order.get("field")
        direction = str(order.get("direction", "ASC")).upper()
        if field not in FILTERS or direction not in {"ASC", "DESC"}:
            raise ValueError("Invalid ORDER BY")
        sql += f" ORDER BY {FILTERS[field]} {direction}"

    limit = spec.get("limit", 100)
    if not isinstance(limit, int) or not 1 <= limit <= 1000:
        raise ValueError("LIMIT must be an integer from 1 to 1000")
    sql += " LIMIT %s"
    params.append(limit)
    return sql, params


def main():
    print('Enter JSON (example: {"columns":["student.name","course.name"],"where":[{"field":"course.id","op":"=","value":"PY101"}],"order_by":{"field":"student.spi","direction":"DESC"},"limit":2})')
    try:
        spec = json.loads(input())
        sql, params = build_query(spec)
    except (ValueError, json.JSONDecodeError) as exc:
        print("INVALID:", exc)
        return
    print("SQL_OK")
    print(sql)
    print("PARAMS", repr(params))


if __name__ == "__main__":
    main()
