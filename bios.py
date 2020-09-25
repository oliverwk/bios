#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, sys
os.system('clear')
import requests
from bs4 import BeautifulSoup
import csv, xlsxwriter
import json
URL = "https://www.pathe.nl/bioscoop/utrechtleidscherijn"
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.5 Safari/605.1.15'}
page = requests.get(URL, headers=headers )
soup = BeautifulSoup(page.content, 'html.parser')
body = soup.find(id="js-cinema-schedule")
csv_file = open("/Users/MWK/Desktop/rdw/bios.csv","w")
fieldnames = ['titel', 'Start tijd', 'img_url']
writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
writer.writeheader()
xlsx = '/Users/MWK/Desktop/bios/bios.xlsx'
workbook = xlsxwriter.Workbook(xlsx)
worksheet = workbook.add_worksheet()
N1AKD = open("/Users/MWK/Desktop/rdw/bios.json","w")
N1AKD.writelines("[")
items = body.find_all("div", class_="schedule-simple__item")
count = 1
datas=[]

catogorie = 0
Naam = 0
Start_tijd = 1
img_url = 2

for item in items:
    data = {}
    p_data = item.find("a", class_="poster")
    print("\n"+p_data["title"])
    li = item.find("li", class_="js-tooltip-parental-advisory")
    icons = li.find_all("img")
    for icon in icons:
        advies = icon["alt"]
        print(advies)
        catogorie = icon["src"].split("-")[1].split("-")[0]
        print(catogorie)
        worksheet.write(count, Naam, str(catogorie))
        catogorien = []
        catogorien.append(catogorie)
        data["catogorien"] = catogorien

    catogorie = icons[0]["src"].split("-")[1].split("-")[0]
    start_times = item.find("span", class_="schedule-time__start")
    print("De film begint om: "+start_times.get_text())
    hd_img = p_data.find("img")
    print("\n"+hd_img["src"])
    worksheet.write(count, Naam, str(p_data["title"]))
    worksheet.write(count, Start_tijd, str(start_times.get_text()))
    worksheet.write(count, img_url, str(hd_img["src"]))
    worksheet.write(count, catogorie, str(icons[0]["src"].split("-")[1].split("-")[0])
    writer.writerow({'titel': p_data["title"] , 'Start tijd': start_times.get_text(), 'img_url': hd_img["src"]})
    data["title"] = p_data["title"]
    data["tijd"] = start_times.get_text()
    data["img_url"] = hd_img["src"].replace(" ", "%20")
    data["id"] = count
    json.dumps(data)
    datas.append(data)
    count += 1



csv_file.close()
workbook.close()
N1AKD.close()
def sortFunction(value):
	return value["tijd"]

sorteds = sorted(json.loads(str(datas).replace("'", '"')), key=sortFunction)
jsonx = open("/Users/MWK/Desktop/rdw/bios.json","w")
jsonx.writelines(str(json.dumps(sorteds, indent=4)))
jsonx.close()
from github import Github
print("Pushing to Github")
g = Github(os.getenv("git_access_token"))
repo = g.get_repo("oliverwk/wttpknng")
contents = repo.get_contents("bios.json")
repo.update_file(contents.path, "updated bios.json from python3", str(json.dumps(sorteds, indent=4)), contents.sha, branch="master")
print("Pushed to Github")
print("sending wathsapp message")
from twilio.rest import Client
account_sid = 'AC560f51cedc776774bd44d9c9688fbc43'
auth_token = str(os.getenv("twillio_authkey"))

client = Client(account_sid, auth_token)
message = client.messages.create(
                              from_='whatsapp:+14155238886',
                              body=f"Om {sorteds[0]['tijd']} begint de film {sorteds[0]['title']}.",
                              media_url=[sorteds[0]["img_url"]],
                              to='whatsapp:+31622339914'
                          )
print("The wathsapp message send: ",f"Om {sorteds[0]['tijd']} begint de film {sorteds[0]['title']}.")
