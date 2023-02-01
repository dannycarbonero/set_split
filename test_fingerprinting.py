#%%

file_name = "E:/Library v4/Trance/Paul van Dyk/The Politics Of Dancing 3/10 - For You.mp3"
file_name_2 ='E:/Library v4/Other/Scores/Risk of Rain 2/15 - The Rain Formerly Known as Purple.mp3'

#%%
import acoustid
import requests
import json

fingerprint = acoustid.fingerprint_file(file_name_2)
response = requests.get("https://api.acoustid.org/v2/lookup", params={"client": "dASxAPhfZl", "meta": "recordings", "duration": int(fingerprint[0]), "fingerprint": fingerprint[1], "format": "json",})
data = response.json()