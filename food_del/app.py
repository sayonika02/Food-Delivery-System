import streamlit as st
import pandas as pd
import random

# DB Management
import psycopg2

conn = psycopg2.connect(
    database="food_delivery",
    user="postgres",
    password="4647",
    host="localhost",
    port="5432"
)
c = conn.cursor()
# DB  Functions

# ADMIN
def create_admintable():
    	c.execute('CREATE TABLE IF NOT EXISTS admins(user_name TEXT,password TEXT, email TEXT)')


def add_admindata(username,password,email):
	c.execute('INSERT INTO admins(user_name,password,email) VALUES (%s,%s,%s)',(username,password,email))
	conn.commit()

def login_admin(username,password):
	c.execute('SELECT * FROM admins WHERE user_name =%s AND password = %s',(username,password))
	data = c.fetchall()
	return data

# USER
def create_usertable():
	c.execute('CREATE TABLE IF NOT EXISTS users(username TEXT,password TEXT)')


def add_userdata(username,password,email,address,contact):
	c.execute('INSERT INTO users(user_name,password,email,address,contact_number) VALUES (%s,%s,%s,%s,%s)',(username,password,email,address,contact))
	conn.commit()

def login_user(username,password):
	c.execute('SELECT * FROM users WHERE user_name =%s AND password = %s',(username,password))
	data = c.fetchall()
	return data

def view_user(username, password):
	c.execute('SELECT user_id, user_name, email, address, contact_number FROM users where user_name=%s AND password = %s',(username,password))
	data = c.fetchall()
	return data


def display_site():
    c.execute('SELECT * FROM restaurant')
    data = c.fetchall()
    return data


def add_reviewdata(restaurants, usernames, ratings, feedbacks):
    c.execute('SELECT restaurant_id FROM restaurant WHERE restaurant_name LIKE \'{}\''.format(restaurants))
    rid = c.fetchone()
    c.execute('INSERT INTO review(name, rating, feedback, rest_id) VALUES (\'{0}\',{1},\'{2}\',{3})'.format(usernames, ratings, feedbacks, rid[0]))
    conn.commit()   

def display_review():
    c.execute('SELECT restaurant_name, name, rating, feedback FROM restaurant, review WHERE restaurant.restaurant_id=review.rest_id GROUP BY restaurant.restaurant_name, name, rating, feedback ORDER BY restaurant_name')
    data = c.fetchall()
    return data

def view_menu(res_id):
    c.execute('SELECT * FROM menu WHERE menu.res_id={}'.format(res_id))
    data = c.fetchall()
    return data  

def insert_record(item, table_name):
    # INSERT USING SCHEMA
    c.execute('INSERT INTO {} VALUES {}'.format(table_name, item))
    conn.commit()

#TABLES

def display_table(table_name):
    c.execute('SELECT * FROM {0}'.format(table_name))
    data = c.fetchall()
    return data

def get_table_schema(table_name):
    c.execute('SELECT column_name, data_type FROM information_schema.columns WHERE table_name = \'{0}\''.format(table_name))
    data = c.fetchall()
    return data

def delete_record(table_name, t_id, del_id):
    c.execute('DELETE FROM {} WHERE {} = {}'.format(table_name, t_id, del_id))
    conn.commit()
    return "Record deleted"

# PLACE ORDER
def place_order(item_id, res_id, uname, payment_type):
    c.execute('SELECT price FROM menu where menu.res_id={} AND menu.item_id={}'.format(res_id, item_id))
    amt = c.fetchone()[0]
    c.execute('SELECT user_id FROM users where users.user_name=\'{}\''.format(uname))
    uid = c.fetchone()[0]
    c.execute('SELECT item_name FROM menu where menu.item_id={}'.format(item_id))
    item = c.fetchone()[0]
    c.execute('SELECT CURRENT_DATE')
    o_date = c.fetchone()[0]
    c.execute('SELECT emp_id FROM employee WHERE emp_id not in (SELECT employee_id from orders ) ')
    emp_id = c.fetchone()[0]
    c.execute('INSERT INTO orders("order_date","amount","order_items","user_id","employee_id","item_id") VALUES (\'{0}\',{1},\'{2}\',{3},{4},{5})'.format(o_date, amt, item, uid, emp_id, item_id))
    c.execute('SELECT order_id FROM orders ORDER BY order_id DESC LIMIT 1')
    o_id = c.fetchone()[0]
    c.execute('INSERT INTO payment("amount","sender_name","payment_date","payment_type","order_id") VALUES ({0},\'{1}\',\'{2}\',\'{3}\',{4})'.format(amt, uname, o_date, payment_type, o_id))
    conn.commit()
    return "Order placed successfully."

def main():
    
    st.header("FOOD DELIVERY SYSTEM")
    menu = ["Login", "Signup"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Login":
        st.subheader("Welcome Back!")

        username = st.text_input("User Name")
        password = st.text_input("Password",type='password')
        if st.checkbox("Login"):
        
                if not username.startswith("admin"):
                    create_usertable()

                    result = login_user(username,password)                   
                    if result:
                        st.success("Logged In as {}".format(username))

                        user_menu = ["Profile","Place Order","Write Review"]
                        task = st.sidebar.selectbox("User Menu", user_menu)
                        if task == "Place Order":
                            user_result = display_site()
                            table_schema = [r[0] for r in get_table_schema("restaurant")]
                            clean_db = pd.DataFrame(user_result, columns = table_schema)
                            st.dataframe(clean_db)
                            res_id = st.number_input("Enter Restaurant ID", min_value=1, max_value=1000, step=1)
                            if st.button("View Menu"):
                                res_menu = view_menu(res_id)
                                clean_db = pd.DataFrame(res_menu, columns = ["item_name","price","description","availability_status","res_id","item_id"])
                                st.dataframe(clean_db)

                                #take order
                            item_id = st.number_input("Enter item ID", min_value=1, max_value=1000, step=1)
                            payment_type = st.selectbox("Choose payment option", ["UPI","Cash on Delivery","Card"])
                            if st.button("Place Order!"):
                                order_status = place_order(item_id, res_id, username, payment_type)
                                st.header(order_status)


                        elif task == "Write Review":
                            user_reviews = display_review()
                            rev_db = pd.DataFrame(user_reviews, columns = ["restaurant_name", "name", "rating", "feedback"])
                            st.dataframe(rev_db)
                            st.subheader("Write your own Review")
                            restaurant = st.text_input("Restaurant Name")
                            rating = st.slider("Rating",0,10)
                            feedback = st.text_input("Feedback")
                            if st.button("Publish Review"):
                                add_reviewdata(restaurant, username, rating, feedback)
                            st.success("You have successfully reviewed {}".format(restaurant))


                        elif task == "Profile":
                            st.subheader("User Profile")
                            user_result = view_user(username, password)
                            clean_db = pd.DataFrame(user_result,columns=["user_id","user_name","email","address","contact_number"])
                            st.dataframe(clean_db)
                    
                    else:
                        st.warning("Incorrect Username/Password")                       

                elif username.startswith("admin"):
                    # manage and view all tables
                    create_admintable()
                    result = login_admin(username,password)
                    if result:

                        st.success("Logged In as {}".format(username))

                        admin_menu = ["users","restaurant","review", "menu", "employee", "orders", "payment"]
                        task = st.sidebar.selectbox("View Tables", admin_menu)
                        table_result = display_table(task)
                        table_schema = [r[0] for r in get_table_schema(task)]
                        clean_db = pd.DataFrame(table_result, columns = table_schema)
                        st.dataframe(clean_db)

                        del_id = st.number_input("Enter ID of the record to be deleted", min_value=1, max_value=1000, step=1)
                        if st.button("Delete"):
                            s = delete_record(task, table_schema[0], del_id)
                            st.header(s)

                        admin_insert_menu = ["restaurant", "menu","employee"]
                        itask = st.sidebar.selectbox("Insert into Tables", admin_insert_menu)
                        table_schema = [r for r in get_table_schema(itask)]
                        i = list()
                        for r in range(len(table_schema)-1):
                            if table_schema[r][1]=='integer':
                                i.append(st.number_input("Enter {}".format(table_schema[r][0]),min_value=1, max_value=1000, step=1))
                            else:
                                i.append(st.text_input("Enter {}".format(table_schema[r][0])))

                        if st.button("Insert"):
                            # PASS SCHEMA IN CORRECT FORMAT
                            insert_record(tuple(i), itask)

                    else:
                        st.warning("Incorrect Username/Password")

    elif choice == "Signup":
        st.title('Signup')
        st.subheader("Create New Account")
        new_user = st.text_input("Username")
        new_password = st.text_input("Password",type='password')
        email = st.text_input("Email")

        if not new_user.startswith("admin"):
            address = st.text_input("Address")
            contact = st.text_input("Contact No")
            if st.button("Signup"):
    
                create_usertable()
                add_userdata(new_user,new_password, email, address, contact)
                st.success("You have successfully created a valid Account")
                st.info("Go to Login Menu to login")
        else:
            if st.button("Signup"):

                create_admintable()
                add_admindata(new_user,new_password, email)
                st.success("You have successfully created a valid Account")
                st.info("Go to Login Menu to login")               

if __name__ == '__main__':
    main()