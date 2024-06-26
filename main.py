from scrape_videos import scrapeVideos
from make_compilation import makeCompilation
from upload_ytvid import uploadYtvid
import schedule
import time
import datetime
import os
import shutil
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import json
import config
import subprocess

num_to_month = {
    1: "Jan",
    2: "Feb",
    3: "Mar",
    4: "Apr",
    5: "May",
    6: "June",
    7: "July",
    8: "Aug",
    9: "Sept",
    10: "Oct",
    11: "Nov",
    12: "Dec"
}

IG_USERNAME = config.IG_USERNAME
IG_PASSWORD = config.IG_PASSWORD

title = "TRY NOT TO LAUGH (BEST Dank video memes) V1"
now = datetime.datetime.now()
videoDirectory = "./DankMemes_" + num_to_month[now.month].upper() + "_" + str(now.year) + "_V" + str(now.day) + "/"
outputFile = "./" + num_to_month[now.month].upper() + "_" + str(now.year) + "_v" + str[now.day] + ".mp4"

INTRO_VID = ''
OUTRO_VID = ''
TOTAL_VID_LENGTH = 13*60
MAX_CLIP_LENGTH = 19
MIN_CLIP_LENGTH = 5
DAILY_SCHEDULED_TIME = "20:00"
TOKEN_NAME = "token.json"

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

def routine():
    creds = None
    if os.path.exists(TOKEN_NAME):
        with open(TOKEN_NAME, 'r') as token:
            creds_data = json.load(token)
            creds = Credentials.from_authorized_user_info(creds_data, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            raise Exception("No valid credentials found.")
        with open(TOKEN_NAME, 'w') as token:
            token.write(creds.to_json())

    googleAPI = build('youtube', 'v3', credentials=creds)

    now = datetime.datetime.now()
    description = ""
    if not os.path.exists(videoDirectory):
        os.makedirs(videoDirectory)

    scrapeVideos(username=IG_USERNAME, password=IG_PASSWORD, output_folder=videoDirectory, days=1)

    description = "Enjoy the memes! :) \n\nlike and subscribe to @Chewy for more \n\n"

    makeCompilation(path=videoDirectory, introName=INTRO_VID, outroName=OUTRO_VID,
                    totalVidLength=TOTAL_VID_LENGTH, maxClipLength=MAX_CLIP_LENGTH,
                    minClipLength=MIN_CLIP_LENGTH, outputFile=outputFile)

    description += "\n\nCopyright Disclaimer, Under Section 107 of the Copyright Act 1976, allowance is made for 'fair use' for purposes such as criticism, comment, news reporting, teaching, scholarship, and research. Fair use is a use permitted by copyright statute that might otherwise be infringing. Non-profit, educational or personal use tips the balance in favor of fair use.\n\n"
    description += "#memes #dankmemes #compilation #funny #funnyvideos \n\n"

    uploadYtvid(VIDEO_FILE_NAME=outputFile, title=title, description=description, googleAPI=googleAPI)

    shutil.rmtree(videoDirectory, ignore_errors=True)
    try:
        os.remove(outputFile)
    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))

    # Commit and push changes to GitHub
    commit_and_push_changes()

def commit_and_push_changes():
    try:
        subprocess.run(["git", "config", "--global", "user.name", "github-actions[bot]"], check=True)
        subprocess.run(["git", "config", "--global", "user.email", "github-actions[bot]@users.noreply.github.com"], check=True)
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", "Automated update"], check=True)
        subprocess.run(["git", "push", f"https://{os.getenv('GH_PAT')}@github.com/{os.getenv('GITHUB_REPOSITORY')}.git", "HEAD:main"], check=True)
        print("Changes pushed to GitHub successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to push changes to GitHub: {e}")

def attemptRoutine():
    while True:
        try:
            routine()
            break
        except OSError as err:
            print(f"Routine Failed on OS error: {err}")
            time.sleep(60 * 60)

schedule.every().day.at(DAILY_SCHEDULED_TIME).do(attemptRoutine)

attemptRoutine()
while True:
    schedule.run_pending()
    time.sleep(60)
