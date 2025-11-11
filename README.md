RotaBasit 📍 (Simple Route Optimizer)

This project is a "Micro-SaaS" (Software as a Service) prototype designed to help small businesses (like florists, restaurants, or e-commerce shops) optimize their daily delivery routes that involve multiple stops.

The project uses a Flask (Python) backend and a Leaflet.js (JavaScript) frontend. The optimization "brain" solves the Vehicle Routing Problem (VRP) using Google's industrial-grade ortools library.

(Image from the live, locally-running project)

⚠️ Important Note: Why is there no live link?

This project cannot run on free hosting services like Render, Heroku, or PythonAnywhere due to the high memory (RAM) usage of the ortools library.

The low memory limits of free-tier servers cause them to crash when attempting to load this "heavy" library.

Therefore, this repository is intended as a portfolio project. Its purpose is to demonstrate my skills in Industrial Engineering (optimization) and Full-Stack web development (Python/Flask + JS).

To see the full project and its optimization "brain" in action, you must run it on your local machine.

🚀 Local Setup and Running

You can get the project running on your computer in 5 minutes:

1. Clone the Project:

git clone [https://github.com/yigitckk/RotaBasit.git](https://github.com/yigitckk/RotaBasit.git)
cd RotaBasit


2. Set Up a Python Virtual Environment:

# Windows
python -m venv venv
venv\Scripts\activate

# MacOS / Linux
python3 -m venv venv
source venv/bin/activate


3. Install Required Libraries:
(This step may take a few minutes as it installs ortools.)

pip install -r requirements.txt


4. Start the Server:

python app.py


5. Open Your Browser:
Navigate to http://127.0.0.1:5000/ in your browser.

You can now select the stops and press "Rotayı Optimize Et" (Optimize Route) to test the ortools optimization live.

🛠️ Tech Stack

Backend: Python, Flask

Optimization: Google OR-Tools

Frontend: Vanilla JavaScript, Leaflet.js, HTML5, CSS3

Server: Gunicorn

🎯 Future Development Ideas

Steps that could be built upon this prototype:

Real Geocoding: Allowing users to enter text addresses and converting them to coordinates via an API like Google Maps.

Dynamic Distance Matrix: Integrating an API to pull real-time driving distances (including traffic) between selected points, rather than using a static matrix.

"Lighter" Algorithm: To make the project deployable on free servers, replacing ortools with a custom Simulated Annealing metaheuristic algorithm coded in pure Python.
