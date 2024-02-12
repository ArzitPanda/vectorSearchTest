from flask import Flask, render_template, request, redirect, url_for, jsonify
from PyPDF2 import PdfReader
from pymongo import MongoClient
from openai import OpenAI
import json
from bson import json_util

app = Flask(__name__)

# Connect to MongoDB
client = MongoClient(
    'mongodb+srv://arzit:Panda2001@cluster0.ngraetz.mongodb.net/?retryWrites=true&w=majority'
)
db = client['DataResume']
collection = db['resume']


def extract_text_from_pdf(pdf_file):
  reader = PdfReader(pdf_file)
  text = ""
  for page in reader.pages:
    text += page.extract_text()
  return text


def createJsonMaker(text):
  client = OpenAI(
      api_key="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")

  response = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[{
          "role":
          "system",
          "content":
          "You are a resume-to-JSON maker. You have received A text-based resume. give a json data with name,email,phoneNo,address,skills,education,achievements. don't give any other information."
      }, {
          "role": "user",
          "content": text
      }])
  return response.choices[0].message.content


def makeEmbeddings(text):
  client = OpenAI(
      api_key="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")
  response = client.embeddings.create(input=text,
                                      model="text-embedding-3-small")
  return response.data[0].embedding


@app.route('/')
def index():
  return "hello world"


@app.route('/', methods=['POST'])
def upload_file():
  if request.method == 'POST':
    if 'file' not in request.files:
      return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
      return redirect(request.url)
    if file:
      # Extract text from PDF
      print(file.filename)
      text = extract_text_from_pdf(file)
      sparseText = createJsonMaker(text)
      obj = json.loads(sparseText)
      obj.update({"plot_embedding": makeEmbeddings(text)})
      json_string = json.dumps(obj)

      # # Save extracted text to MongoDB
      # resume_data = {'text': text}
      collection.insert_one(obj)
      return json_string
      # return redirect(url_for('upload_file'))
  return " "


@app.route('/search', methods=['POST'])
def handle_search():
  # Check if request has JSON data
  if not request.is_json:
    return jsonify({'error': 'Request must be JSON'}), 400
  print("hello")
  # Get the search field from the JSON body
  search_field = request.json.get('search')

  # Check if search field is missing
  if not search_field:
    return jsonify({'error': 'Missing search field'}), 400

  # Process the search (e.g., perform some action based on the search)
  # For example, you can search the database based on the search field
  embedding = makeEmbeddings(search_field)
  result_cursor = collection.aggregate([
      {
          "$vectorSearch": {
              "index": "vector_index",
              "path": "plot_embedding",
              "queryVector": embedding,
              "numCandidates": 2,
              "limit": 2
          }
      },
      {
          "$project": {
              "plot_embedding": 0  # Exclude the plot_embedding field
          }
      }
  ])

  # Return the result as JSON
  result_list = [doc for doc in result_cursor]

  # Serialize the list using bson.json_util
  json_result = json_util.dumps(result_list)

  # Return the serialized JSON
  return json_result, 200, {'Content-Type': 'application/json'}


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=80)
