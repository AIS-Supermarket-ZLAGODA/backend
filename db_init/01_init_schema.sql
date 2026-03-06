CREATE TABLE IF NOT EXISTS test_table (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR(255)
);

CREATE TABLE Category (
    category_number SERIAL PRIMARY KEY,
    category_name VARCHAR(50) NOT NULL
);

CREATE TABLE Product (
    id_product SERIAL PRIMARY KEY,
    category_number INT NOT NULL,
    product_name VARCHAR(50) NOT NULL,
    characteristics VARCHAR(100) NOT NULL,
    FOREIGN KEY (category_number) REFERENCES Category(category_number)
        ON UPDATE CASCADE
        ON DELETE NO ACTION
);

CREATE TABLE Store_Product (
    UPC VARCHAR(12) PRIMARY KEY,
    UPC_prom VARCHAR(12),
    id_product INT NOT NULL,
    selling_price DECIMAL(13,4) NOT NULL,
    products_number INT NOT NULL,
    promotional_product BOOLEAN NOT NULL,
    FOREIGN KEY (UPC_prom) REFERENCES Store_Product(UPC)
        ON UPDATE CASCADE
        ON DELETE SET NULL,
    FOREIGN KEY (id_product) REFERENCES Product(id_product)
        ON UPDATE CASCADE
        ON DELETE NO ACTION
);

CREATE TABLE Employee (
    id_employee VARCHAR(10) PRIMARY KEY,
    empl_surname VARCHAR(50) NOT NULL,
    empl_name VARCHAR(50) NOT NULL,
    empl_patronymic VARCHAR(50),
    empl_role VARCHAR(10) NOT NULL,
    salary DECIMAL(13,4) NOT NULL,
    date_of_birth DATE NOT NULL,
    date_of_start DATE NOT NULL,
    phone_number VARCHAR(13) NOT NULL UNIQUE,
    city VARCHAR(50) NOT NULL,
    street VARCHAR(50) NOT NULL,
    zip_code VARCHAR(9) NOT NULL,
    password_hash VARCHAR(255) NOT NULL
);

CREATE TABLE Customer_Card (
    card_number VARCHAR(13) PRIMARY KEY,
    cust_surname VARCHAR(50) NOT NULL,
    cust_name VARCHAR(50) NOT NULL,
    cust_patronymic VARCHAR(50),
    phone_number VARCHAR(13) NOT NULL,
    city VARCHAR(50),
    street VARCHAR(50),
    zip_code VARCHAR(9),
    percent INT NOT NULL
);

CREATE TABLE "Check" (
    check_number VARCHAR(10) PRIMARY KEY,
    id_employee VARCHAR(10) NOT NULL,
    card_number VARCHAR(13),
    print_date TIMESTAMP NOT NULL,
    sum_total DECIMAL(13,4) NOT NULL,
    vat DECIMAL(13,4) NOT NULL,
    FOREIGN KEY (id_employee) REFERENCES Employee(id_employee)
        ON UPDATE CASCADE
        ON DELETE NO ACTION,
    FOREIGN KEY (card_number) REFERENCES Customer_Card(card_number)
        ON UPDATE CASCADE
        ON DELETE NO ACTION
);

CREATE TABLE Sale (
    UPC VARCHAR(12) NOT NULL,
    check_number VARCHAR(10) NOT NULL,
    product_number INT NOT NULL,
    selling_price DECIMAL(13,4) NOT NULL,
    PRIMARY KEY (UPC, check_number),
    FOREIGN KEY (UPC) REFERENCES Store_Product(UPC)
        ON UPDATE CASCADE
        ON DELETE NO ACTION,
    FOREIGN KEY (check_number) REFERENCES "Check"(check_number)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);