import mysql.connector
from flask import Flask, render_template, request

app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Harsha@1234",
    auth_plugin="mysql_native_password",
    database="LibraryManagementSystem",
)
cur = db.cursor()


##Helper Functions##
def get_most_borrowed_books():
    cur.execute(
        """
        SELECT Name, COUNT(*) AS BorrowCount
        FROM Books
        INNER JOIN Loaned ON Books.ID = Loaned.Book_ID
        GROUP BY Name
        ORDER BY BorrowCount DESC
        LIMIT 5;
    """
    )
    most_borrowed_books = cur.fetchall()
    return most_borrowed_books


def get_most_read_authors():

    cur.execute(
        """
        SELECT Writer.Name, COUNT(*) AS ReadCount
        FROM Loaned
        INNER JOIN Books ON Loaned.Book_ID = Books.ID
        INNER JOIN Writer ON Books.Writer_ID = Writer.ID
        GROUP BY Writer.ID
        ORDER BY ReadCount DESC
        LIMIT 5;
    """
    )
    most_read_authors = cur.fetchall()
    return most_read_authors


## Routes
# Function to display menu options
@app.route("/")
def display_index():
    return render_template("index.html")


# Route to display the search form
@app.route("/search", methods=["GET"])
def display_search_form():
    return render_template("search.html")


# Function to search for a book
@app.route("/search", methods=["POST"])
def search_book():
    if request.method == "POST":
        book_name = request.form["search_query"]
        sql = """
            SELECT Books.*, Writer.Name AS Author_Name, Publisher.Name AS Publisher_Name
            FROM Books
            INNER JOIN Writer ON Books.Writer_ID = Writer.ID
            INNER JOIN Publisher ON Books.Publisher_ID = Publisher.ID
            WHERE Books.Name LIKE %s
        """
        val = ("%" + book_name + "%",)
        cur.execute(sql, val)
        results = cur.fetchall()
        if results:
            return render_template("search_result.html", results=results)
        else:
            return render_template("book_not_found.html")


# Route to display the insert form
@app.route("/insert", methods=["GET"])
def display_insert_form():
    return render_template("insert.html")


# Function to insert data into selected table
@app.route("/insert", methods=["POST"])
def insert_data():
    if request.method == "POST":
        table_name = request.form["table_name"]
        if table_name == "Books":
            name = request.form["Name"]
            isbn = request.form["ISBN"]
            writer_id = request.form["Writer_ID"]
            publisher_id = request.form["Publisher_ID"]
            sql = "INSERT INTO Books (Name, ISBN, Writer_ID, Publisher_ID) VALUES (%s, %s, %s, %s)"
            val = (name, isbn, writer_id, publisher_id)
        elif table_name == "Writer":
            name = request.form["Name"]
            gender = request.form["Gender"]
            qualification = request.form["Qualification"]
            sql = "INSERT INTO Writer (Name, Gender, Qualification) VALUES (%s, %s, %s)"
            val = (name, gender, qualification)
        elif table_name == "Publisher":
            name = request.form["Name"]
            city = request.form["City"]
            zip_code = request.form["Zip"]
            sql = "INSERT INTO Publisher (Name, City, Zip) VALUES (%s, %s, %s)"
            val = (name, city, zip_code)
        elif table_name == "Branch":
            city = request.form["city"]
            street = request.form["street"]
            state = request.form["state"]
            zip_code = request.form["zip"]
            sql = (
                "INSERT INTO Branch (City, Street, State, ZIP) VALUES (%s, %s, %s, %s)"
            )
            val = (city, street, state, zip_code)
        elif table_name == "Reader":
            name = request.form["reader_name"]
            email = request.form["email"]
            phone = request.form["phone"]
            city = request.form["city"]
            zip_code = request.form["zip"]
            sql = "INSERT INTO Reader (Name, Email, Phone, City, Zip) VALUES (%s, %s, %s, %s, %s)"
            val = (name, email, phone, city, zip_code)
        elif table_name == "Loaned":
            reader_id = request.form["Reader_ID"]
            book_id = request.form["Book_ID"]
            branch_id = request.form["Branch_ID"]
            issue_date = request.form["Loan_Date"]
            return_date = request.form["Return_Date"]
            sql = "INSERT INTO Loaned (Reader_ID, Book_ID, Branch_ID, Issue_Date, Return_Date) VALUES (%s, %s, %s, %s, %s)"
            val = (reader_id, book_id, branch_id, issue_date, return_date)

        # Execute SQL query and commit changes
        try:
            cur.execute(sql, val)
            db.commit()
            insertion_status = (
                True  # Set insertion_status to True if no exception occurred
            )
        except Exception as e:
            db.rollback()  # Rollback changes if there was an error
            print("Error occurred:", str(e))  # Print error message for debugging
            insertion_status = False

        # return f"{table_name} inserted successfully."
        return render_template("insert_status.html", insertion_status=insertion_status)


# Route to display the borrow form
@app.route("/borrow", methods=["GET"])
def display_borrow_form():
    return render_template("borrow.html")


# Function to borrow a book
@app.route("/borrow", methods=["POST"])
def borrow_book():
    if request.method == "POST":
        customer_id = request.form["customer_id"]
        book_id = request.form["book_id"]
        branch_id = request.form["branch_id"]
        issue_date = request.form["Load_Date"]
        return_date = request.form["return_date"]

        # Example: Inserting borrowed book details into the database
        sql = "INSERT INTO Loaned (Reader_ID, Book_ID, Branch_ID, Issue_Date, Return_Date) VALUES (%s, %s, %s, %s, %s)"
        val = (customer_id, book_id, branch_id, issue_date, return_date)
        cur.execute(sql, val)
        db.commit()
        return render_template("borrow_success.html")


# Route to display the SQL query form
@app.route("/sql_query", methods=["GET"])
def display_sql_query_form():
    return render_template("run_query.html")


# Route to handle the SQL query submission
@app.route("/run_sql_query", methods=["POST"])
def run_sql_query():
    if request.method == "POST":
        sql_query = request.form["sql_query"]
        try:
            cur.execute(sql_query)
            result = cur.fetchall()
            columns = [col[0] for col in cur.description]
            # Convert the list of tuples to a list of dictionaries
            results_with_keys = [dict(zip(columns, row)) for row in result]
            return render_template("query_results.html", result=results_with_keys)
        except mysql.connector.Error as err:
            error_message = f"Error executing SQL query: {err}"
            return render_template("query_error.html", error_message=error_message)


# Route for rendering the interactive dashboard
@app.route("/dashboard")
def dashboard():
    # Query for most borrowed books
    cur.execute(
        "SELECT Name, COUNT(*) AS Total_Borrowed FROM Books INNER JOIN Loaned ON Books.ID = Loaned.Book_ID GROUP BY Name ORDER BY Total_Borrowed DESC LIMIT 5"
    )
    most_borrowed_books = cur.fetchall()

    # Query for most read writers
    cur.execute(
        "SELECT Writer.Name, COUNT(*) AS Total_Read FROM Writer INNER JOIN Books ON Writer.ID = Books.Writer_ID INNER JOIN Loaned ON Books.ID = Loaned.Book_ID GROUP BY Writer.Name ORDER BY Total_Read DESC LIMIT 5"
    )
    most_read_writers = cur.fetchall()

    # Query for user demographics
    cur.execute(
        "SELECT City, Zip, COUNT(*) AS Total_Users FROM Reader GROUP BY City, Zip"
    )
    user_demographics = cur.fetchall()
    return render_template(
        "dashboard.html",
        most_borrowed_books=most_borrowed_books,
        most_read_writers=most_read_writers,
        user_demographics=user_demographics,
    )


if __name__ == "__main__":
    app.run(debug=True)
