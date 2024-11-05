import streamlit as st
from sql_connection import mysql_connect
from regular_user import regular_user
def login():
    if 'db_state' not in st.session_state or 'mycursor_state' not in st.session_state:
        mysql_connect()
    db =st.session_state.db_state
    mycursor = st.session_state.mycursor_state
    if 'userid' not in st.session_state:
        st.session_state.userid = None
    if st.session_state.page=='login':
        mysql_connect()
        st.header('Login')
        username = st.text_input(label='Username',placeholder="Enter username")
        password = st.text_input(label='Password',placeholder="Enter password",type="password")
        if st.button("Login"):
            mycursor.execute(f'SELECT user_id FROM regular_users WHERE username = %s AND password = %s',(username,password))
            userid = mycursor.fetchone()
            if userid is not None:
                st.session_state.userid = userid
                st.session_state.page='regular_user'
                st.rerun()
            else:
                st.error("Please enter valid credentials")
if __name__=='__main__':
    login()
