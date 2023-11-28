import sqlite3
from tkinter import *
from tkinter import messagebox
from tkinter.simpledialog import askstring
conn = sqlite3.connect("SQL.db")
c = conn.cursor()


class ManageAdminWindow(Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.title("Manage Admin")
        self.master.geometry("1500x700+0+0")
        self.config(bg="powder blue")

        self.admin_id = StringVar()
        self.admin_name = StringVar()

        self.create_widgets()

    def create_widgets(self):
        label_admin_id = Label(
            self, text="Enter Admin Name:", font="Helvetica 14 bold", bg="powder blue")
        label_admin_id.grid(row=0, column=0, padx=20, pady=20)
        entry_admin_id = Entry(
            self, font="Helvetica 14 bold", textvariable=self.admin_id, bd=2)
        entry_admin_id.grid(row=0, column=1, padx=20, pady=20)

        btn_submit = Button(self, text="Submit", font="Helvetica 12 bold",
                            width=10, bg="cadet blue", command=self.display_admin_details)
        btn_submit.grid(row=1, column=0, columnspan=2, pady=20)
        btn_exit = Button(self, text="Exit", font="Helvetica 12 bold",
                          width=10, bg="powder blue", command=self.destroy)
        btn_exit.grid(row=1, column=1, columnspan=2, pady=20)

    def display_admin_details(self):
        entered_admin_id = self.admin_id.get()
        c.execute("SELECT * FROM ADMIN WHERE USERNAME=?", (entered_admin_id,))
        admin_data = c.fetchone()

        if admin_data:
            # Assuming the name is in the second column
            self.admin_name.set(admin_data[1])
            self.show_management_buttons()
        else:
            messagebox.showerror(
                "HOSPITAL MANAGEMENT SYSTEM", "Invalid Admin ID")

    def show_management_buttons(self):
        admin_name_label = Label(
            self, textvariable=self.admin_name, font="Helvetica 14 bold", bg="powder blue")
        admin_name_label.grid(row=2, column=0, columnspan=2, pady=20)

        btn_delete_admin = Button(self, text="Delete Admin", font="Helvetica 12 bold",
                                  width=15, bg="powder blue", command=self.verify_master_password)
        btn_delete_admin.grid(row=3, column=0, pady=10)

        btn_change_password = Button(self, text="Change Password", font="Helvetica 12 bold",
                                     width=15, bg="powder blue", command=self.change_password)
        btn_change_password.grid(row=3, column=1, pady=10)

    def verify_master_password(self):
        master_password = askstring(
            "Verify Master Password", "Enter master password:")

        # Fetch the master password from the database

        c.execute("SELECT VALUE FROM SECURITY WHERE IDENTIFIER = 'master_pass'")
        result = c.fetchone()
        print(result)
        if result:
            # Assuming the master password is at index 1
            stored_master_password = result[0]
            if master_password == stored_master_password:
                self.delete_admin()
            else:
                messagebox.showerror(
                    "HOSPITAL MANAGEMENT SYSTEM", "Invalid master password")
        else:
            messagebox.showerror(
                "HOSPITAL MANAGEMENT SYSTEM", "Master password not found in the database")

    def delete_admin(self):
        admin_id_to_delete = self.admin_id.get()

        # Perform the deletion from the database (You need to implement this)
        c.execute("DELETE FROM ADMIN WHERE USERNAME =?", (admin_id_to_delete,))
        conn.commit()

        messagebox.showinfo(
            "HOSPITAL MANAGEMENT SYSTEM", "Admin deleted successfully!")

    def change_password(self):
        admin_id_to_change = askstring("Change Password", "Enter Admin ID:")
        if not admin_id_to_change:
            return  # User canceled the input

        # Ask for the current password for verification
        current_password = askstring(
            "Change Password", "Enter current password:")
        if not current_password:
            return  # User canceled the input

        # Verify the current password
        if not self.verify_current_password(admin_id_to_change, current_password):
            messagebox.showerror("HOSPITAL MANAGEMENT SYSTEM",
                                 "Incorrect current password!")
            return

        # Ask for the new password
        new_password = askstring("Change Password", "Enter new password:")
        if not new_password:
            return  # User canceled the input

        # Update the password in the database
        conn = sqlite3.connect("SQL.db")
        c = conn.cursor()

        c.execute("UPDATE ADMIN SET PASSWORD=? WHERE USERNAME=?",
                  (new_password, admin_id_to_change))

        conn.commit()
        conn.close()

        messagebox.showinfo("HOSPITAL MANAGEMENT SYSTEM",
                            "Password changed successfully!")

    def verify_current_password(self, admin_id, current_password):
        # Verify the current password against the stored password in the database
        conn = sqlite3.connect("SQL.db")
        c = conn.cursor()

        # Example: Assuming your table name is 'ADMIN'
        c.execute("SELECT PASSWORD FROM ADMIN WHERE USERNAME=?", (admin_id,))
        stored_password = c.fetchone()

        conn.close()
        print(stored_password, current_password, sep='\t\t')
        # Check if the entered current password matches the stored password
        return stored_password is not None and current_password == stored_password[0]


class RegistrationFrame(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("HOSPITAL MANAGEMENT SYSTEM - Admin Registration")
        self.master.geometry("800x500+0+0")
        self.master.config(bg="powder blue")
        self.pack()

        self.AdminUsername = StringVar()
        self.AdminPassword = StringVar()

        self.create_widgets()

    def create_widgets(self):

        self.lblTitle = Label(self, text="ADMIN REGISTRATION",
                              font="Helvetica 20 bold", bg="powder blue", fg="black")
        self.lblTitle.grid(row=0, column=0, columnspan=2, pady=40)

        self.RegistrationFrame1 = Frame(
            self, width=400, height=80, relief="ridge", bg="cadet blue", bd=20)
        self.RegistrationFrame1.grid(row=1, column=0)
        self.RegistrationFrame2 = Frame(
            self, width=400, height=80, relief="ridge", bg="cadet blue", bd=20)
        self.RegistrationFrame2.grid(row=2, column=0)

        self.lblAdminUsername = Label(
            self.RegistrationFrame1, text="Admin Username", font="Helvetica 14 bold", bg="cadet blue", bd=22)
        self.lblAdminUsername.grid(row=0, column=0)
        self.entryAdminUsername = Entry(
            self.RegistrationFrame1, font="Helvetica 14 bold", textvariable=self.AdminUsername, bd=2)
        self.entryAdminUsername.grid(row=0, column=1)

        self.lblAdminPassword = Label(
            self.RegistrationFrame1, text="Admin Password", font="Helvetica 14 bold", bg="cadet blue", bd=22)
        self.lblAdminPassword.grid(row=1, column=0)
        self.entryAdminPassword = Entry(
            self.RegistrationFrame1, font="Helvetica 14 bold", show="*", textvariable=self.AdminPassword, bd=2)
        self.entryAdminPassword.grid(row=1, column=1)

        self.btnRegister = Button(self.RegistrationFrame2, text="Register",
                                  font="Helvetica 10 bold", width=10, bg="powder blue", command=self.register_admin)
        self.btnRegister.grid(row=3, column=0)
        self.btnExit = Button(self.RegistrationFrame2, text="Exit", font="Helvetica 10 bold",
                              width=10, bg="powder blue", command=self.master.destroy)
        self.btnExit.grid(row=3, column=1)
        self.btnManage = Button(self.RegistrationFrame2, text="Manage",
                                font="Helvetica 10 bold", width=10, bg="powder blue", command=self.open_manage_window)
        self.btnManage.grid(row=3, column=2)

    def open_manage_window(self):
        manage_admin_window = ManageAdminWindow(self.master)

    def register_admin(self):
        admin_username = self.AdminUsername.get()
        admin_password = self.AdminPassword.get()

        # Store admin details in the database
        conn = sqlite3.connect("SQL.db")
        c = conn.cursor()

        # Check if the username already exists
        c.execute("SELECT * FROM ADMIN WHERE USERNAME=?", (admin_username,))
        if c.fetchone() is not None:
            messagebox.showerror("HOSPITAL MANAGEMENT SYSTEM",
                                 "Username already exists!")
        else:
            c.execute("INSERT INTO ADMIN (USERNAME, PASSWORD) VALUES (?, ?)",
                      (admin_username, admin_password))
            conn.commit()
            conn.close()

            messagebox.showinfo("HOSPITAL MANAGEMENT SYSTEM",
                                "Admin registered successfully!")
            self.master.destroy()


