# ABOUT THIS PROJECT

Python Flask application that fetches and displays data from two APIs: OpenFoodFacts for food product details and nutritional information, and NewsData.io for news articles. Here’s an overview of the code:

**Features:**

**Fetching Food Data:**
The app calls the OpenFoodFacts API to gather data on food products. It allows users to specify parameters like the page number, limit of results per page, and the maximum number of pages to fetch.
It retrieves information on various food items including nutritional values like calories, fat, carbohydrates, vitamins, and minerals.
The data is processed into a Pandas DataFrame, making it easy to manipulate and convert into JSON format for API responses.

**Fetching News Articles:**
The app also allows fetching news articles using the NewsData.io API. It accepts an optional query parameter to filter the news results based on a topic.
The fetched news articles are returned in a JSON format.
Error handling is implemented to ensure that appropriate error messages are returned in case of issues like invalid inputs or API fetch errors.

**Requirements (not limited to):**
1. Flask: Web framework for building the application.
2. Requests: To make HTTP requests to external APIs.
3. Pandas: For processing and structuring data from the APIs into DataFrames.
4. HTML Template: The app uses an HTML template (index.html) located in the public folder for rendering the front-end.
5. Googletrans: For language translation.
6. Redis : Incorporated Redis through Docker to speed up API fetching.
#
**To set up the project locally, follow these steps:**

1. Clone the repository
   ```bash
   git clone https://github.com/maicaalmonte/nutricalculator.git

2. Create virtual environment
   ```bash
   python -m venv .venv

3.  Activate the virtual environment:
 *  On Windows:
 
      ``` bash
       .venv\scripts\activate
   
*  On macOS/Linux:
      ```bash
      source .venv/bin/activate

4. Install Requirements
      ```bash
      pip install -r requirements.txt


#
# ![Screenshot 2024-12-25 105055](https://github.com/user-attachments/assets/8d0a2428-9f40-4d6e-9815-93ca5c741288)
# ![Screenshot 2024-12-25 105104](https://github.com/user-attachments/assets/75f727b9-2054-4666-ad98-77949b92e78a)
# ![Screenshot 2024-12-25 101838](https://github.com/user-attachments/assets/f4e280b9-3617-4767-84ad-58d43ab58294)
# ![Screenshot 2024-12-25 110555](https://github.com/user-attachments/assets/55a4c72c-f549-4a5e-a047-68de4b3ba067)
# ![Screenshot 2024-12-28 183705](https://github.com/user-attachments/assets/5ebd5b84-787f-4c58-9532-db24ed626d68)





