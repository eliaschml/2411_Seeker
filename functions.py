# this file contains all (mostly non fasthtml) functions for the webapp
import pytesseract
from dotenv import load_dotenv
import os 
from PIL import Image
from io import BytesIO
import pdfplumber
import google.generativeai as genai
import prompts
import uuid
from supabase import create_client

#%% PDF text extractor
# extracts text from all pages of one pdf file
def extract_text(pdf_path):
  # initialize output variable
  raw_text = ''
  with pdfplumber.open(pdf_path) as pdf:
    pages = []
    for page in pdf.pages:
        # Extract text using Tesseract OCR
        image = page.to_image(resolution=500)
        image_bytes = BytesIO()
        image.save(image_bytes, format="PNG")
        image_bytes.seek(0)
        text = pytesseract.image_to_string(Image.open(image_bytes))
        # append text from each page to page list
        pages.append(text)
    # concatenates page texts from list into one string 
    raw_text = " ".join(pages)
  return raw_text

#%% text reordering function
def reorder_text(jumbled_text):
  load_dotenv()
  reordered_texts = '' 
  # setup gemini model
  api_key = os.getenv('GOOGLE_API_KEY')
  genai.configure(api_key=api_key)
  # reorder each text using gemini
  model = genai.GenerativeModel("models/gemini-1.0-pro")
  prompt = prompts.reorder_prompt(jumbled_text)
  response = model.generate_content(
    prompt
  )
  reordered_texts=response.text
  return reordered_texts

#%% generate record id
def gen_record_id():
   record_id = uuid.uuid1()
   return str(record_id)
#%% generate job description id
def gen_jd_id(record_id):
   return f'{record_id}{uuid.uuid1()}'
#%% optimize cv function
def optimize_cv(cv_text, jd_text):
  load_dotenv()
  optimized_cv = '' 
  # setup gemini model
  api_key = os.getenv('GOOGLE_API_KEY')
  genai.configure(api_key=api_key)
  # reorder each text using gemini
  model = genai.GenerativeModel("models/gemini-1.0-pro")
  prompt = prompts.optimize_promt(cv_text, jd_text)
  response = model.generate_content(
    prompt
  )
  optimized_cv=response.text
  return optimized_cv
#%% db get record function
def get_record_dict(record_id=''):
  # returns list of data matching the query from supabase database
  load_dotenv()
  supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))
  try:
    response = (
      supabase
        .table('seeker_log')
        .select('record_dict')
        .eq('record_id',record_id)
        .execute()
    )
    if response.data:
      return response.data
    else:
      print("Record not found")
      return None
  except Exception as e:
    print(f"Error fetching record: {e}")
    return None
#%% db add record function
def add_record(record_id ,record_content):
  load_dotenv()
  supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))
  supabase.table('seeker_log').insert({
    "record_id": record_id
    ,"record_dict": record_content
    }).execute()
#%% db add job description function
def add_jd(record_id ,jd_id, jd_text, submission_timestamp):
  load_dotenv()
  supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))
  supabase.table('jd_log').insert({
    "record_id": record_id
    ,"jd_id": jd_id
    , "jd_text": jd_text
    , "submission_timestamp": submission_timestamp
    }).execute()