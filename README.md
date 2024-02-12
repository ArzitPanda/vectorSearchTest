
## Title: Resume Processing and Search API


1. **Resume Processing:** Upload a PDF resume and receive a JSON response containing extracted information like name, email, skills, education, and achievements.
2. **Resume Search:** Submit a search query and retrieve similar resumes based on their content using text embeddings.

## Features

* Extracts text from uploaded PDF resumes.
* Uses OpenAI API to convert text to JSON format and create text embeddings.
* Stores processed resumes in a MongoDB database.
* Enables searching for similar resumes based on text embeddings.

## Usage

### Resume Processing

1. Access the API endpoint at `/`.
2. Send a POST request with a file named `file` containing the PDF resume.
3. The API will respond with a JSON object containing the extracted information.

### Resume Search

1. Access the API endpoint at `/search`.
2. Send a POST request with a JSON payload containing the `search` field specifying your search query.
3. The API will respond with a JSON array containing the most relevant resumes based on their text embeddings.

## Prerequisites

* Python 3.x
* Flask
* PyPDF2
* pymongo
* openai
* MongoDB instance with a database and collection named `DataResume` and `resume` respectively.

## Installation

1. Install required dependencies:

```bash
pip install Flask PyPDF2 pymongo openai bson
```

2. Replace placeholders in `app.py` with your MongoDB connection details and OpenAI API key.

## Running the Application

```bash
python app.py
```

This starts the Flask application on port 80. You can access the API endpoints at `http://localhost:80/` and `http://localhost:80/search`.

## Notes

* This is a basic example and can be further customized based on your specific needs.
* Consider security aspects like user authentication and authorization for production environments.
* Explore advanced search functionalities and improve result accuracy based on your dataset.

This README file provides a basic overview of your application. You can further customize it to include more details, instructions, and examples relevant to your specific functionalities. Remember to update placeholders with your actual credentials and data structure.
