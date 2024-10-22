import streamlit as st
from regular_user import regular_user
from admin_user import admin_user
def main():
    if 'page' not in st.session_state:
        st.session_state.page = None
    if 'loginbtns' not in st.session_state:
        st.session_state.loginbtns = True
    col1,col2 = st.columns(2)
    if st.session_state.loginbtns:
        with col1:
            if st.button('User Login'):
                st.session_state.page = 'regular_user'
                st.session_state.loginbtns = False
                st.rerun()
        with col2:
            if st.button('Admin Login'):
                st.session_state.page = 'admin_user'
                st.session_state.loginbtns = False
                st.rerun()

    if st.session_state.page == 'regular_user':
        regular_user()
    elif st.session_state.page == 'admin_user':
        admin_user()
if __name__=='__main__':
    main()
