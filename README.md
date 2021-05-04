# PSS - Personal Speech Synthesis

**Installation**

1) Install [Python](https://www.python.org/downloads/)
    - Ensure that python.exe and pip.exe are available in your path
2) Install [git](https://git-scm.com/download/win)
3) Clone the project with `git clone https://github.com/CouchMaster789/PSS`
4) Install all Python dependencies by running `pip install -r requirements.txt` (in the root project directory)
5) Setup the database by running the following commands in order:
    1) `flask db init`
    2) `flask db migrate`
    3) `flask db upgrade`

**Updating Versions**

1) Pull the latest version with `git pull`
2) Ensure the latest dependencies are installed with `pip install -r requirements.txt`
3) Update any database model changes with the following commands:
    1) flask db migrate
    2) flask db upgrade
   
**Running the WebApp**

Enter `flask run` into a terminal