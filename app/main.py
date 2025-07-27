import os
import sys
from customtkinter import *
from PIL import Image
from tkinter import ttk, messagebox
import database
import winsound

def resource_path(relative_path: str) -> str:
    """
    Get absolute path to resource, works for dev and PyInstaller.
    """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    return os.path.normpath(os.path.join(base_path, relative_path))

def auto_insert_emp_prefix(event):
    current_text = id_entry.get()
    if not current_text.startswith("EMP"):
        id_entry.insert(0, "EMP")


def run():
    global app_window, id_entry, name_entry, phone_entry, role_box, gender_box, salary_entry, advanced_table

    app_window = CTk()
    window_width = 1300
    window_height = 780

    # Get screen size
    screen_width = app_window.winfo_screenwidth()
    screen_height = app_window.winfo_screenheight()

    # Calculate x and y coordinates to center the window
    x = int((screen_width / 2) - (window_width / 2))
    y = int((screen_height / 2) - (window_height / 2))

    # Set the geometry of the window to be window_width x window_height and placed at x,y
    app_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    app_window.resizable(False, False)
    app_window.title('Employee Management System')
    app_window.configure(fg_color='black')

    # Continue your existing code ...
    logo = CTkImage(Image.open(resource_path('assets/images/bgemp.jpg')), size=(window_width, 165))
    logoLabel = CTkLabel(app_window, image=logo, text='')
    logoLabel.grid(row=0, column=0, columnspan=2)

    # Core functional definitions

    def add_employee():
        if id_entry.get() == '' or phone_entry.get() == '' or name_entry.get() == '' or salary_entry.get() == '':
            messagebox.showerror('Error', 'Please Fill All Fields')
        elif database.id_exists(id_entry.get()):
            messagebox.showerror('Error', 'ID already exists')
        elif not id_entry.get().startswith('EMP'):
            messagebox.showerror('Error', "Invalid ID format. Use 'EMP' followed by a number (e.g., 'EMP1').")
        else:
            database.insert_data(id_entry.get(), name_entry.get(), phone_entry.get(), role_box.get(), gender_box.get(), salary_entry.get())
            inserted_data_view()
            clear()
            winsound.PlaySound(resource_path('assets/sounds/click_button.wav'), winsound.SND_FILENAME)
            messagebox.showinfo('Success', 'Employee Added')

    def inserted_data_view():
        employees = database.fetch_employees()
        advanced_table.delete(*advanced_table.get_children())
        for employee in employees:
            advanced_table.insert('', END, values=employee)

    def clear(value=False):
        if value:
            advanced_table.selection_remove(advanced_table.focus())
        id_entry.delete(0, END)
        name_entry.delete(0, END)
        phone_entry.delete(0, END)
        role_box.set('AI Researcher')
        gender_box.set('Male')
        salary_entry.delete(0, END)

    def selection(event):
        selected_item = advanced_table.selection()
        if selected_item:
            row = advanced_table.item(selected_item)['values']
            clear()
            id_entry.insert(0, row[0])
            name_entry.insert(0, row[1])
            phone_entry.insert(0, row[2])
            role_box.set(row[3])
            gender_box.set(row[4])
            salary_entry.insert(0, row[5])

    def update_employee():
        selected_item = advanced_table.selection()
        if not selected_item:
            messagebox.showerror("Error", "Select Data To Update")
        else:
            database.update(id_entry.get(), name_entry.get(), phone_entry.get(), role_box.get(), gender_box.get(), salary_entry.get())
            inserted_data_view()
            clear()
            messagebox.showinfo("Success", "Data is Updated")

    def delete_employee():
        selected_item = advanced_table.selection()
        if not selected_item:
            messagebox.showerror('Error', 'No Employee Selected')
        else:
            database.delete(id_entry.get())
            inserted_data_view()
            clear()
            messagebox.showinfo('Success', 'Employee Deleted')

    def search_employee():
        if search_entry.get() == '':
            messagebox.showerror('Error', 'Enter Value To Search')
        elif search_box.get() == 'Search By':
            messagebox.showerror('Error', 'Please Select Option From Search By')
        else:
            searched_data = database.search(search_box.get(), search_entry.get())
            advanced_table.delete(*advanced_table.get_children())
            for employee in searched_data:
                advanced_table.insert('', END, values=employee)

    def show_all():
        inserted_data_view()
        search_entry.delete(0, END)
        search_box.set('Search By')

    def delete_all():
        result = messagebox.askyesno('Confirm', 'Do you really want to delete all records?')
        if result:
            database.delete_all_records()
            inserted_data_view()
            clear()

    # Layout - Left frame (inputs + labels)
    left_window_frame = CTkFrame(app_window, fg_color='black')
    left_window_frame.grid(row=1, column=0)

    id_icon = CTkImage(Image.open(resource_path("assets/images/logo_id.png")), size=(25, 25))
    name_icon = CTkImage(Image.open(resource_path("assets/images/logo_name.png")), size=(25, 25))
    phone_icon = CTkImage(Image.open(resource_path("assets/images/logo_phone.png")), size=(25, 25))
    role_icon = CTkImage(Image.open(resource_path("assets/images/logo_role.png")), size=(25, 25))
    gender_icon = CTkImage(Image.open(resource_path("assets/images/logo_gender.png")), size=(25, 25))
    salary_icon = CTkImage(Image.open(resource_path("assets/images/logo_salary.png")), size=(25, 25))

    label_style = {"font": ("Arial", 18, "bold"), "text_color": "white", "fg_color": "transparent",
                   "anchor": "w", "compound": "left"}

    id_label = CTkLabel(left_window_frame, text="         Id", image=id_icon, **label_style)
    id_label.grid(row=0, column=0, padx=(0, 8), pady=30)
    name_label = CTkLabel(left_window_frame, text="   Name", image=name_icon, **label_style)
    name_label.grid(row=1, column=0, padx=10, pady=30)
    phone_label = CTkLabel(left_window_frame, text="   Phone", image=phone_icon, **label_style)
    phone_label.grid(row=2, column=0, padx=10, pady=30)
    role_label = CTkLabel(left_window_frame, text="      Role", image=role_icon, **label_style)
    role_label.grid(row=3, column=0, padx=10, pady=30)
    gender_label = CTkLabel(left_window_frame, text="  Gender", image=gender_icon, **label_style)
    gender_label.grid(row=4, column=0, padx=10, pady=30)
    salary_label = CTkLabel(left_window_frame, text="   Salary", image=salary_icon, **label_style)
    salary_label.grid(row=5, column=0, padx=10, pady=30)

    id_entry = CTkEntry(left_window_frame, font=('Arial', 17, 'bold'), width=200, height=35,
                        border_width=2, corner_radius=3,
                        fg_color="#F8F9FA", border_color="#ced4da", text_color="#212529")
    id_entry.grid(row=0, column=1, padx=(5, 12), pady=12)
    id_entry.bind("<FocusIn>", auto_insert_emp_prefix)

    name_entry = CTkEntry(left_window_frame, font=('Arial', 17, 'bold'), width=200, height=35,
                          border_width=2, corner_radius=3,
                          fg_color="#F8F9FA", border_color="#ced4da", text_color="#212529")
    name_entry.grid(row=1, column=1)

    phone_entry = CTkEntry(left_window_frame, font=('Arial', 17, 'bold'), width=200, height=35,
                           border_width=2, corner_radius=3,
                           fg_color="#F8F9FA", border_color="#ced4da", text_color="#212529")
    phone_entry.grid(row=2, column=1)

    role_options = ['Data Scientist', 'Data Analyst', 'Machine Learning Engineer',
                    'Data Engineer', 'Business Intelligence Analyst', 'Statistician',
                    'AI Researcher', 'Deep Learning Engineer']
    role_box = CTkComboBox(left_window_frame, values=role_options, state='readonly',
                           font=('Arial', 17, 'bold'), width=200, height=35,
                           border_width=2, corner_radius=3,
                           fg_color="#F8F9FA", border_color="#ced4da", text_color="#212529")
    role_box.grid(row=3, column=1)
    role_box.set('AI Researcher')

    gender_options = ['Male', 'Female']
    gender_box = CTkComboBox(left_window_frame, values=gender_options, state='readonly',
                             font=('Arial', 17, 'bold'), width=200, height=35,
                             border_width=2, corner_radius=3,
                             fg_color="#F8F9FA", border_color="#ced4da", text_color="#212529")
    gender_box.grid(row=4, column=1)
    gender_box.set('Male')

    salary_entry = CTkEntry(left_window_frame, font=('Arial', 17, 'bold'), width=200, height=35,
                            border_width=2, corner_radius=3,
                            fg_color="#F8F9FA", border_color="#ced4da", text_color="#212529")
    salary_entry.grid(row=5, column=1)

    # Right Frame: Search, Table, Buttons etc.
    right_window_frame = CTkFrame(app_window, fg_color='silver', width=900)
    right_window_frame.grid(row=1, column=1, pady=10)

    search_options = ['id', 'Name', 'Phone', 'Role', 'Gender', 'Salary']
    search_box = CTkComboBox(right_window_frame, values=search_options, width=180, state='readonly',
                             font=('Arial', 15, 'bold'), height=29,
                             border_width=2, corner_radius=3,
                             fg_color="#F8F9FA", border_color="white", text_color="#212529")
    search_box.grid(row=0, column=0, pady=0, padx=(5, 5))
    search_box.set('Search By')

    search_entry = CTkEntry(right_window_frame, placeholder_text='Search By (Value)',
                            font=('Arial', 15, 'bold'), height=28,
                            border_width=2, corner_radius=3,
                            fg_color="#F8F9FA", border_color="white", text_color="#212529")
    search_entry.grid(row=0, column=1, pady=0, padx=(0, 150))

    search_button = CTkButton(right_window_frame, text="Search By",
                             font=("Arial", 15, "bold"), width=120, height=28,
                             corner_radius=5, fg_color="#0d6efd", hover_color="#0b5ed7",
                             border_color="#0a58ca", border_width=2,
                             text_color="white", cursor="hand2",
                             command=search_employee)
    search_button.grid(row=0, column=2, pady=0, padx=(150, 0))
    search_button.bind("<ButtonPress>", lambda e: search_button.configure(border_width=4))
    search_button.bind("<ButtonRelease>", lambda e: search_button.configure(border_width=2))

    show_all_button = CTkButton(right_window_frame, text="Show All",
                               font=("Arial", 15, "bold"), width=120, height=28,
                               corner_radius=5, fg_color="#0d6efd", hover_color="#0b5ed7",
                               border_color="#0a58ca", border_width=2,
                               text_color="white", cursor="hand2", command=show_all)
    show_all_button.grid(row=0, column=3, pady=(8, 6), padx=(4, 0))
    show_all_button.bind("<ButtonPress>", lambda e: show_all_button.configure(border_width=4))
    show_all_button.bind("<ButtonRelease>", lambda e: show_all_button.configure(border_width=2))

    advanced_table = ttk.Treeview(right_window_frame, height=14)
    advanced_table.grid(row=1, column=0, columnspan=4, sticky="ew", padx=(2, 2), pady=(3, 3))
    advanced_table['columns'] = ('Id', 'Name', 'Phone', 'Role', 'Gender', 'Salary')

    for col in advanced_table['columns']:
        advanced_table.heading(col, text=col)

    advanced_table.config(show='headings')
    advanced_table.column('Id', width=100)
    advanced_table.column('Name', width=160)
    advanced_table.column('Phone', width=160)
    advanced_table.column('Role', width=200)
    advanced_table.column('Gender', width=140)
    advanced_table.column('Salary', width=160)

    style = ttk.Style()
    style.theme_use("clam")
    style.configure('Treeview.Heading', font=('arial', 14, 'bold'))
    style.configure('Treeview', font=('arial', 11, 'bold'), rowheight=30,
                    background='#161C30', foreground='white')

    scrollbar = ttk.Scrollbar(right_window_frame, orient=VERTICAL, command=advanced_table.yview)
    scrollbar.grid(row=1, column=4, sticky='ns', pady=(5, 4), padx=(1, 4))
    advanced_table.configure(yscrollcommand=scrollbar.set)

    bottom_window_frame = CTkFrame(app_window, fg_color='black')
    bottom_window_frame.grid(row=2, column=0, columnspan=2)

    new_button_logo_icon = CTkImage(Image.open(resource_path("assets/images/logo_new_employee.png")), size=(30, 30))
    add_button_logo_icon = CTkImage(Image.open(resource_path("assets/images/logo_add_employee.png")), size=(30, 30))
    update_button_logo_icon = CTkImage(Image.open(resource_path("assets/images/logo_update_employee.png")), size=(30, 30))
    delete_button_logo_icon = CTkImage(Image.open(resource_path("assets/images/logo_delete_employee.png")), size=(30, 30))
    delete_all_button_logo_icon = CTkImage(Image.open(resource_path("assets/images/logo_delete_all.png")), size=(30, 30))

    new_button = CTkButton(bottom_window_frame, text="  New Employee", image=new_button_logo_icon,
                           font=("Arial", 15, "bold"), width=160, height=40, corner_radius=15,
                           fg_color="#0d6efd", hover_color="#0b5ed7",
                           border_color="#0a58ca", border_width=2, text_color="white",
                           anchor="w", compound="left", command=lambda: clear(True))
    new_button.grid(row=0, column=0, pady=(10, 5), padx=(0, 30))
    new_button.bind("<ButtonPress>", lambda e: new_button.configure(border_width=4))
    new_button.bind("<ButtonRelease>", lambda e: new_button.configure(border_width=2))

    add_button = CTkButton(bottom_window_frame, text="  Add Employee", image=add_button_logo_icon,
                          font=("Arial", 15, "bold"), width=160, height=40, corner_radius=15,
                          fg_color="#0d6efd", hover_color="#0b5ed7",
                          border_color="#0a58ca", border_width=2, text_color="white",
                          anchor="w", compound="left", command=add_employee)
    add_button.grid(row=0, column=1, pady=(10, 5), padx=30)
    add_button.bind("<ButtonPress>", lambda e: add_button.configure(border_width=4))
    add_button.bind("<ButtonRelease>", lambda e: add_button.configure(border_width=2))

    update_button = CTkButton(bottom_window_frame, text="  Update Employee", image=update_button_logo_icon,
                             font=("Arial", 15, "bold"), width=160, height=40, corner_radius=15,
                             fg_color="#0d6efd", hover_color="#0b5ed7",
                             border_color="#0a58ca", border_width=2, text_color="white",
                             anchor="w", compound="left", command=update_employee)
    update_button.grid(row=0, column=2, pady=(10, 5), padx=30)
    update_button.bind("<ButtonPress>", lambda e: update_button.configure(border_width=4))
    update_button.bind("<ButtonRelease>", lambda e: update_button.configure(border_width=2))

    delete_button = CTkButton(bottom_window_frame, text="  Delete Employee", image=delete_button_logo_icon,
                             font=("Arial", 15, "bold"), width=160, height=40, corner_radius=15,
                             fg_color="#0d6efd", hover_color="#0b5ed7",
                             border_color="#0a58ca", border_width=2, text_color="white",
                             anchor="w", compound="left", command=delete_employee)
    delete_button.grid(row=0, column=3, pady=(10, 5), padx=30)
    delete_button.bind("<ButtonPress>", lambda e: delete_button.configure(border_width=4))
    delete_button.bind("<ButtonRelease>", lambda e: delete_button.configure(border_width=2))

    delete_all_button = CTkButton(bottom_window_frame, text="  Delete All", image=delete_all_button_logo_icon,
                                 font=("Arial", 15, "bold"), width=160, height=40, corner_radius=15,
                                 fg_color="#0d6efd", hover_color="#0b5ed7",
                                 border_color="#0a58ca", border_width=2, text_color="white",
                                 anchor="w", compound="left", command=delete_all)
    delete_all_button.grid(row=0, column=4, pady=(10, 5), padx=(30, 0))
    delete_all_button.bind("<ButtonPress>", lambda e: delete_all_button.configure(border_width=4))
    delete_all_button.bind("<ButtonRelease>", lambda e: delete_all_button.configure(border_width=2))

    inserted_data_view()
    advanced_table.bind('<<TreeviewSelect>>', selection)
    app_window.mainloop()

if __name__ == "__main__":
    run()
