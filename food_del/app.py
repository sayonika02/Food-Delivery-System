import streamlit as st
import psycopg2

def main():
    
    menu = ["Login", "Signup"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Login":
        st.title('Login')
        st.subheader("Welcome Back!")
        username = st.text_input("Username")
        password = st.text_input("Password", type = 'password')
        if st.button("Login"):
            st.success("Logged In as {}". format(username))
    elif choice == "Signup":
        st.title('Signup')
        st.subheader("Create New Account")

if __name__ == '__main__':
    main()
