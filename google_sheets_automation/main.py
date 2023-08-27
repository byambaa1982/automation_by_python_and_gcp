import pandas as pd
import json
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import sqlite3
from datetime import datetime, timedelta

def get_user_information(sheet_name):
  scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

  creds = ServiceAccountCredentials.from_json_keyfile_name('creds.json',scope)

  client = gspread.authorize(creds)

  industries = client.open("quizs").worksheet(sheet_name)
  users = pd.DataFrame(industries.get_all_values())

  return users


questions = get_user_information("questions")
questions = questions.rename(columns=questions.iloc[0]).drop(questions.index[0])
questions['question_created'] = datetime.now()


db_path = 'quiz.sqlite3'  
conn = sqlite3.connect(db_path)