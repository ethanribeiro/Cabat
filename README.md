# Cabat

This is a Django project that interacts with the SAM.gov API to fetch and display entity data.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

You need to have Python 3.8.10 and pip/pip3 20.0.2 installed on your machine. This project is built with Django version 4.2.5.

### Installing

1. Clone the repository:
    ```bash
    git clone https://github.com/ethanribeiro/Cabat.git
    ```

2. Navigate into the project directory:
    ```bash
    cd cabat
    ```

3. Install the project dependencies:
    ```bash
    pip3 install -r requirements.txt
    ```

4. Install the redis-server project dependency: (Just in case)
    ```bash
    sudo apt-get update
    ```
    And then
    ```bash
    sudo apt-get install redis-server
    ```

### Project Setup

1. Create a `.env` file in the project root directory (same as where the manage.py file is located) and then copy & paste this block of code into the '.env' file:
    ```plaintext
    API_KEY=yourAPIKey
    DJANGO_SECRET_KEY='django-insecure-*wjx(lzqw%+uq!ml5=ps9ifhmc%_zj#0^t^m2ww#86*q&8aesy'
    DATABASE_NAME=Cabat
    DATABASE_MONGODB_URI=mongodbLink
    DATABASE_MONGODB_USERNAME=yourUsername
    DATABASE_MONGODB_PASSWORD=yourPassword
    ```

2. Go to the MongoDB Atlas website and create an account: https://www.mongodb.com/atlas/database
   1. Answer the "Getting to know you" questions with "Learn MongoDB", "I've never developed software with MongoDB before", "Python", Select all boxes except "Other", and then "Not sure"
   2. Select M0 (the free option), leave name as Cluster0, select Google Cloud as provider, Select Iowa (us-central1) for Region, and then click on the "Create Deployment" button.
   3. If "Username" and "Password" are preloaded onto the fields, take a quick picture on your phone of the screen showing your username and password. Once that's done, click on the "Copy" button, then click on "Create Database User", and then click on "Choose a connection method" button.
   4. Click on "Drivers".
   5. For your driver, select Python, and then select version "3.12 or later". You should already have pymongo installed from step 3 of installing project dependencies from requirements.txt file. Click on the copy icon, under "3. Add your connection string into your application code", on the left side. And then click "Done".
   6. On the left sidebar, click on "Network Access" tab, under "Security" with a lock icon.
   7. Click on "+ ADD IP ADDRESS", then click on "ALLOW ACCESS FROM ANYWHERE", then delete what's inside the "Comment:" field, and then click "Confirm".
   8. Wait until the "Status" of IP Address 0.0.0.0/0 says "Active".

3. Go back to the `.env` file and paste the MongoDB connection string that you previously copied, to the `DATABASE_MONGODB_URI` variable.
   1. Modify the connection string by deleting this part in the end of string: `&appName=Cluster0`
   2. Copy and paste your sam.gov api key to the `API_KEY` variable.
   3. Copy and paste your mongodb username to the `DATABASE_MONGODB_USERNAME` variable and your mongodb password to the `DATABASE_MONGODB_PASSWORD` variable. (Hint: Just copy from the connection string you pasted in the `DATABASE_MONGODB_URI` variable: `mongodb+srv://<username>:<password>@cluster0`)

4. In the terminal, opened in the root directory “cabat”, enter:
    ```bash
    sudo service redis-server stop
    ```
    And then:
    ```bash
    sudo redis-server
    ```

5. Open another tab in the terminal, while redis-server is running, opened in the root directory “cabat” like before, and then enter:
    ```bash
    daphne -b 0.0.0.0 -p 8000 cabat.asgi:application
    ```
    And the program should then be up and running!

6. Open your browser and go to `http://localhost:8000/sam_api/entities/`. There you should see a button that says “Fetch Opportunities”. Click on it and it should then send a get request to sam.gov, via API, and then be receiving contracts. The program will notify you if the get request was successful or not. Click “Ok”, and if ran successfully, you should be seeing a list of 10 “Opportunities”.

### Please note!

The prototype is set in a way that it will only fetch 10 opportunities. If you tried to click the button again, nothing will have seem to change. This is intentional for the prototype demo. Further versions of said prototype will be set with collecting more data and new data as this project soon will reach it’s “product ready” state.
