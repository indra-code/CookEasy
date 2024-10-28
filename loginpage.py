import streamlit as st
from sql_connection import mysql_connect
from regular_user import regular_user
def login():
    if 'db_state' not in st.session_state or 'mycursor_state' not in st.session_state:
        mysql_connect()
    db =st.session_state.db_state
    mycursor = st.session_state.mycursor_state
    if st.session_state.page=='login':
        mysql_connect()
        st.header('Login')
        st.text_input(label='Username',placeholder="Enter username")
        st.text_input(label='Password',placeholder="Enter password",type="password")
        if st.button("Login"):
            st.session_state.page='regular_user'
            st.rerun()
    if st.session_state.page=='regular_user':
        regular_user()
if __name__=='__main__':
    login()
