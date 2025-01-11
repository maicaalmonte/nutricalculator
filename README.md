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
![20250112_003236](https://github.com/user-attachments/assets/cb6671ba-0576-4501-953f-5511a41db5c5)






