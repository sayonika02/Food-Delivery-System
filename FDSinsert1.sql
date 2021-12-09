\c food_delivery

INSERT INTO restaurant (restaurant_name, cuisine, address)
VALUES
('KFC', 'American', '385 Terry Lane'),
('Dominos', 'Italian', '453 Ring Road '),
('Taco Bell', 'Mexican', '657 Ashoka Road'),
('McDonalds', 'Fast Food', '456 Terry Lane'),
('Dosa Corner','Indian', '887 Holt Lane');


INSERT INTO review ( rating, feedback, name, rest_id)
VALUES (4, 'I was pleasantly surprised', 'Nelly', 5),
(6, 'Poor Quality Bread', 'Rena', 2);


INSERT INTO menu
( item_name, price, description, availability_status, res_id)
VALUES ('Chicken Lollipops',350,'frenched chicken winglet','Yes',1),
('Pesto Pasta', 240, 'creamy green sauce and pasta', 'Yes', 2),
('Veg Burger', 150, 'Arrabiata sauce and any pasta', 'Yes', 4),
('Manchurian', 120, 'mushroom/gobi', 'Yes', 3),
('Taco', 100, 'taco with cheese toppings', 'Yes', 3),
('Meatballs', 155, 'with sauce', 'Yes', 1),
('Non veg Burger', 210, 'chicken patty', 'Yes', 4),
('Pizza', 250, 'thin crust 10 inch', 'Yes', 2),
('Masala Dosa', 50, 'dosa with chutney and potato curry', 'Yes', 5),
('Upma', 40, 'vegetable upma served with chutney', 'Yes', 5),
('Idli', 40, 'idli served with chutney and sambar', 'Yes', 5);


INSERT INTO employee(emp_name, contact_no, email_addr)
VALUES 
('Nirmala','2225812373','nirmala.al@gmail.com'),
('shambhavi','6625812374','shambhavi@gmail.com'),
('divya','5525812373','divya@gmail.com'),
('sheetal','9825812373','sheet@gmail.com'),
('sejal','9900123731','sej@gmail.com'),
('priya','7775812373','priya@gmail.com'),
('nirma','2552812373','nirma@gmail.com'),
('mala','2221852373','mala@gmail.com'),
('satwik','2227812373','satwok@gmail.com'),
('Elliot','8441473477','elliotcoke@gmail.com');

INSERT INTO users(user_name, password, contact_number, email, address)
VALUES 
('user1','user1','2225812373','u1@gmail.com', 'home1 blr'),
('user2','user2','8441473477','u2@gmail.com', 'home2 blr');
