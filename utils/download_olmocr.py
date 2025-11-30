import requests
from tqdm import tqdm
from zipfile import ZipFile
import os
from dotenv import load_dotenv
# from path_generator import generate

## define object for models
class ModelSetup:
    def __init__(self, url, zip_path, extract_path, model_path):
        self.url = url
        self.zip_path = zip_path
        self.extract_path = extract_path
        self.model_path = model_path

    def download(self):
        if os.path.exists(self.zip_path):
            print("Zip already exists, skipping download.")
            return
        with requests.get(self.url, stream=True) as r:
            r.raise_for_status()
            total = int(r.headers.get("content-length", 0))
            with open(self.zip_path, "wb") as f, tqdm(
                total=total, unit="B", unit_scale=True, desc="Downloading"
            ) as bar:
                for chunk in r.iter_content(1024 * 1024):
                    f.write(chunk)
                    bar.update(len(chunk))

    def extract(self):
        with ZipFile(self.zip_path, "r") as zip_ref:
            for file in tqdm(zip_ref.namelist(), desc="Extracting", unit="file"):
                zip_ref.extract(member=file, path=self.extract_path)

    def cleanup(self):
        if os.path.exists(self.zip_path):
            os.remove(self.zip_path)
            print("Zip file deleted.")

    def run(self):
        print("Starting models setup...\n")

        if not os.path.exists(self.model_path):
            self.download()
            self.extract()
        self.cleanup()
        print("\nModel ready!")

##--------------------------------------------------------------------
if __name__ == "__main__":
    # load_dotenv()
    # model_url = os.getenv("model_url")
    # zip_path, extract_path, model_path = generate(url=model_url).values()
    # ModelSetup(
    #     url=model_url,
    #     zip_path=zip_path,
    #     extract_path=extract_path,
    #     model_path=model_path
    # ).run()
    pass