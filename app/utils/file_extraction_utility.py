import httpx
import io
import pandas
import requests

def download_public_s3_file_to_dataframe(url):
    response = requests.get(url)
    if response.status_code == 200:
        return  io.StringIO(response.text)