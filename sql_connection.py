from dotenv import load_dotenv
import mysql.connector
import os
import streamlit as st
def mysql_connect():
    load_dotenv()
    pwd = os.getenv("SQL_PASSWORD")
    if 'db_state' not in st.session_state:
        st.session_state.db_state = mysql.connector.connect(
            host = "localhost",
            user = "root",
            passwd = pwd,
            database = "testdatabase"
        )
        st.session_state.mycursor_state = st.session_state.db_state.cursor()