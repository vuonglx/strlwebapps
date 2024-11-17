import re
import streamlit as st
import csv  # pip install requests


def is_valid_email(email):
    # Basic regex pattern for email validation
    email_pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(email_pattern, email) is not None


def contact_form():
    with st.form("contact_form"):
        name = st.text_input("First Name")
        email = st.text_input("Email Address")
        message = st.text_area("Your Message")
        submit_button = st.form_submit_button("Submit")

        if submit_button:
            if not name:
                st.error("Please provide your name.", icon="🧑")
                st.stop()

            if not email:
                st.error("Please provide your email address.", icon="📨")
                st.stop()

            if not is_valid_email(email):
                st.error("Please provide a valid email address.", icon="📧")
                st.stop()

            if not message:
                st.error("Please provide a message.", icon="💬")
                st.stop()

            # Save the data to a CSV file
            data = {"email": email, "name": name, "message": message}
            with open("contacts.csv", mode="a", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=["email", "name", "message"])
                writer.writerow(data)

            st.success("Your message has been saved successfully! 🎉", icon="🚀")
