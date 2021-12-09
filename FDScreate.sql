drop database food_delivery;
create database food_delivery;

\c food_delivery

CREATE TABLE users( 
user_name VARCHAR,
password VARCHAR,
email VARCHAR,
address VARCHAR,
contact_number VARCHAR(10),
user_id SERIAL PRIMARY KEY
);

CREATE TABLE restaurant(
restaurant_name VARCHAR,
cuisine VARCHAR(30),
address VARCHAR(50),
restaurant_id SERIAL PRIMARY KEY
);

CREATE TABLE review(
review_id SERIAL PRIMARY KEY,
name VARCHAR,
rating INTEGER,
feedback VARCHAR,
rest_id INTEGER,
FOREIGN KEY(rest_id) REFERENCES restaurant(restaurant_id)
);

CREATE TABLE menu(
item_name VARCHAR(30),
price INTEGER,
description VARCHAR(50),
availability_status VARCHAR(5),
res_id INTEGER,
FOREIGN KEY(res_id) REFERENCES restaurant(restaurant_id),
item_id SERIAL PRIMARY KEY
);

CREATE TABLE employee(
emp_name VARCHAR,
contact_no VARCHAR(10),
email_addr VARCHAR,
emp_id SERIAL PRIMARY KEY
);

CREATE TABLE orders(
order_id SERIAL PRIMARY KEY,
order_date DATE,
amount INTEGER,
order_items VARCHAR,
user_id INTEGER,
FOREIGN KEY(user_id) REFERENCES users(user_id),
employee_id INTEGER,
FOREIGN KEY(employee_id) REFERENCES employee(emp_id),
item_id INTEGER,
FOREIGN KEY(item_id) REFERENCES menu(item_id)
);


CREATE TABLE payment(
payment_id SERIAL PRIMARY KEY,
amount INTEGER,
sender_name VARCHAR,
payment_date DATE,
payment_type VARCHAR,
order_id INTEGER,
FOREIGN KEY(order_id) REFERENCES orders(order_id)
);

