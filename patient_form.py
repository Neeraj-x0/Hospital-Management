from tkinter import *
import tkinter.messagebox
import sqlite3
conn = sqlite3.connect("SQL.db")
print("DATABASE CONNECTION SUCCESSFUL")

class Patient:
    def __init__(self, master):
        self.master = master
        self.master.title("HOSPITAL MANAGEMENT SYSTEM")
        self.master.geometry("1500x700+0+0")
        self.master.config(bg="cadet blue")
        self.frame = Frame(self.master, bg="cadet blue")
        self.frame.pack()

        # =============ATTRIBUTES===========
        self.pat_ID = IntVar()
        self.pat_name = StringVar()
        self.pat_dob = StringVar()
        self.pat_address = StringVar()
        self.pat_sex = StringVar()
        self.pat_BG = StringVar()
        self.pat_email = StringVar()
        self.pat_contact = IntVar()
        self.pat_contactalt = IntVar()
        self.pat_CT = StringVar()

        # ===============TITLE==========
        self.lblTitle = Label(self.frame, text="PATIENT REGISTRATION FORM",
                              font="Helvetica 20 bold", bg="cadet blue")
        self.lblTitle.grid(row=0, column=0, columnspan=2, pady=50)

        # ==============FRAME==========
        self.LoginFrame = Frame(self.frame, width=400, height=80, relief="ridge", bg="cadet blue", bd=20)
        self.LoginFrame.grid(row=1, column=0)

        self.LoginFrame2 = Frame(self.frame, width=400, height=80, relief="ridge", bg="cadet blue", bd=20)
        self.LoginFrame2.grid(row=2, column=0)

        # ===========LABELS=============
        labels = [
            ("PATIENT ID", self.pat_ID, 0, 0),
            ("PATIENT NAME", self.pat_name, 1, 0),
            ("SEX", self.pat_sex, 2, 0),
            ("DOB (YYYY-MM-DD)", self.pat_dob, 3, 0),
            ("BLOOD GROUP", self.pat_BG, 4, 0),
            ("CONTACT NUMBER", self.pat_contact, 0, 2),
            ("ALTERNATE CONTACT", self.pat_contactalt, 1, 2),
            ("EMAIL", self.pat_email, 2, 2),
            ("CONSULTING TEAM / DOCTOR", self.pat_CT, 3, 2),
            ("ADDRESS", self.pat_address, 4, 2),
        ]

        for label_text, variable, row, column in labels:
            lbl = Label(self.LoginFrame, text=label_text, font="Helvetica 14 bold", bg="cadet blue", bd=22)
            lbl.grid(row=row, column=column)
            entry = Entry(self.LoginFrame, font="Helvetica 14 bold", bd=2, textvariable=variable)
            entry.grid(row=row, column=column + 1)

        # Buttons
        buttons = [
            ("SUBMIT", 10, self.INSERT_PAT),
            ("UPDATE", 11, self.UPDATE_PAT),
            ("DELETE", 12, self.D_DISPLAY),
            ("SEARCH", 13, self.S_DISPLAY),
            ("EXIT", 14, self.Exit),
        ]

        for button_text, col, command in buttons:
            btn = Button(self.LoginFrame2, text=button_text, width=10, font="Helvetica 14 bold", bg="cadet blue", command=command)
            btn.grid(row=3, column=col)

    def clear(self):
        # Clear all entry fields
        for variable in [self.pat_ID, self.pat_name, self.pat_dob, self.pat_address,
                         self.pat_sex, self.pat_BG, self.pat_email, self.pat_contact,
                         self.pat_contactalt, self.pat_CT]:
            variable.set("")

    def INSERT_PAT(self):
        p1 = self.pat_ID.get()
        p2 = self.pat_name.get()
        p3 = self.pat_sex.get()
        p4 = self.pat_BG.get()
        p5 = self.pat_dob.get()
        p6 = self.pat_contact.get()
        p7 = self.pat_contactalt.get()
        p8 = self.pat_address.get()
        p9 = self.pat_CT.get()
        p10 = self.pat_email.get()

        # Check if patient ID already exists
        existing_patient = conn.execute("SELECT * FROM PATIENT WHERE PATIENT_ID=?", (p1,)).fetchall()

        if existing_patient:
            tkinter.messagebox.showerror("HOSPITAL DATABASE SYSTEM", "PATIENT_ID ALREADY EXISTS")
        else:
            conn.execute('INSERT INTO PATIENT VALUES(?,?,?,?,?,?,?,?)', (p1, p2, p3, p4, p5, p8, p9, p10,))
            conn.execute('INSERT INTO CONTACT_NO VALUES (?,?,?)', (p1, p6, p7,))
            tkinter.messagebox.showinfo("HOSPITAL DATABASE SYSTEM", "DETAILS INSERTED INTO DATABASE")
            self.clear()
        conn.commit()

    def UPDATE_PAT(self):
        u1 = self.pat_ID.get()
        u2 = self.pat_name.get()
        u3 = self.pat_sex.get()
        u4 = self.pat_dob.get()
        u5 = self.pat_BG.get()
        u6 = self.pat_contact.get()
        u7 = self.pat_contactalt.get()
        u8 = self.pat_email.get()
        u9 = self.pat_CT.get()
        u10 = self.pat_address.get()

        existing_patient = conn.execute("SELECT * FROM PATIENT WHERE PATIENT_ID=?", (u1,)).fetchall()

        if existing_patient:
            conn.execute('UPDATE PATIENT SET NAME=?,SEX=?,DOB=?,BLOOD_GROUP=?,ADDRESS=?,CONSULT_TEAM=?,EMAIL=? WHERE PATIENT_ID=?',
                         (u2, u3, u4, u5, u10, u9, u8, u1,))
            conn.execute('UPDATE CONTACT_NO SET CONTACTNO=?,ALT_CONTACT=? WHERE PATIENT_ID=?', (u6, u7, u1,))
            tkinter.messagebox.showinfo("HOSPITAL DATABASE SYSTEM", "DETAILS UPDATED INTO DATABASE")
            self.clear()
            conn.commit()
        else:
            tkinter.messagebox.showerror("HOSPITAL DATABASE SYSTEM", "PATIENT IS NOT REGISTERED")

    def Exit(self):
        self.master.destroy()

    def D_DISPLAY(self):
        self.newWindow = Toplevel(self.master)
        self.app = DMenu(self.newWindow)

    def S_DISPLAY(self):
        self.newWindow = Toplevel(self.master)
        self.app = SMenu(self.newWindow)


class DMenu:
    def __init__(self, master):
        self.master = master
        self.master.title("HOSPITAL MANAGEMENT SYSTEM")
        self.master.geometry("1500x700+0+0")
        self.master.config(bg="cadet blue")
        self.frame = Frame(self.master, bg="cadet blue")
        self.frame.pack()
        self.del_pid = IntVar()
        self.lblTitle = Label(self.frame, text="DELETE WINDOW", font="Helvetica 20 bold", bg="cadet blue")
        self.lblTitle.grid(row=0, column=0, columnspan=2, pady=50)

        # ==============FRAME==========
        self.LoginFrame = Frame(self.frame, width=400, height=80, relief="ridge", bg="cadet blue", bd=20)
        self.LoginFrame.grid(row=1, column=0)

        self.LoginFrame2 = Frame(self.frame, width=400, height=80, relief="ridge", bg="cadet blue", bd=20)
        self.LoginFrame2.grid(row=2, column=0)

        # ===========LABELS=============
        self.lblpatid = Label(self.LoginFrame, text="ENTER PATIENT ID TO DELETE", font="Helvetica 14 bold", bg="cadet blue", bd=22)
        self.lblpatid.grid(row=0, column=0)
        self.lblpatid = Entry(self.LoginFrame, font="Helvetica 14 bold", bd=2, textvariable=self.del_pid)
        self.lblpatid.grid(row=0, column=1)

        self.DeleteB = Button(self.LoginFrame2, text="DELETE", width=10, font="Helvetica 14 bold", bg="cadet blue", command=self.DELETE_PAT)
        self.DeleteB.grid(row=3, column=1)

    def DELETE_PAT(self):
        inp_d = self.del_pid.get()
        c1 = conn.cursor()
        existing_patient = conn.execute("SELECT * FROM PATIENT WHERE PATIENT_ID=?", (inp_d,)).fetchall()

        if not existing_patient:
            tkinter.messagebox.showerror("HOSPITAL DATABASE SYSTEM", "PATIENT RECORD NOT FOUND")
        else:
            conn.execute('DELETE FROM PATIENT WHERE PATIENT_ID=?', (inp_d,))
            tkinter.messagebox.showinfo("HOSPITAL DATABASE SYSTEM", "DETAILS DELETED FROM DATABASE")
            conn.commit()


class SMenu:
    def __init__(self, master):
        self.master = master
        self.master.title("HOSPITAL MANAGEMENT SYSTEM")
        self.master.geometry("1500x700+0+0")
        self.master.config(bg="cadet blue")
        self.frame = Frame(self.master, bg="cadet blue")
        self.frame.pack()
        self.s_pid = IntVar()
        self.lblTitle = Label(self.frame, text="SEARCH WINDOW", font="Helvetica 20 bold", bg="cadet blue")
        self.lblTitle.grid(row=0, column=0, columnspan=2, pady=25)

        # ==============FRAME==========
        self.LoginFrame = Frame(self.frame, width=400, height=80, relief="ridge", bg="cadet blue", bd=20)
        self.LoginFrame.grid(row=1, column=0)

        self.LoginFrame2 = Frame(self.frame, width=400, height=80, relief="ridge", bg="cadet blue", bd=20)
        self.LoginFrame2.grid(row=2, column=0)

        # ===========LABELS=============
        self.lblpatid = Label(self.LoginFrame, text="ENTER PATIENT ID TO SEARCH", font="Helvetica 14 bold", bg="cadet blue", bd=22)
        self.lblpatid.grid(row=0, column=0)
        self.lblpatid = Entry(self.LoginFrame, font="Helvetica 14 bold", bd=2, textvariable=self.s_pid)
        self.lblpatid.grid(row=0, column=1)

        # ===========Button=============
        self.SearchB = Button(self.LoginFrame2, text="SEARCH", width=10, font="Helvetica 14 bold", bg="cadet blue", command=self.SEARCH_PAT)
        self.SearchB.grid(row=0, column=1)

        self.ExitB = Button(self.LoginFrame2, text="EXIT", width=10, font="Helvetica 14 bold", bg="cadet blue", command=self.master.destroy)
        self.ExitB.grid(row=0, column=2)

    def SEARCH_PAT(self):
        inp_s = self.s_pid.get()
        c1 = conn.cursor()
        existing_patient = conn.execute('SELECT * FROM PATIENT WHERE PATIENT_ID=?', (inp_s,)).fetchall()

        if not existing_patient:
            tkinter.messagebox.showerror("HOSPITAL DATABASE SYSTEM", "PATIENT RECORD NOT FOUND")
        else:
            result = c1.execute('SELECT * FROM PATIENT NATURAL JOIN CONTACT_NO WHERE PATIENT_ID=?', (inp_s,)).fetchone()
            self.display_search_result(result)

    def display_search_result(self, result):
        labels = [
            ("PATIENT ID", result[0], 1, 0),
            ("PATIENT NAME", result[1], 2, 0),
            ("SEX", result[2], 3, 0),
            ("DOB (YYYY-MM-DD)", result[4], 5, 0),
            ("BLOOD GROUP", result[3], 4, 0),
            ("ADDRESS", result[5], 1, 2),
            ("CONSULTING TEAM / DOCTOR", result[6], 2, 2),
            ("EMAIL", result[7], 3, 2),
            ("CONTACT NUMBER", result[8], 4, 2),
            ("ALTERNATE CONTACT", result[9], 5, 2),
        ]

        for label_text, value, row, column in labels:
            label = Label(self.LoginFrame, text=label_text, font="Helvetica 14 bold", bg="cadet blue", bd=22)
            label.grid(row=row, column=column)
            display_label = Label(self.LoginFrame, font="Helvetica 14 bold", bd=2, bg="cadet blue", text=value)
            display_label.grid(row=row, column=column + 1)
