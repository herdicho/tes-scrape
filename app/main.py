from fastapi import FastAPI, Response
from pydantic import BaseModel
from langchain_community.document_loaders import SeleniumURLLoader
import json

class Url(BaseModel):
  url: str

app = FastAPI()

@app.post("/scrape_url")
def scrape_url(url: Url):
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
  
  result = [
    { "Content": content[0].page_content }
  ]

  json_str = json.dumps(result, indent=4, default=str)
  return Response(content=json_str, media_type='application/json')