import streamlit as st
import requests

st.title("Book App")
action = st.sidebar.selectbox("Action", ["Create", "Update", "Delete"])
url = "http://127.0.0.1:8000"

if action == "Create":
    title = st.text_input("Title")
    author = st.text_input("Author")
    if st.button("Submit"):
        requests.post(f"{url}/Books/", json={"title": title, "author": author})
        st.write("Done")

elif action == "Update":
    id = st.number_input("ID", step=1)
    title = st.text_input("New Title")
    author = st.text_input("New Author")
    if st.button("Submit"):
        requests.put(f"{url}/Book/{id}", json={"title": title, "author": author})
        st.write("Done")

elif action == "Delete":
    id = st.number_input("ID", step=1)
    if st.button("Delete"):
        requests.delete(f"{url}/Book/{id}")
        st.write("Done")