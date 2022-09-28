# candyvan

CandyStreet Inventory Management Web Project

---

# Routes

A.K.A. Pages to be created

## /inventory

Main page for inventory management system.

### /inventory/login

Login Page. People without valid credential info will be redirected to this page when attempting to access other pages.

### /inventory/sell

A.k.a. Employee page. Employees will be able to view current stock and sell them.

### /inventory/admin

A.k.a. Employer page. Admins will be able to manage the site in the following subpages.

#### /inventory/admin/account

Account management page where admin will be able to add employees. Moreover, Superuser will be able to create another admin accounts as well.

#### /inventory/admin/stock

Stock management page. Admins will be able to add or set a new item and its prices or quantity. Financial controls will also be available.

#### /inventory/admin/revenue

TODO: Decide if this should be merged into /stock

Page with a table to show revenue per days.

#### /inventory/admin/log

Page intended to show all currently logged actions taken.

---

# Models

SQL models to be used.

## User

| Column Name | Description | Type |
|        ---: | :---        | :--- |
| id | Unique ID | int |
| username | Username used to log in or audit | str(30) |
| password | Hashed password info | str(?) |
| type | User Type. 99: Superuser, 0: Admin, 1: Employee | int |

## Item

| Column Name | Description | Type |
|        ---: | :---        | :--- |
| id | Unique ID | int |
| name | Name of the item | str(30) |
| buy_price | Price when purchased to stock | int |
| sell_price | Price when sold to customers | int |
| quantity | Current quantity available in stock | int |

## Sale

Note: Separate Sales log must be created per item in cases where multiple items are sold in a single sale.

| Column Name | Description | Type |
|        ---: | :---        | :--- |
| id | Unique ID | int |
| time | Time the sale was made | datetime |
| user_id | Seller who made the sale | int |
| item_id | Item that was sold. | int |
| parent_entry | Reference to previous entry if multiple sale entries were made | int |
| quantity | Quantity of the sold item | int |

## Transaction

| Column Name | Description | Type |
|        ---: | :---        | :--- |
| id | Unique ID | int |
| time | Time the transaction was made | int |
| user_id | User who triggered the transaction | int |
| sale_id | Sale entry that triggered the transaction, if existing. Null if done manually by admin. | int |
| amount | Amount of money moved. Could be positive/negative | int |

## Revenue

| Column Name | Description | Type |
|        ---: | :---        | :--- |
| id | Unique ID | int |
| date | the date the data is representing | datetime |
| revenue | The amount of profit made in a day | int |

## Log

| Column Name | Description | Type |
|        ---: | :---        | :--- |
| id | Unique ID | int |
| time | The time the action was taken | datetime |
| action | String representing the action taken | text |
