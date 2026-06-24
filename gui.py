import streamlit as st
import requests

st.title("Student App")

url = "http://127.0.0.1:8000"

action = st.sidebar.selectbox(
    "Action",
    [
        "Create",
        "Read",
        "Update",
        "Delete",
        "Create Attendance",
        "Read Attendance",
        "Update Attendance",
        "Delete Attendance",
    ],
)

# =========================
# STUDENTS
# =========================

if action == "Create":
    st.subheader("Create Student")

    name = st.text_input("Name")
    subject = st.text_input("Subject")
    teacher = st.text_input("Teacher")
    grade = st.text_input("Grade")

    if st.button("Add Student"):
        if name and subject and teacher and grade:
            res = requests.post(
                f"{url}/student/",
                json={
                    "name": name,
                    "subject": subject,
                    "teacher": teacher,
                    "grade": grade,
                },
            )

            if res.status_code in [200, 201]:
                st.success("Student added successfully")
            else:
                st.error(res.text)
        else:
            st.warning("Please fill all fields")


elif action == "Read":
    st.subheader("Students")

    if st.button("Refresh Students"):
        st.session_state["students"] = requests.get(
            f"{url}/students/"
        ).json()

    if "students" not in st.session_state:
        st.session_state["students"] = requests.get(
            f"{url}/students/"
        ).json()

    students = st.session_state["students"]

    if students:
        st.dataframe(students, use_container_width=True)
    else:
        st.info("No students found")


elif action == "Update":
    st.subheader("Update Student")

    upd_id = st.number_input("Student ID", min_value=1, step=1)
    name = st.text_input("Name")
    grade = st.text_input("Grade")
    teacher = st.text_input("Teacher")
    subject = st.text_input("Subject")

    if st.button("Update Student"):
        res = requests.put(
            f"{url}/student/{upd_id}",
            json={"name": name, "grade": grade, "teacher": teacher, "subject": subject}
        )
        if res.status_code == 200:
            st.success("Updated")
        else:
            st.error(res.text)


elif action == "Delete":
    st.subheader("Delete Student")

    del_id = st.number_input(
        "Student ID",
        min_value=1,
        step=1,
    )

    if st.button("Delete Student"):
        res = requests.delete(f"{url}/student/{del_id}")

        if res.status_code == 200:
            st.success("Student deleted successfully")
        else:
            st.error(res.text)


# ==========================
# CREATE ATTENDANCE
# ==========================
elif action == "Create Attendance":
    st.subheader("Create Attendance")

    students = requests.get(f"{url}/students/").json()

    if not students:
        st.warning("No students found. Create a student first.")
        st.stop()

    selected_student = st.selectbox(
        "Student",
        options=students,
        format_func=lambda x: f"{x['id']} - {x['name']}"
    )

    att_present = st.selectbox(
        "Present",
        [True, False]
    )

    if st.button("Add Attendance"):
        res = requests.post(
            f"{url}/attendance/",
            json={
                "student_id": selected_student["id"],
                "present": att_present
            }
        )

        if res.status_code in [200, 201]:
            st.success("Attendance added successfully")
        else:
            st.error(res.text)


# ==========================
# READ ATTENDANCE
# ==========================
elif action == "Read Attendance":
    st.subheader("Attendance Records")

    try:
        attendances = requests.get(
            f"{url}/attendances/"
        ).json()

        if attendances:
            st.dataframe(attendances, use_container_width=True)
        else:
            st.info("No attendance records found")

    except Exception as e:
        st.error(str(e))


# ==========================
# UPDATE ATTENDANCE
# ==========================
elif action == "Update Attendance":
    st.subheader("Update Attendance")

    attendances = requests.get(
        f"{url}/attendances/"
    ).json()

    if not attendances:
        st.warning("No attendance records found")
        st.stop()

    selected_attendance = st.selectbox(
        "Select Attendance Record",
        options=attendances,
        format_func=lambda x: (
            f"ID {x['id']} | "
            f"Student {x['student_id']} | "
            f"Present: {x['present']}"
        )
    )

    upd_att_sid = st.number_input(
        "Student ID",
        min_value=1,
        value=selected_attendance["student_id"]
    )

    upd_att_present = st.selectbox(
        "Present",
        [True, False],
        index=0 if selected_attendance["present"] else 1
    )

    if st.button("Update Attendance"):
        res = requests.put(
            f"{url}/attendance/{selected_attendance['id']}",
            json={
                "student_id": upd_att_sid,
                "present": upd_att_present
            }
        )

        if res.status_code == 200:
            st.success("Attendance updated successfully")
        else:
            st.error(res.text)


# ==========================
# DELETE ATTENDANCE
# ==========================
elif action == "Delete Attendance":
    st.subheader("Delete Attendance")

    attendances = requests.get(
        f"{url}/attendances/"
    ).json()

    if not attendances:
        st.warning("No attendance records found")
        st.stop()

    selected_attendance = st.selectbox(
        "Select Attendance Record",
        options=attendances,
        format_func=lambda x: (
            f"ID {x['id']} | "
            f"Student {x['student_id']} | "
            f"Present: {x['present']}"
        )
    )

    if st.button("Delete Attendance"):
        res = requests.delete(
            f"{url}/attendance/{selected_attendance['id']}"
        )

        if res.status_code == 200:
            st.success("Attendance deleted successfully")
        else:
            st.error(res.text)