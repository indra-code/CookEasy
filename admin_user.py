import streamlit as st
import pandas as pd
from sql_connection import mysql_connect

def callback():
    mycursor = st.session_state.mycursor_state
    db = st.session_state.db_state
    edited_rows = st.session_state["data_editor"]["edited_rows"]
    print(edited_rows.items())
    rows_to_delete = []
    for idx, value in edited_rows.items():
        if value["Delete User"] is True:
            id = st.session_state["data"].iloc[idx]["User id"]
            print(int(id))
            mycursor.execute(f"DELETE FROM regular_users WHERE user_id = %s",(int(id),))
            db.commit()
            rows_to_delete.append(idx)

    st.session_state["data"] = (
        st.session_state["data"].drop(rows_to_delete, axis=0).reset_index(drop=True)
    )

def admin_user():
    if 'db_state' not in st.session_state or 'mycursor_state' not in st.session_state:
        mysql_connect()
    mycursor = st.session_state.mycursor_state
    db = st.session_state.db_state
    if "data" not in st.session_state:
        mycursor.execute("SELECT user_id, username FROM regular_users")
        r = mycursor.fetchall()
        users = [user for user in r]
        st.session_state.data = pd.DataFrame(
            data=users,
            columns=["User id", "Username"]
        )

    if 'userid_delete' not in st.session_state:
        st.session_state.userid_delete = None 

    columns = st.session_state["data"].columns
    column_config = {column: st.column_config.Column(disabled=True) for column in columns}

    modified_df = st.session_state["data"].copy()
    modified_df["Delete User"] = False 
    modified_df = modified_df[modified_df.columns.tolist()]
    with st.sidebar:
        if st.button("Logout"):
            st.session_state.page='app'
            st.session_state.loginbtns = True
            st.rerun()
    st.header("Admin Dashboard")
    st.subheader("Users Table")
    st.data_editor(
        modified_df,
        key="data_editor",
        on_change=callback,
        hide_index=True,
        column_config=column_config,
        width=500    
        )

if __name__ == "__main__":
    admin_user()
