"""
example of k for all the bellow code:

k = ('MT001',      # k[0] - meter number
     '2023-12-01', # k[1] - bill date
     1500,         # k[2] - current units
     1200,         # k[3] - previous units
     300,          # k[4] - units consumed
     1800,         # k[5] - bill amount
     '2023-12-15', # k[6] - due date
     'No')         # k[7] - paid status


"""
# Connects to a MySQL database with the specified host, user, password, and database name. The connection is stored in the global variable `db1` for use throughout the application.
import mysql.connector
db1 = None # create a  global variable to store the database connection
def connect(): # function to connect to the database
    global db1 #declare the global variable db1
    db1 = mysql.connector.connect(host="localhost",user="root",
    password="root",
    database = "electricity"
  )
  

def showusers(): # function to display the list of users
    c1 = db1.cursor() # create a cursor object to interact with the database
    c1.execute("select * from users") # execute a query to fetch all rows from the users table
    res = c1.fetchall() # fetch all rows from the result set and sstore it in the res variable

    # ex = res = [('admin', 'admin123'), ('user1', 'pass123')]

    #print(res)
    print("List of Users ")
    for val in res:
        print("UserName = "+val[0] + " Password = " + val[1])

def login():
    print("-" * 50)  # Prints a line of 50 dashes for formatting
    print("\t Electricity Bill Generation System")  # Prints title with tab indent
    print("-" * 50)  # Another separator line
    print("\t LOGIN")  # Login header with tab indent
    
    un = input("Enter User Name : ")  # Gets username from user
    pw = input("Enter Password : ")  # Gets password from user
    
    # SQL query with placeholders (%s) for safe parameter insertion
    q = "select * from users where username = %s and passw = %s"
    val = (un,pw)  # Tuple of values to insert into query
    
    c2 = db1.cursor()  # Creates database cursor
    c2.execute(q,val)  # Executes query with username and password

    #in c2.execute(q,val) the %s is a place holder for the values in val
    #so q will look like this: "select * from users where username = 'admin' and passw = 'pass123'"

    res = c2.fetchall()  # Gets all matching results
    
    print("-" * 50)  # Separator line
    
    if len(res) == 0:  # If no matching user found
        print("Invalid User Name or Password ")
        print("-" * 50)
        return False  # Login failed
    else:  # If user found
        print("Access Granted !!!")
        print("-" * 50)
        return True  # Login successful


    
def delcustomer():
    print("*" * 50)  # Prints 50 asterisks for formatting
    print("\tDELETING A CUSTOMER")
    print("*" * 50)
    
    cid = input("Enter Customer Id : ")  # Gets customer ID to delete
    cursor1 = db1.cursor()
    q = "delete from customer where cid='" + cid + "'"  # SQL delete query
    cursor1.execute(q)
    db1.commit()  # Saves changes to database
    print("Customer Deleted Successfully")

def addcustomer():
  print("*" * 50)
  print("\tWelcome to Electricity Management")
  print("*" * 50)

  # Get customer details from user
  cid = input("Enter Customer Id : ")
  cname = input("Enter Customer Name : ")
  addr = input("Enter Address : ")
  phone = input("Enter Phone Number : ")
  email = input("Enter Email :")
  mtr = input("Enter meter no : ")
  cursor1 = db1.cursor()
  q = "insert into customer values (%s,%s,%s,%s,%s,%s)" # SQL insert query with placeholders
  val = (cid,cname,addr,phone,email,mtr) # Tuple of values to insert
  cursor1.execute(q,val) # q has %s as placeholders so the valuses in val will be replaced in the place od %s
  db1.commit() # Saves changes to database
  print("Customer Added Successfully")


def showcustomers():
    cursor1 = db1.cursor()  # Creates database cursor
    cursor1.execute("Select * from Customer")  # Gets all customer records
    res = cursor1.fetchall()  # Stores results in res

    """
    example res:

    res = [
    ('C101', 'John Smith', '123 Main St', 'john@email.com', '9876543210', 'MT001'),
    ('C102', 'Mary Jones', '456 Oak Ave', 'mary@email.com', '8765432109', 'MT002'),
    ('C103', 'Bob Wilson', '789 Pine Rd', 'bob@email.com', '7654321098', 'MT003')
    ]

    """
    
    # Prints formatted header
    print("-" * 50)
    print("          CUSTOMER DETAILS ")
    print("-" * 50)
    print("Id   Name     Email     Phone    Meter")
    
    # Prints each customer's details
    for k in res:
        print(k[0],"  ",k[1],"  ",k[3],"  ",k[4],"\t",k[5])

        """
        example output of above code:
            --------------------------------------------------
            CUSTOMER DETAILS 
            --------------------------------------------------
            Id   Name     Email     Phone    Meter
            C101  John Smith  john@email.com  9876543210  MT001
            C102  Mary Jones  mary@email.com  8765432109  MT002
        """

def generatebill():
    # collecting billing info.
    mtr = input("Enter Meter No .: ")
    dt = input("Enter the date of Bill Generation : ")
    cunits = int(input("Enter Current Units on Meter : "))
    punits = int(input("Enter Previous Units of Meter : "))

    #calculate unit consumed
    consumed = cunits - punits

    #calculate bill ammount
    if consumed < 200:
        bill = 4 * consumed
    elif consumed <400:
        bill = 6 * consumed
    else:
        bill = 8 * consumed

    #display consumption and bill ammount    
    print("Total Units Consumed ",consumed)
    print("Total Amount to be paid ",bill)

    duedt = input("Enter the Due Date of Payment : ")

    # Prepare and execute database insert
    q = "insert into bill values(%s,%s,%s,%s,%s,%s,%s,'No')"
    val =(mtr,dt,cunits,punits,consumed,bill,duedt)
    c2 = db1.cursor()
    c2.execute(q,val)
    print("Bill Generated Successfully !!!")
    db1.commit()
    
def showunpaid():
    cursor1 = db1.cursor()  # Create database cursor
    cursor1.execute("Select * from bill where paid='No'")  # Get all unpaid bills
    res = cursor1.fetchall()  # Store results in res
    
    # Print formatted header
    print("   LIST OF UNPAID BILLS   ")
    print("-" * 40)
    print("MeterNo.  BillDate   Amount")
    
    # Print each unpaid bill's details
    for k in res:
        print(k[0],"\t",k[1],"\t",k[5])

        """
        example output of above code:
            LIST OF UNPAID BILLS
            ----------------------------------------
            MeterNo.  BillDate   Amount
            MT001     2023-04-01  200
            MT002     2023-04-02  300
            MT003     2023-04-03  400
        """

def paybill():
    mtr = input("Enter Meter No.: ")
    cursor1 = db1.cursor()

    # Fetch unpaid bills for the given meter number
    query = "SELECT * FROM bill WHERE paid = 'No' AND meterno = %s"
    cursor1.execute(query, (mtr,))
    res = cursor1.fetchall()

    if not res:
        print("No unpaid bills found for the given meter number.")
        return

    print("Following Bills are unpaid for the given meter no ")
    print("-" * 40)
    print("MeterNo.  BillDate   Amount   DueDate")
    for k in res:
        print(k[0],"\t",k[1],"\t",k[5],"\t",k[6])

    bdate = input("Enter the bill date for the bill to be paid : ")
    
    # Update bill status using parameterized query
    update_query = "UPDATE bill SET paid='Yes' WHERE billdate = %s AND meterno = %s"
    cursor1.execute(update_query, (bdate, mtr))
    db1.commit()

    mp = input("Please Select the mode of Payment(Cash/Cheque/Card): ")
    print("Transaction Complete !!!")
    
connect()  # Establishes database connection
print("Connected")

if login():  # Only proceeds if login is successful
    while True:  # Continuous loop for menu
        # Display menu header
        print("-" * 50)
        print("\t CHOOSE AN OPERATION ")
        print("-" * 50)
        
        # Menu options
        print("Press 1 - Add a New Customer")
        print("Press 2 - Delete an Existing Customer")
        print("Press 3 - Show all Customers")
        print("Press 4 - Generate the Bill")
        print("Press 5 - Mark the Bill as Paid")
        print("Press 6 - Show All Unpaid Bills")
        print("Press 7 - Quit")
        
        # Get user choice
        ch = int(input("Enter Your Choice : "))
        
        # Execute corresponding function based on choice
        if ch == 1:
            addcustomer()
        elif ch == 2:
            delcustomer()
        elif ch == 3:
            showcustomers()
        elif ch == 4:
            generatebill()
        elif ch == 5:
            paybill()
        elif ch == 6:
            showunpaid()
        elif ch == 7:
            break  # Exit the program
