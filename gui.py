import streamlit as st
import requests

BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Student Manager", layout="wide")
st.title("Student Manager")

tab1, tab2 = st.tabs(["Students", "Attendance"])


# ── Students ──────────────────────────────────────────────────────────────────

with tab1:
    st.header("Students")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Add Student")
        name = st.text_input("Name")
        grade = st.text_input("Grade")
        teacher = st.text_input("Teacher")
        subject = st.text_input("Subject")

        if st.button("Add Student"):
            if name and grade and teacher and subject:
                res = requests.post(f"{BASE_URL}/student/", json={
                    "name": name, "grade": grade, "teacher": teacher, "subject": subject
                })
                if res.status_code == 200:
                    st.success("Student added successfully")
                else:
                    st.error("Failed to add student")
            else:
                st.warning("Please fill in all fields")

    with col2:
        st.subheader("All Students")
        if st.button("Refresh Students"):
            st.session_state["students"] = requests.get(f"{BASE_URL}/students/").json()

        if "students" not in st.session_state:
            st.session_state["students"] = requests.get(f"{BASE_URL}/students/").json()

        students = st.session_state["students"]
        if students:
            st.dataframe(students, use_container_width=True)
        else:
            st.info("No students found")

    st.divider()

    col3, col4 = st.columns(2)

    with col3:
        st.subheader("Update Student")
        upd_id = st.number_input("Student ID to update", min_value=1, step=1, key="upd_id")
        upd_name = st.text_input("New Name", key="upd_name")
        upd_grade = st.text_input("New Grade", key="upd_grade")
        upd_teacher = st.text_input("New Teacher", key="upd_teacher")
        upd_subject = st.text_input("New Subject", key="upd_subject")

        if st.button("Update Student"):
            if upd_name and upd_grade and upd_teacher and upd_subject:
                res = requests.put(f"{BASE_URL}/student/{upd_id}", json={
                    "name": upd_name, "grade": upd_grade,
                    "teacher": upd_teacher, "subject": upd_subject
                })
                if res.status_code == 200:
                    st.success("Student updated successfully")
                else:
                    st.error("Student not found")
            else:
                st.warning("Please fill in all fields")

    with col4:
        st.subheader("Delete Student")
        del_id = st.number_input("Student ID to delete", min_value=1, step=1, key="del_id")

        if st.button("Delete Student"):
            res = requests.delete(f"{BASE_URL}/student/{del_id}")
            if res.status_code == 200:
                st.success("Student deleted successfully")
            else:
                st.error("Student not found")


# ── Attendance ────────────────────────────────────────────────────────────────

with tab2:
    st.header("Attendance")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Add Attendance")
        att_student_id = st.number_input("Student ID", min_value=1, step=1, key="att_sid")
        att_present = st.selectbox("Present", ["True", "False"])

        if st.button("Add Attendance"):
            res = requests.post(f"{BASE_URL}/attendance/", json={
                "student_id": att_student_id,
                "present": att_present == "True"
            })
            if res.status_code == 200:
                st.success("Attendance recorded")
            else:
                st.error("Failed to record attendance")

    with col2:
        st.subheader("All Attendance Records")
        if st.button("Refresh Attendance"):
            st.session_state["attendances"] = requests.get(f"{BASE_URL}/attendances/").json()

        if "attendances" not in st.session_state:
            st.session_state["attendances"] = requests.get(f"{BASE_URL}/attendances/").json()

        attendances = st.session_state["attendances"]
        if attendances:
            st.dataframe(attendances, use_container_width=True)
        else:
            st.info("No attendance records found")

    st.divider()

    col3, col4 = st.columns(2)

    with col3:
        st.subheader("Update Attendance")
        upd_att_id = st.number_input("Attendance ID to update", min_value=1, step=1, key="upd_att_id")
        upd_att_sid = st.number_input("New Student ID", min_value=1, step=1, key="upd_att_sid")
        upd_att_present = st.selectbox("Present", ["True", "False"], key="upd_att_present")

        if st.button("Update Attendance"):
            res = requests.put(f"{BASE_URL}/attendance/{upd_att_id}", json={
                "student_id": upd_att_sid,
                "present": upd_att_present == "True"
            })
            if res.status_code == 200:
                st.success("Attendance updated")
            else:
                st.error("Attendance record not found")

    with col4:
        st.subheader("Delete Attendance")
        del_att_id = st.number_input("Attendance ID to delete", min_value=1, step=1, key="del_att_id")

        if st.button("Delete Attendance"):
            res = requests.delete(f"{BASE_URL}/attendance/{del_att_id}")
            if res.status_code == 200:
                st.success("Attendance record deleted")
            else:
                st.error("Attendance record not found")