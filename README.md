# Fake-API

Welcome to the Fake-API repository! This is a simple guide to help you get started with setting up and running the Fake-API project.

## Actual version

The actual version is [v2.1.0](https://github.com/nicomendoza274/fake-api/releases/tag/v2.1.0).

## Getting Started

- **Clone the repository:**

  ```sh
  git clone git@github.com:nicomendoza274/fake-api.git
  ```

## Installation

Follow these steps to set up and run the project on your local machine:

- **Install Python 3.10+**

- **Create a Virtual Environment:**

  ```sh
  python3 -m venv venv
  ```

- **Activate the Virtual Environment:**
  On macOS/Linux:

  ```sh
  source venv/bin/activate
  ```

  On Windows:

  ```sh
  .\venv\Scripts\activate
  ```

- **Install Dependencies:**

  ```sh
  pip install -r requirements.txt
  ```

- **Create environment files in root**

  Copy env.example and change it to create all environment: `.env.dev`, `.env.qa`, `.env.prod`

  ```sh
  cp env.example .env.dev
  ```

- **Move to src folder**

  ```sh
  cd src/
  ```

- **Run the Project:**

  Development

  ```sh
  uvicorn main:app --env-file ../.env.dev --reload
  ```

  QA

  ```sh
  uvicorn main:app --env-file ../.env.qa --reload
  ```

  > Or select your **profile debugger** and press **F5**. **F5** run QA default.

  Once the project is up and running, you can access it through your [browser](http://localhost:8000/)
