from fastapi import FastAPI, Response
from pydantic import BaseModel
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from langchain_community.document_loaders import SeleniumURLLoader
import json
import textwrap
from fpdf import FPDF
from PyPDF2 import PdfFileMerger

class Url(BaseModel):
  url: str

app = FastAPI()

@app.post("/scrape_url")
def scrape_url(url: Url):
  # Set up Chrome options
  chrome_options = webdriver.ChromeOptions()
  chrome_options.add_argument("--headless")
  chrome_options.add_argument("--no-sandbox")
  chrome_options.add_argument("--disable-dev-shm-usage")
  
  service = Service(ChromeDriverManager().install())

  # Set path to chromedriver as per Docker setup
  driver = webdriver.Chrome(service=service, options=chrome_options)
  
  # Use the SeleniumURLLoader with the provided driver
  loader = SeleniumURLLoader(urls=[url.url], browser='chrome', arguments=[
          "--disable-dev-shm-usage",
          "--window-size=1920,1080",
          "--headless",
          "--disable-gpu",
          "--no-sandbox",
          "--start-maximized",
      ],)
  
  # Get the data
  content = loader.load()
  
  # Close the driver
  driver.quit()

  result = [
    { "Content": content[0].page_content }
  ]

  json_str = json.dumps(result, indent=4, default=str)
  return Response(content=json_str, media_type='application/json')