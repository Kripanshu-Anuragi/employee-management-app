# Employee Management System
A robust, modern, and extensible **desktop application** for efficient employee data management, built with Python, CustomTkinter, and SQLite.

## 🚀 Features
- **Beautiful Modern UI**: CustomTkinter-based, clean design, dark/light-friendly.
- **User Authentication**: Secure login and password change option.
- **Add, Update, Delete & Search**: All-in-one employee record management (CRUD).
- **Case-Insensitive Search**: Quick, user-friendly lookups (e.g., `'Data Scientist'` or `'data scientist'`).
- **Image & Sound Assets**: Subjective UI feedback with icons and button click sounds.
- **Data Persistence**: Uses SQLite, so all employee data is safely stored.
- **Easy Packaging**: Hassle-free EXE build; everything bundled—no manual setup required.
- **Modular Codebase**: Fully open to future enhancements (role-based access, cloud sync, analytics, etc.).

## 🖥️ Screenshot
Signup Screen
> _![Login Screen](assets/images/Signup_screenshot.png)_

## 📦 Folder Structure
employee_management_system/
├── app/
│ ├── login.py
│ ├── main.py
│ └── database.py
├── assets/
│ ├── images/
│ │ └── ... (all UI images)
│ └── sounds/
│ └── click_button.wav
├── data/
│ └── (auto-created .db, user_data.txt)


## 🛠️ Installation & Run (For Developers)
1. Clone the repository:
git clone https://github.com/yourusername/employee_management_system.git
cd employee_management_system
2. Install requirements:
pip install -r requirements.txt
3. Run the app:
python app/login.py

## 🏗️ Build Windows EXE
After code updates:

Remove-Item -Recurse -Force .\dist, .\build, .\EmployeeManagementSystem.spec

pyinstaller --name EmployeeManagementSystem --onefile --windowed --add-data "assets;assets" --add-data "data;data" app/login.py

Executable will be in the `dist` folder.

## 🌟 Contributing & Future Roadmap
This project is **modular and future-ready**!  
Planned/potential features:
- Advanced Role/User access management
- Analytics dashboard—charts, trends, export CSV/Excel
- Cloud data sync, multi-user remote access
- Theme switching, localization/internationalization

**PRs and ideas welcome!**

## 📸 Screenshots

| Login Screen | Dashboard Page |
|--------------|---------------|
| ![Login Screen](assets/images/login_screenshot.png) | ![Dashboard](assets/images/dashboard_screenshot.png) |


## 🤝 License
MIT License

*Built to scale and adapt. Ready for real-world HR teams and the next wave of desktop innovation!*

