import streamlit as st
import requests

from Module import student

st.title("Student App")
action = st.sidebar.selectbox("Action", ["Create", "Update", "Read" ,"Delete", "Create Attendance ", "Update Attendance", "Read Attendance" ,"Delete Attendance"])
url = "http://127.0.0.1:8000"

if action == "Create":
    name = st.text_input("Name")
    subject = st.text_input("Subject")
    teacher = st.text_input("Teacher")
    grade = st.text_input("Grade")
    if st.button("Add Student"):
        if name and grade and teacher and subject:
            res = requests.post(f"{url}/student/", json={
                "name": name, "grade": grade, "teacher": teacher, "subject": subject
            })
elif action == "Read":
    if st.button("Refresh Students"):
        st.session_state["students"] = requests.get(f"{url}/students/").json()

    if "students" not in st.session_state:
        st.session_state["students"] = requests.get(f"{url}/students/").json()

    students = st.session_state["students"]
    if students:
        st.dataframe(students, use_container_width=True)
    else:
        st.info("No students found")
elif action == "Update":

    st.subheader("Update Student")
    upd_id = st.number_input("Student ID to update", min_value=1, step=1, key="upd_id")
    upd_name = st.text_input("New Name", key="upd_name", value=student)
    upd_grade = st.text_input("New Grade", key="upd_grade", value=student)
    upd_teacher = st.text_input("New Teacher", key="upd_teacher", value=student)
    upd_subject = st.text_input("New Subject", key="upd_subject", value=student)
    if st.button("Submit"):
        if upd_name and upd_grade and upd_teacher and upd_subject:
            res = requests.put(f"{url}/student/{upd_id}", json={
                "name": upd_name, "grade": upd_grade,
                "teacher": upd_teacher, "subject": upd_subject
            })
# Fix Update Student to have the info already filled in when chosen the id where there is a drop down of wich one to choose
elif action =="Delete":
        st.subheader("Delete Student")
        del_id = st.number_input("Student ID to delete", min_value=1, step=1, key="del_id")

        if st.button("Delete Student"):
            res = requests.delete(f"{url}/student/{del_id}")

# ── Attendance ──────────────────────────────────────────────────────

elif action == "Create Attendance ":
    att_student_id = st.number_input(
        "Student ID",
        min_value=1,
        step=1,
        key="att_sid"
    )

    att_present = st.selectbox(
        "Present",
        ["True", "False"]
    )

    if st.button("Add Attendance"):
        res = requests.post(
            f"{url}/attendance/",
            json={
                "student_id": att_student_id,
                "present": att_present == "True"
            }
        )

elif action == "Read Attendance":
    if st.button("Refresh Attendance"):
        st.session_state["attendances"] = requests.get(
            f"{url}/attendances/"
        ).json()

    if "attendances" not in st.session_state:
        st.session_state["attendances"] = requests.get(
            f"{url}/attendances/"
        ).json()

    attendances = st.session_state["attendances"]

    if attendances:
        st.dataframe(attendances, use_container_width=True)
    else:
        st.info("No attendance records found")

elif action == "Update Attendance":
    upd_att_id = st.number_input(
        "Attendance ID to update",
        min_value=1,
        step=1,
        key="upd_att_id"
    )

    upd_att_sid = st.number_input(
        "New Student ID",
        min_value=1,
        step=1,
        key="upd_att_sid"
    )

    upd_att_present = st.selectbox(
        "Present",
        ["True", "False"],
        key="upd_att_present"
    )

    if st.button("Update Attendance"):
        res = requests.put(
            f"{url}/attendance/{upd_att_id}",
            json={
                "student_id": upd_att_sid,
                "present": upd_att_present == "True"
            }
        )

elif action == "Delete Attendance":
    del_att_id = st.number_input(
        "Attendance ID to delete",
        min_value=1,
        step=1,
        key="del_att_id"
    )

    if st.button("Delete Attendance"):
        res = requests.delete(
            f"{url}/attendance/{del_att_id}"
        )