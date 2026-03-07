INSERT INTO Category (category_name) VALUES
('Молочні продукти'),
('Хлібобулочні вироби'),
('М''ясо та птиця');

INSERT INTO Product (category_number, product_name, producer, characteristics) VALUES
(1, 'Молоко 2.5%', 'Галичина', 'Пляшка 1л, пастеризоване'),
(2, 'Хліб білий', 'Куліничі', 'Нарізний, 500г, вищий гатунок'),
(3, 'Куряче філе', 'Наша Ряба', 'Охолоджене, фасоване по 1кг');

INSERT INTO Store_Product (UPC, UPC_prom, id_product, selling_price, products_number, promotional_product) VALUES
('123456789012', NULL, 1, 35.50, 50, FALSE),
('123456789013', NULL, 2, 24.00, 30, FALSE),
('123456789014', NULL, 3, 160.00, 15, FALSE),
('123456789015', '123456789012', 1, 28.40, 10, TRUE);

INSERT INTO Employee (id_employee, empl_surname, empl_name, empl_patronymic, empl_role, salary, date_of_birth, date_of_start, phone_number, city, street, zip_code, password_hash) VALUES
('EMP0000001', 'Шевченко', 'Олександр', 'Іванович', 'Касир', 15000.00, '1995-05-15', '2023-01-10', '+380501234567', 'Дніпро', 'вул. Центральна, 1', '49000', '$argon2id$v=19$m=65536,t=3,p=4$l5zMiQZAJyTEkBvLRG0Gaw$gVeOmzoGn4H7D88/zXyla+8nE+HJSE4q7duQTbGEGAs'),
('EMP0000002', 'Коваленко', 'Марія', 'Петрівна', 'Менеджер', 25000.00, '1985-08-22', '2020-11-01', '+380671234567', 'Дніпро', 'пр. Науки, 10', '49005', '$argon2id$v=19$m=65536,t=3,p=4$EY3tqqtXkIHpzkY0fjOPug$EemqS/Q5Qji/tG0rscJVIsU3eJT/RxrOEAePr1DR8ak');

INSERT INTO Customer_Card (card_number, cust_surname, cust_name, cust_patronymic, phone_number, city, street, zip_code, percent) VALUES
('CARD000000001', 'Іваненко', 'Іван', 'Сергійович', '+380631112233', 'Дніпро', 'вул. Робоча, 55', '49008', 5),
('CARD000000002', 'Петренко', 'Анна', 'Вікторівна', '+380991112233', 'Дніпро', 'вул. Титова, 12', '49006', 10);

INSERT INTO "Check" (check_number, id_employee, card_number, print_date, sum_total, vat) VALUES
('CHK0000001', 'EMP0000001', 'CARD000000001', '2026-03-04 10:15:00', 59.50, 11.90),
('CHK0000002', 'EMP0000001', NULL, '2026-03-04 11:30:00', 160.00, 32.00);

INSERT INTO Sale (UPC, check_number, product_number, selling_price) VALUES
('123456789012', 'CHK0000001', 1, 35.50),
('123456789013', 'CHK0000001', 1, 24.00),
('123456789014', 'CHK0000002', 1, 160.00);