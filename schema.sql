-- Drop child tables first if they exist
BEGIN
    EXECUTE IMMEDIATE 'DROP TABLE Payments CASCADE CONSTRAINTS';
EXCEPTION
    WHEN OTHERS THEN
        IF SQLCODE != -942 THEN RAISE; END IF;
END;
/

BEGIN
    EXECUTE IMMEDIATE 'DROP TABLE Order_Items CASCADE CONSTRAINTS';
EXCEPTION
    WHEN OTHERS THEN
        IF SQLCODE != -942 THEN RAISE; END IF;
END;
/

BEGIN
    EXECUTE IMMEDIATE 'DROP TABLE Orders CASCADE CONSTRAINTS';
EXCEPTION
    WHEN OTHERS THEN
        IF SQLCODE != -942 THEN RAISE; END IF;
END;
/

BEGIN
    EXECUTE IMMEDIATE 'DROP TABLE Reservations CASCADE CONSTRAINTS';
EXCEPTION
    WHEN OTHERS THEN
        IF SQLCODE != -942 THEN RAISE; END IF;
END;
/

BEGIN
    EXECUTE IMMEDIATE 'DROP TABLE Menu_Items CASCADE CONSTRAINTS';
EXCEPTION
    WHEN OTHERS THEN
        IF SQLCODE != -942 THEN RAISE; END IF;
END;
/

BEGIN
    EXECUTE IMMEDIATE 'DROP TABLE Restaurant_Tables CASCADE CONSTRAINTS';
EXCEPTION
    WHEN OTHERS THEN
        IF SQLCODE != -942 THEN RAISE; END IF;
END;
/

BEGIN
    EXECUTE IMMEDIATE 'DROP TABLE Customers CASCADE CONSTRAINTS';
EXCEPTION
    WHEN OTHERS THEN
        IF SQLCODE != -942 THEN RAISE; END IF;
END;
/

CREATE TABLE Customers (
    Customer_ID       NUMBER PRIMARY KEY,
    FirstName         VARCHAR2(100) NOT NULL,
    LastName          VARCHAR2(100) NOT NULL,
    PhoneNum          VARCHAR2(20) NOT NULL UNIQUE,
    Email             VARCHAR2(255) UNIQUE,
    TimeCreated_AT    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Restaurant_Tables (
    Table_ID          NUMBER PRIMARY KEY,
    TableNum          NUMBER NOT NULL UNIQUE,
    Capacity          NUMBER NOT NULL,
    IsEmpty           NUMBER(1) DEFAULT 1 NOT NULL,
    CONSTRAINT chk_table_capacity CHECK (Capacity > 0),
    CONSTRAINT chk_table_isempty CHECK (IsEmpty IN (0, 1))
);

CREATE TABLE Menu_Items (
    MenuItem_ID       NUMBER PRIMARY KEY,
    ItemName          VARCHAR2(150) NOT NULL,
    Price             NUMBER(8,2) NOT NULL,
    Category          VARCHAR2(50) NOT NULL,
    Is_Available      NUMBER(1) DEFAULT 1 NOT NULL,
    CONSTRAINT chk_menu_price CHECK (Price >= 0),
    CONSTRAINT chk_menu_available CHECK (Is_Available IN (0, 1))
);

CREATE TABLE Reservations (
    Res_ID            NUMBER PRIMARY KEY,
    Customer_ID       NUMBER NOT NULL,
    Table_ID          NUMBER NOT NULL,
    Start_Time        TIMESTAMP NOT NULL,
    End_Time          TIMESTAMP NOT NULL,
    Party_Size        NUMBER NOT NULL,
    Status            VARCHAR2(20) NOT NULL,
    CONSTRAINT fk_res_customer
        FOREIGN KEY (Customer_ID) REFERENCES Customers(Customer_ID),
    CONSTRAINT fk_res_table
        FOREIGN KEY (Table_ID) REFERENCES Restaurant_Tables(Table_ID),
    CONSTRAINT chk_res_party CHECK (Party_Size > 0),
    CONSTRAINT chk_res_status CHECK (Status IN ('booked', 'completed', 'cancelled')),
    CONSTRAINT chk_res_time CHECK (End_Time > Start_Time),
    CONSTRAINT uq_res_table_start UNIQUE (Table_ID, Start_Time)
);

CREATE TABLE Orders (
    Order_ID          NUMBER PRIMARY KEY,
    Customer_ID       NUMBER NOT NULL,
    Order_Date        TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    TotalAmount       NUMBER(10,2) NOT NULL,
    Status            VARCHAR2(20) NOT NULL,
    CONSTRAINT fk_order_customer
        FOREIGN KEY (Customer_ID) REFERENCES Customers(Customer_ID),
    CONSTRAINT chk_order_total CHECK (TotalAmount >= 0),
    CONSTRAINT chk_order_status CHECK (Status IN ('open', 'paid', 'cancelled'))
);

CREATE TABLE Order_Items (
    Order_Item_ID     NUMBER PRIMARY KEY,
    Order_ID          NUMBER NOT NULL,
    MenuItem_ID       NUMBER NOT NULL,
    Quantity          NUMBER NOT NULL,
    Item_Price        NUMBER(8,2) NOT NULL,
    CONSTRAINT fk_item_order
        FOREIGN KEY (Order_ID) REFERENCES Orders(Order_ID),
    CONSTRAINT fk_item_menu
        FOREIGN KEY (MenuItem_ID) REFERENCES Menu_Items(MenuItem_ID),
    CONSTRAINT chk_item_qty CHECK (Quantity > 0),
    CONSTRAINT chk_item_price CHECK (Item_Price >= 0)
);

CREATE TABLE Payments (
    Payment_ID        NUMBER PRIMARY KEY,
    Order_ID          NUMBER NOT NULL UNIQUE,
    PaymentMethod     VARCHAR2(50) NOT NULL,
    TaxAmount         NUMBER(8,2) NOT NULL,
    TotalPaid         NUMBER(10,2) NOT NULL,
    PaymentDate       TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_payment_order
        FOREIGN KEY (Order_ID) REFERENCES Orders(Order_ID),
    CONSTRAINT chk_payment_tax CHECK (TaxAmount >= 0),
    CONSTRAINT chk_payment_total CHECK (TotalPaid >= 0)
);