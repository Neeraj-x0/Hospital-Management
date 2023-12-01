from tkinter import *
from tkinter import messagebox
import sqlite3
from menu import Menu
from admin_reg import RegistrationFrame
conn = sqlite3.connect("SQL.db")
c = conn.cursor()


class LoginFrame(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("HOSPITAL MANAGEMENT SYSTEM")
        self.master.geometry("800x500+0+0")
        self.master.config(bg="powder blue")
        self.pack()

        self.Username = StringVar()
        self.Password = StringVar()

        self.create_widgets()

    def create_widgets(self):
        self.lblTitle = Label(self, text="HOSPITAL MANAGEMENT SYSTEM",
                              font="Helvetica 20 bold", bg="powder blue", fg="black")
        self.lblTitle.grid(row=0, column=0, columnspan=2, pady=40)

        self.LoginFrame1 = Frame(
            self, width=400, height=80, relief="ridge", bg="cadet blue", bd=20)
        self.LoginFrame1.grid(row=1, column=0)
        self.LoginFrame2 = Frame(
            self, width=400, height=80, relief="ridge", bg="cadet blue", bd=20)
        self.LoginFrame2.grid(row=2, column=0)

        self.lblUsername = Label(
            self.LoginFrame1, text="Username", font="Helvetica 14 bold", bg="cadet blue", bd=22)
        self.lblUsername.grid(row=0, column=0)
        self.entryUsername = Entry(
            self.LoginFrame1, font="Helvetica 14 bold", textvariable=self.Username, bd=2)
        self.entryUsername.grid(row=0, column=1)

        self.lblPassword = Label(
            self.LoginFrame1, text="Password", font="Helvetica 14 bold", bg="cadet blue", bd=22)
        self.lblPassword.grid(row=1, column=0)
        self.entryPassword = Entry(
            self.LoginFrame1, font="Helvetica 14 bold", show="*", textvariable=self.Password, bd=2)
        self.entryPassword.grid(row=1, column=1)

        self.btnLogin = Button(self.LoginFrame2, text="Login", font="Helvetica 10 bold",
                               width=10, bg="powder blue", command=self.login_system)
        self.btnLogin.grid(row=3, column=0)
        self.btnExit = Button(self.LoginFrame2, text="Exit", font="Helvetica 10 bold",
                              width=10, bg="powder blue", command=self.master.destroy)
        self.btnExit.grid(row=3, column=1)
        self.btnAdminManagement = Button(self.LoginFrame2, text="Admin Management",
                                         font="Helvetica 10 bold", width=15, bg="powder blue", command=self.admin_management_login)
        self.btnAdminManagement.grid(row=3, column=2)

    def admin_management_login(self):
        # Create a custom dialog for entering the master password
        dialog = Toplevel(self.master)
        dialog.title("Admin Management Login")

        lblPassword = Label(dialog, text="Master Password:",
                            font="Helvetica 14 bold", bd=22)
        lblPassword.grid(row=0, column=0)

        entryPassword = Entry(dialog, font="Helvetica 14 bold", show="*", bd=2)
        entryPassword.grid(row=0, column=1)

        btnLogin = Button(dialog, text="Login", font="Helvetica 10 bold", width=10, bg="powder blue",
                          command=lambda: self.verify_master_password(entryPassword.get(), dialog))
        btnLogin.grid(row=1, column=0, columnspan=2, pady=10)

    def verify_master_password(self, entered_password, dialog):
        c.execute("SELECT VALUE FROM SECURITY WHERE IDENTIFIER = 'master_pass'")
        result = c.fetchone()

        # Verify the entered master password (You need to check it against the stored master password in the database)
        # Replace with actual stored master password check
        if entered_password == result[0]:
            self.newWindow = Toplevel(self.master)
            self.app = RegistrationFrame(self.newWindow)
        else:
            messagebox.showerror(
                "HOSPITAL MANAGEMENT SYSTEM", "INVALID MASTER PASSWORD")

    def login_system(self):
        username = self.Username.get()
        password = self.Password.get()

        # Check if the username exists in the database
        c.execute("SELECT * FROM ADMIN WHERE USERNAME=?", (username,))
        admin_data = c.fetchone()

        if admin_data is not None:
            # Assuming password is stored in the second column
            admin_password = admin_data[2]

            # Verify the entered password
            if admin_password == password:
                self.newWindow = Toplevel(self.master)
                self.app = Menu(self.newWindow)
            else:
                messagebox.showerror(
                    "HOSPITAL MANAGEMENT SYSTEM", "INVALID PASSWORD")
        else:
            messagebox.showerror(
                "HOSPITAL MANAGEMENT SYSTEM", "INVALID USERNAME")


def main():
    root = Tk()
    app = LoginFrame(root)
    root.mainloop()


if __name__ == "__main__":
    main()
