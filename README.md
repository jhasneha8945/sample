Chemical Equipment Parameter Visualizer
The aim of this project is to build a hybrid application that runs both as a Web Application and a Desktop Application. The project focuses on data visualization and analytics for chemical equipment.
Hybrid Web + Desktop app for chemical equipment CSV data analysis and visualization.
Tech Stack
Backend: Django REST API + Pandas + SQLite
Web Frontend: React + Chart.js  
Desktop Frontend: PyQt5 + Matplotlib
Quick Start
 1. Backend (Django API)
bash
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

3. Web Frontend (React)
bash
cd web-frontend
npm install
npm start

5. Desktop Frontend (PyQt5)
bash
cd desktop-frontend
pip install -r requirements.txt
python main.py

Project Structure
text
backend       # Django API
web-frontend    # React + Chart.js
desktop-frontend    # PyQt5 + Matplotlib
sampleequipmentdata.csv  # Test data
 
README.md
Features
CSV Upload
Charts + Stats
History 
PDF Reports

Test Data
Use sampleequipmentdata.csv

Demo
Record 2-3 min video of app working → upload as demo.mp4

