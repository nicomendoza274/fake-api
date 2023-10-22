# PyNotes-API
Welcome to the Fake-API repository! This is a simple guide to help you get started with setting up and running the Fake-API project.

## Actual version
The actual version is [v1.0.0](https://github.com/nicomendoza274/fake-api/releases/tag/v1.0.0).

## Getting Started

Follow these steps to set up and run the project on your local machine:

**Install Python 3.10+**

**Clone the repository:**
```sh 
git clone git@github.com:nicomendoza274/fake-api.git
```
**Create enviroment file**
rename .env.example by .env

**Create a Virtual Environment:**
```sh
 python3 -m venv env
```
**Activate the Virtual Environment:**
On macOS/Linux:
```sh
 source venv/bin/activate
```
On Windows:
```sh
 .\venv\Scripts\activate
```
**Install Dependencies:**
```sh
 pip install -r requirements.txt
```
**Run the Project:**
```sh
 uvicorn main:app --reload
```
## Docker
if you prefer to use docker follow these steps, it is important that you have docker installed on your computer
```sh
docker compose build
```
```sh
docker compose up
```
Once the project is up and running, you can access it through your browser or API client.