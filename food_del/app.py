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
    
# Initialize connection.
# Uses st.cache to only run once.
@st.cache(allow_output_mutation=True, hash_funcs={"_thread.RLock": lambda _: None})
def init_connection():
    return psycopg2.connect(**st.secrets["postgres"])

conn = init_connection()

# Perform query.
# Uses st.cache to only rerun when the query changes or after 10 min.
@st.cache(ttl=600)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()

rows = run_query("SELECT * from site;")

# Print results.
for row in rows:
    st.write(f"{row[0]}")
