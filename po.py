import sqlite3
from tkinter import *
from tkinter import messagebox


class Database:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.create_tables()

    def create_tables(self):
        self.conn.execute('CREATE TABLE IF NOT EXISTS client (id integer, name TEXT, adresse TEXT )')
        self.conn.execute('CREATE TABLE IF NOT EXISTS orders (id integer, categorie TEXT, date TEXT , FOREIGN KEY (client_id) REFERENCES client(id) ON DELETE CASCADE)')
        self.conn.commit()

    def add_client(self, id, name, adresse):
        try:
            self.conn.execute("INSERT INTO client (id, name, adresse) VALUES (?, ?, ?)", (id, name, adresse))
            self.conn.commit()
            return "Client added successfully!"
        except Exception as e:
            return f"Error: {e}"

    def add_order(self, order_id, category, date , client_id):
        try:
            self.conn.execute("INSERT INTO orders (id, categorie, date , client_id) VALUES (?, ?, ?,?)", (order_id, category, date , client_id))
            self.conn.commit()
            return "Order added successfully!"
        except Exception as e:
            return f"Error: {e}"

    def delete_order(self, order_id):
        try:
            self.conn.execute("DELETE FROM orders WHERE id = ?", (order_id,))
            self.conn.commit()
            return "Order deleted successfully!"
        except Exception as e:
            return f"Error: {e}"

    def check_order(self, order_id):
        cursor = self.conn.execute("SELECT * FROM orders WHERE id = ?", (order_id,))
        order = cursor.fetchone()
        if order:
            return f"Order ID: {order[0]}, Category: {order[1]}, Date: {order[2]} , Client: {order[3]}"
        return "Order not found"

    def check_client(self,client_id):
        cursor = self.conn.execute("SELECT * FROM orders WHERE client_id = ?", (client_id,))
        orders = cursor.fetchall()
        if orders:
            return orders
        else:
            return "No orders found for this client."

    def close(self):
        self.conn.close()


class OrderApp:
    def __init__(self, win, db):
        self.win = win
        self.db = db
        self.win.title("Orders Management")
        self.win.geometry("975x500")
        self.win.config(bg="#f5f5f5")
        self.win.iconbitmap("C:/Users/pc/Downloads/order.ico")

        self.client_frame = Frame(self.win, bg="white", bd=2, relief="solid", padx=300, pady=100)
        self.order_frame = Frame(self.win, bg="white", bd=2, relief="solid", padx=300, pady=10)
        self.check_frame = Frame(self.win, bg="white", bd=2, relief="solid", padx=300, pady=100)
        self.view_orders_frame = Frame(self.win, bg="white", bd=2, relief="solid", padx=300, pady=100)

        def show_frame(frame):
            frame.tkraise()

        for frame in (self.client_frame, self.order_frame, self.check_frame , self.view_orders_frame):
            frame.grid(row=1, column=0, columnspan=4, sticky="nsew", padx =20 ,pady=10)


        Button(self.win, text="Add Client", font=("Arial", 12, "bold"), command=lambda: show_frame(self.client_frame),
               width=20, bg="#FFF6E3").grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        Button(self.win, text="Add/Delete Order", font=("Arial", 12, "bold"),
               command=lambda: show_frame(self.order_frame), width=20, bg="#FFCCEA").grid(row=0, column=1, sticky="ew", padx=10, pady=10)

        Button(self.win, text="Check Order", font=("Arial", 12, "bold"), command=lambda: show_frame(self.check_frame),
               width=20, bg="#BFECFF").grid(row=0, column=2, sticky="ew", padx=10, pady=10)
        Button(self.win, text="View Client Orders", font=("Arial", 12, "bold"),
               command=lambda: show_frame(self.view_orders_frame), width=20, bg="#FFDFDF").grid(row=0, column=3,sticky="ew",padx=10, pady=10)



        self.init_client_frame()
        self.init_order_frame()
        self.init_check_frame()
        self.init_view_orders_frame()

    def init_client_frame(self):
        Label(self.client_frame, text="Add New Client", font=("Arial", 14, "bold"), bg="white").grid(row=0, column=0,pady=5)

        self.id_entry = Entry(self.client_frame, width=40)
        self.id_entry.insert(0, "Enter ID here")
        self.id_entry.grid(row=1, column=0, padx=10, pady=5)

        self.name_entry = Entry(self.client_frame, width=40)
        self.name_entry.insert(0, "Enter Name here")
        self.name_entry.grid(row=2, column=0, padx=10, pady=5)

        self.adresse_entry = Entry(self.client_frame, width=40)
        self.adresse_entry.insert(0, "Enter Address here")
        self.adresse_entry.grid(row=3, column=0, padx=10, pady=5)

        Button(self.client_frame, text="Submit Client", font=("Arial", 10, "bold"), command=self.add_client, width=15,bg="#add8e6").grid(row=4, column=0, pady=10)

    def add_client(self):
        idd = int(self.id_entry.get())
        name = self.name_entry.get()
        adresse = self.adresse_entry.get()
        message = self.db.add_client(idd, name, adresse)
        Label(self.client_frame, text=message, fg="green", bg="white").grid(row=5, column=0, pady=10)

    def init_order_frame(self):
        Label(self.order_frame, text="Add/Delete Order", font=("Arial", 14, "bold"), bg="white").grid(row=0, column=0,pady=5)

        self.order_id_entry = Entry(self.order_frame, width=40)
        self.order_id_entry.insert(0, "Enter Order ID here")
        self.order_id_entry.grid(row=1, column=0, padx=10, pady=5)

        self.category_entry =Listbox(self.order_frame, width=40)
        self.category_entry.insert(1, "Legumes")
        self.category_entry.insert(2, "Fruits")
        self.category_entry.insert(3, "Electronics")
        self.category_entry.insert(4, "Vetements")
        self.category_entry.grid(row=2, column=0, padx=10, pady=5)

        self.date_entry = Entry(self.order_frame, width=40)
        self.date_entry.insert(0, "Enter Date here")
        self.date_entry.grid(row=3, column=0, padx=10, pady=5)

        self.client_id_entry = Entry(self.order_frame, width=40)
        self.client_id_entry.insert(0, "Enter Client ID here")
        self.client_id_entry.grid(row=4, column=0, padx=10, pady=5)

        Button(self.order_frame, text="Add Order", font=("Arial", 10, "bold"), command=self.add_order, width=15,bg="#90ee90").grid(row=5, column=0, pady=10)
        Button(self.order_frame, text="Delete Order", font=("Arial", 10, "bold"), command=self.delete_order, width=15, bg="#f08080").grid(row=7, column=0, pady=10)

    def show_warning(self):
        messagebox.showwarning("Warning", "Please fill in all fields.")

    def add_order(self):
        order_id = self.order_id_entry.get()
        date = self.date_entry.get()
        client_id = self.client_id_entry.get()

        selected_category_index = self.category_entry.curselection()
        #si l'utilisateur choisi un choix parmi les choix available :
        if selected_category_index:
            category = self.category_entry.get(selected_category_index)
        #sinon ca va remplir categorie par une chaine videet qui va ensuite causer un erreur
        else:
            category = ""
        if not order_id or not category or not date or not client_id:
            self.show_warning()
        else:
            message = self.db.add_order(int(order_id), category, date , client_id)
        Label(self.order_frame, text=message, fg="green", bg="white").grid(row=5, column=1, pady=5)

    def delete_order(self):
        order_id = int(self.order_id_entry.get())
        message = self.db.delete_order(order_id)
        Label(self.order_frame, text=message, fg="green", bg="white").grid(row=6, column=0, pady=5)

    def init_check_frame(self):
        Label(self.check_frame, text="Check Order", font=("Arial", 14, "bold"), bg="white").grid(row=0, column=0,pady=5)
        self.check_id_entry = Entry(self.check_frame, width=40)
        self.check_id_entry.insert(0, "Enter Order ID to Check")
        self.check_id_entry.grid(row=1, column=0, padx=10, pady=5)
        Button(self.check_frame, text="Check Order", font=("Arial", 10, "bold"), command=self.check_order, width=15,bg="#ffb6c1").grid(row=2, column=0, pady=10)

    def check_order(self):
        check_id = int(self.check_id_entry.get())
        message = self.db.check_order(check_id)
        Label(self.check_frame, text=message, fg="green", bg="white").grid(row=3, column=0, pady=10)

    def init_view_orders_frame(self):
        Label(self.view_orders_frame, text="View Orders for Client", font=("Arial", 14, "bold"), bg="white").grid(row=0,column=0,pady=5)
        self.client_id_entry_for_orders = Entry(self.view_orders_frame, width=40)
        self.client_id_entry_for_orders.insert(0, "Enter Client ID here")
        self.client_id_entry_for_orders.grid(row=1, column=0, padx=10, pady=5)

        Button(self.view_orders_frame, text="View Orders", font=("Arial", 10, "bold"), command=self.view_client_orders,
               width=15, bg="#f5a9a9").grid(row=2, column=0, pady=10)

    def view_client_orders(self):
        client_id = int(self.client_id_entry_for_orders.get())
        orders = self.db.check_client(client_id)

        result_str = ""
        if isinstance(orders, str):
            result_str = orders
        else:
            for order in orders:
                result_str += f" - Order ID: {order[0]}, Category: {order[1]}, Date: {order[2]}\n"

        messagebox.showinfo("Client Orders", result_str)


db = Database("orders.db")
win = Tk()
app = OrderApp(win, db)
win.mainloop()
db.close()
