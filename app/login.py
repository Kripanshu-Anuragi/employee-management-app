import os
import sys
from customtkinter import *
from PIL import Image
from tkinter import messagebox

def resource_path(relative_path: str) -> str:
    """Get absolute path to resource, works for dev and PyInstaller EXE."""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    return os.path.normpath(os.path.join(base_path, relative_path))

# --- For PERSISTENT USER DATA ---
def get_user_data_path():
    """
    Returns a path where user_data.txt will ALWAYS be persistent,
    even if built as EXE. EXE: Documents/EmployeeManagementSystem/data/user_data.txt,
    Script: project-root/data/user_data.txt
    """
    if getattr(sys, 'frozen', False):
        docs_folder = os.path.join(os.path.expanduser('~'), "Documents", "EmployeeManagementSystem", "data")
        os.makedirs(docs_folder, exist_ok=True)
        return os.path.join(docs_folder, "user_data.txt")
    else:
        data_dir = resource_path("data")
        os.makedirs(data_dir, exist_ok=True)
        return os.path.join(data_dir, "user_data.txt")

user_data_path = get_user_data_path()

# --- On first run, make sure user_data.txt exists with default user ---
if not os.path.exists(user_data_path) or os.stat(user_data_path).st_size == 0:
    with open(user_data_path, "w") as f:
        f.write("Kripanshu,admin123")

login_window = CTk()
window_width = 930
window_height = 478
screen_width = login_window.winfo_screenwidth()
screen_height = login_window.winfo_screenheight()
x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))
login_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
login_window.resizable(0, 0)
login_window.title("Login Page")

# Background Image
bg_img_path = resource_path("assets/images/login_bg_img.jpg")
image = CTkImage(Image.open(bg_img_path), size=(930, 478))
image_label = CTkLabel(login_window, image=image, text='')
image_label.place(x=0, y=0)

login_heading = CTkLabel(login_window, text='Employee Management System', bg_color="#D7E9FF",
                         text_color="dark blue", font=('Goudy Old Style', 20, 'bold'))
login_heading.place(x=620, y=100)

user_name_entry = CTkEntry(login_window, placeholder_text="Enter Your Username", width=180,
                           fg_color="#F6F7FF", text_color="black")
user_name_entry.place(x=660, y=150)

user_password_entry = CTkEntry(login_window, placeholder_text="Enter Your Password", width=180,
                               show="*", fg_color="#F6F7FF", text_color="black")
user_password_entry.place(x=660, y=200)

eye_open_img = CTkImage(Image.open(resource_path("assets/images/eye_open.png")), size=(20, 20))
eye_closed_img = CTkImage(Image.open(resource_path("assets/images/eye_closed.png")), size=(20, 20))

def toggle_password():
    if user_password_entry.get() == "":
        messagebox.showwarning("Empty Field", "Enter password first!")
        return
    if user_password_entry.cget("show") == "*":
        user_password_entry.configure(show="")
        show_hide_button.configure(image=eye_open_img)
    else:
        user_password_entry.configure(show="*")
        show_hide_button.configure(image=eye_closed_img)

show_hide_button = CTkButton(login_window, command=toggle_password, text="",
                             image=eye_closed_img, width=40, height=30,
                             fg_color="#D7E9FF", hover_color="#F6F7FF",
                             cursor="hand2", bg_color="#D7E9FF")
show_hide_button.place(x=840, y=200)

def login():
    try:
        with open(user_data_path, "r") as f:
            data = f.read().strip()
            saved_user, saved_pass = data.split(",", 1)
    except Exception:
        saved_user, saved_pass = 'Kripanshu', 'DataScientist30LPA'

    if user_name_entry.get() == '' or user_password_entry.get() == '':
        messagebox.showerror('Login Error', 'All fields are required.')
        user_name_entry.delete(0, END)
        user_password_entry.delete(0, END)
    elif user_name_entry.get() == saved_user and user_password_entry.get() == saved_pass:
        messagebox.showinfo('Login Successful', 'You are now logged in.')
        login_window.quit()
        login_window.destroy()
        import main
        main.run()
    else:
        messagebox.showerror('Login Error', 'Invalid credentials. Please try again.')
        user_name_entry.delete(0, END)
        user_password_entry.delete(0, END)

login_button = CTkButton(login_window, text="Login", cursor="hand2", command=login,
                         fg_color="#2C3E50", hover_color="#1D4ED8", text_color="white", corner_radius=0)
login_button.place(x=680, y=250)

def open_signup_window():
    login_window.signup_window = CTkToplevel(login_window)
    signup_window = login_window.signup_window
    sw, sh = 400, 380
    screen_width = login_window.winfo_screenwidth()
    screen_height = login_window.winfo_screenheight()
    sx = int((screen_width / 2) - (sw / 2))
    sy = int((screen_height / 2) - (sh / 2))
    signup_window.geometry(f"{sw}x{sh}+{sx}+{sy}")
    signup_window.title("Sign Up")
    signup_window.resizable(0, 0)
    signup_window.grab_set()
    login_button.configure(state="disabled")

    def signup_window_close():
        login_button.configure(state="normal")
        signup_window.destroy()

    signup_window.protocol("WM_DELETE_WINDOW", signup_window_close)

    CTkLabel(signup_window, text="Old Username").pack(pady=5)
    old_user_entry = CTkEntry(signup_window, placeholder_text="Enter old username")
    old_user_entry.pack(pady=5)

    CTkLabel(signup_window, text="Old Password").pack(pady=5)
    old_pass_entry = CTkEntry(signup_window, placeholder_text="Enter old password", show="*")
    old_pass_entry.pack(pady=5)

    CTkLabel(signup_window, text="New Username").pack(pady=5)
    new_user_entry = CTkEntry(signup_window, placeholder_text="Enter new username")
    new_user_entry.pack(pady=5)

    CTkLabel(signup_window, text="New Password").pack(pady=5)
    new_pass_entry = CTkEntry(signup_window, placeholder_text="Enter new password", show="*")
    new_pass_entry.pack(pady=5)

    def signup_logic():
        old_user = old_user_entry.get().strip()
        old_pass = old_pass_entry.get().strip()
        new_user = new_user_entry.get().strip()
        new_pass = new_pass_entry.get().strip()

        try:
            with open(user_data_path, "r") as f:
                data = f.read().strip()
                if data:
                    stored_user, stored_pass = data.split(",", 1)
                else:
                    stored_user, stored_pass = 'Kripanshu', 'DataScientist30LPA'
        except Exception:
            stored_user, stored_pass = 'Kripanshu', 'DataScientist30LPA'

        if old_user == stored_user and old_pass == stored_pass:
            with open(user_data_path, "w") as f:
                f.write(f"{new_user},{new_pass}")
            messagebox.showinfo("Success", "New user created successfully!")
            signup_window_close()
        else:
            messagebox.showerror("Error", "Old username/password incorrect")

    CTkButton(signup_window, text="Sign Up", command=signup_logic).pack(pady=20)

signup_button = CTkButton(login_window, text="Sign Up", cursor="hand2", command=open_signup_window,
                          fg_color="#1ABC9C", hover_color="#16A085", text_color="white", corner_radius=0)
signup_button.place(x=680, y=290)

login_window.mainloop()
