import streamlit as st
from sql_connection import mysql_connect
from admin_user import admin_user
def admin_login():
    if 'db_state' not in st.session_state or 'mycursor_state' not in st.session_state:
        mysql_connect()
    db =st.session_state.db_state
    mycursor = st.session_state.mycursor_state
    if 'adminid' not in st.session_state:
        st.session_state.adminid = None
    if st.session_state.page=='admin_login':
        mysql_connect()
        st.header('Admin Login')
        username = st.text_input(label='Username',placeholder="Enter username")
        password = st.text_input(label='Password',placeholder="Enter password",type="password")
        if st.button("Login"):
            mycursor.execute(f'SELECT admin_id FROM admin_users WHERE username = %s AND password = %s',(username,password))
            adminid = mycursor.fetchone()
            if adminid is not None:
                st.session_state.adminid = adminid
                st.session_state.page='admin_user'
                st.rerun()
            else:
                st.error("Please enter valid credentials")
if __name__=='__main__':
    admin_login()
