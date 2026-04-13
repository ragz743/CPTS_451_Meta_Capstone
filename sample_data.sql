INSERT INTO Customers (Customer_ID, FirstName, LastName, PhoneNum, Email) VALUES
(1, 'John', 'Smith', '2065551111', 'john.smith@email.com');

INSERT INTO Customers (Customer_ID, FirstName, LastName, PhoneNum, Email) VALUES
(2, 'Emily', 'Johnson', '2065552222', 'emily.j@email.com');

INSERT INTO Customers (Customer_ID, FirstName, LastName, PhoneNum, Email) VALUES
(3, 'Michael', 'Brown', '2065553333', 'michael.b@email.com');

INSERT INTO Customers (Customer_ID, FirstName, LastName, PhoneNum, Email) VALUES
(4, 'Sarah', 'Davis', '2065554444', 'sarah.d@email.com');

INSERT INTO Customers (Customer_ID, FirstName, LastName, PhoneNum, Email) VALUES
(5, 'David', 'Wilson', '2065555555', 'david.w@email.com');


INSERT INTO Restaurant_Tables (Table_ID, TableNum, Capacity, IsEmpty) VALUES
(1, 1, 2, 1);

INSERT INTO Restaurant_Tables (Table_ID, TableNum, Capacity, IsEmpty) VALUES
(2, 2, 4, 1);

INSERT INTO Restaurant_Tables (Table_ID, TableNum, Capacity, IsEmpty) VALUES
(3, 3, 4, 0);

INSERT INTO Restaurant_Tables (Table_ID, TableNum, Capacity, IsEmpty) VALUES
(4, 4, 6, 1);

INSERT INTO Restaurant_Tables (Table_ID, TableNum, Capacity, IsEmpty) VALUES
(5, 5, 8, 0);


INSERT INTO Menu_Items (MenuItem_ID, ItemName, Price, Category, Is_Available) VALUES
(1, 'Cheeseburger', 12.99, 'Main', 1);

INSERT INTO Menu_Items (MenuItem_ID, ItemName, Price, Category, Is_Available) VALUES
(2, 'Caesar Salad', 9.99, 'Appetizer', 1);

INSERT INTO Menu_Items (MenuItem_ID, ItemName, Price, Category, Is_Available) VALUES
(3, 'Grilled Salmon', 18.50, 'Main', 1);

INSERT INTO Menu_Items (MenuItem_ID, ItemName, Price, Category, Is_Available) VALUES
(4, 'French Fries', 4.50, 'Side', 1);

INSERT INTO Menu_Items (MenuItem_ID, ItemName, Price, Category, Is_Available) VALUES
(5, 'Chocolate Cake', 6.75, 'Dessert', 1);


INSERT INTO Reservations (Res_ID, Customer_ID, Table_ID, Start_Time, End_Time, Party_Size, Status) VALUES
(1, 1, 2, TIMESTAMP '2026-03-20 18:00:00', TIMESTAMP '2026-03-20 19:30:00', 3, 'booked');

INSERT INTO Reservations (Res_ID, Customer_ID, Table_ID, Start_Time, End_Time, Party_Size, Status) VALUES
(2, 2, 4, TIMESTAMP '2026-03-20 19:00:00', TIMESTAMP '2026-03-20 21:00:00', 5, 'booked');

INSERT INTO Reservations (Res_ID, Customer_ID, Table_ID, Start_Time, End_Time, Party_Size, Status) VALUES
(3, 3, 1, TIMESTAMP '2026-03-21 17:30:00', TIMESTAMP '2026-03-21 18:30:00', 2, 'completed');

INSERT INTO Reservations (Res_ID, Customer_ID, Table_ID, Start_Time, End_Time, Party_Size, Status) VALUES
(4, 4, 3, TIMESTAMP '2026-03-22 18:00:00', TIMESTAMP '2026-03-22 20:00:00', 4, 'cancelled');


INSERT INTO Orders (Order_ID, Customer_ID, Order_Date, TotalAmount, Status) VALUES
(1, 1, TIMESTAMP '2026-03-20 18:10:00', 21.99, 'open');

INSERT INTO Orders (Order_ID, Customer_ID, Order_Date, TotalAmount, Status) VALUES
(2, 2, TIMESTAMP '2026-03-20 19:15:00', 37.00, 'paid');

INSERT INTO Orders (Order_ID, Customer_ID, Order_Date, TotalAmount, Status) VALUES
(3, 3, TIMESTAMP '2026-03-21 17:40:00', 18.50, 'paid');


INSERT INTO Order_Items (Order_Item_ID, Order_ID, MenuItem_ID, Quantity, Item_Price) VALUES
(1, 1, 1, 1, 12.99);

INSERT INTO Order_Items (Order_Item_ID, Order_ID, MenuItem_ID, Quantity, Item_Price) VALUES
(2, 1, 4, 2, 4.50);

INSERT INTO Order_Items (Order_Item_ID, Order_ID, MenuItem_ID, Quantity, Item_Price) VALUES
(3, 2, 3, 2, 18.50);

INSERT INTO Order_Items (Order_Item_ID, Order_ID, MenuItem_ID, Quantity, Item_Price) VALUES
(4, 3, 3, 1, 18.50);


INSERT INTO Payments (Payment_ID, Order_ID, PaymentMethod, TaxAmount, TotalPaid, PaymentDate) VALUES
(1, 2, 'Credit Card', 3.00, 40.00, TIMESTAMP '2026-03-20 19:30:00');

INSERT INTO Payments (Payment_ID, Order_ID, PaymentMethod, TaxAmount, TotalPaid, PaymentDate) VALUES
(2, 3, 'Cash', 1.50, 20.00, TIMESTAMP '2026-03-21 18:00:00');

COMMIT;