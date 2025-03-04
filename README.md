# Web Application Exercise

A little exercise to build a web application following an agile development process. See the [instructions](instructions.md) for more detail.

## Product vision statement

Our platform connects art enthusiasts with galleries, making it easier to discover, save, filter, and engage with art exhibitions, while enabling gallery owners to easily create and manage exhibition posts.

## User stories

- [User Story 1](https://github.com/software-students-spring2025/2-web-app-pinkberries/issues/1)
- [User Story 2](https://github.com/software-students-spring2025/2-web-app-pinkberries/issues/2)
- [User Story 3](https://github.com/software-students-spring2025/2-web-app-pinkberries/issues/3)
- [User Story 4](https://github.com/software-students-spring2025/2-web-app-pinkberries/issues/4)
- [User Story 5](https://github.com/software-students-spring2025/2-web-app-pinkberries/issues/5)
- [User Story 6](https://github.com/software-students-spring2025/2-web-app-pinkberries/issues/6)
- [User Story 7](https://github.com/software-students-spring2025/2-web-app-pinkberries/issues/7)
- [User Story 8](https://github.com/software-students-spring2025/2-web-app-pinkberries/issues/8)
- [User Story 9](https://github.com/software-students-spring2025/2-web-app-pinkberries/issues/9)
- [User Story 10](https://github.com/software-students-spring2025/2-web-app-pinkberries/issues/10)
- [User Story 11](https://github.com/software-students-spring2025/2-web-app-pinkberries/issues/11)
- [User Story 12](https://github.com/software-students-spring2025/2-web-app-pinkberries/issues/12)
- [User Story 13](https://github.com/software-students-spring2025/2-web-app-pinkberries/issues/13)
- [User Story 14](https://github.com/software-students-spring2025/2-web-app-pinkberries/issues/14)


## Steps necessary to run the software

### Prerequisites
Ensure the following are installed on your system:
- Python 3.8+
- MongoDB (local or Atlas account)
- Git

### Set-up
#### 1. Clone the repository
```
git clone https://github.com/software-students-spring2025/2-web-app-pinkberries.git
cd 2-web-app-pinkberries
```
#### 2. Set up a virtual environment
```
python -m venv venv
```
Replace `python` with `python3` if necessary. 
#### 3. Activate the virtual environment
- on macOS/Linux:
```
source venv/bin/activate
```
- on Windows:
```
venv\Scripts\activate
```
#### 4. Install dependencies
```
pip install -r requirements.txt
```
Replace `pip` with `pip3` if necessary.
#### 5. Configure .env file
- Create a file in the root directory called `.env`
- Edit the `.env` file by referencing the `example.env` file provided:
  - set `MONGO_URI` to your MongoDB connection string
  - set `MONGO_DB` to your database name

### Run application
#### Seed file (optional)
- If you would like to see the website with sample exhibitions pre-populated, run the following beforehand:
```
python seed_exhibitions.py
```
Run the application as follows:
```
flask run
```
By default, it will run on http://127.0.0.1:5000.
## Task boards

- [Sprint 1 Task Board](https://github.com/orgs/software-students-spring2025/projects/47)
- [Sprint 2 Task Board](https://github.com/orgs/software-students-spring2025/projects/120)
