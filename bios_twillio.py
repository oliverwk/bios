#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def first_movie():
    import os
    os.system('clear')
    import requests
    from bs4 import BeautifulSoup

    URL = "https://www.pathe.nl/bioscoop/utrechtleidscherijn"

    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.5 Safari/605.1.15','content-type': 'application/json'}
    page = requests.get(URL, headers=headers )
    print(page.content)
    soup = BeautifulSoup(page.content, 'html.parser')
    times = soup.find("div", class_="schedule__container")
    start_times = times.find_all("span", class_="schedule-time__start")

    for time in start_times:
        print("\nDit zijn de tijden")
        print(time.get_text())

    poster = soup.find(class_="poster")
    hd_img = poster.find("img")
    print("\n"+hd_img["data-lazy"])
    print("\n"+poster["title"])

def multi_movie():
    import os
    os.system('clear')
    import requests
    from bs4 import BeautifulSoup
    import csv
    import random
    import json
    URL = "https://www.pathe.nl/bioscoop/utrechtleidscherijn"

    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.5 Safari/605.1.15'}
    page = requests.get(URL, headers=headers )
    soup = BeautifulSoup(page.content, 'html.parser')

    body = soup.find(id="js-cinema-schedule")

    csv_file = open("/Users/MWK/Desktop/rdw/bios.csv","w")
    fieldnames = ['Naam', 'Start tijd', 'img_url']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    N1AKD = open("/Users/MWK/Desktop/rdw/bios.json","w")
    N1AKD.writelines("[")
    items = body.find_all("div", class_="schedule-simple__item")
    count = 1
    for item in items:
        p_data = item.find("a", class_="poster")
        print("\n"+p_data["title"])
        start_times = item.find("span", class_="schedule-time__start")
        print("De film begint om: "+start_times.get_text())
        hd_img = p_data.find("img")
        print("\n"+hd_img["src"])
        writer.writerow({'Naam': p_data["title"], 'Start tijd': start_times.get_text(), 'img_url': hd_img["src"]})
        data = {}
        data['title'] = p_data["title"]
        data['year'] = start_times.get_text()
        data['img_url'] = hd_img["src"]
        data['id'] = count
        json.dump(data, N1AKD)
        count += 1


    csv_file.close()
    N1AKD.close()
    N2AKD = open("/Users/MWK/Desktop/rdw/bios.json","r")
    N2AKD_READ = N2AKD.read()
    N2AKD_final = N2AKD_READ.replace("}", "},")
    N2AKD.close()
    N3AKD = open("/Users/MWK/Desktop/rdw/bios.json","w")
    N3AKD.writelines(N2AKD_final)
    N3AKD.writelines('{}]')
    N3AKD.close()
    N4AKD = open("/Users/MWK/Desktop/rdw/bios.json","r")
    N4AKD_READ = N4AKD.read()
    N4AKD_final = N4AKD_READ.replace(",{}", "")
    N4AKD.close()
    N5AKD = open("/Users/MWK/Desktop/rdw/bios.json","w")
    N5AKD.writelines(N4AKD_final)
    N5AKD.close()
    def sortFunction(value):
    	return value["year"]

    sortedStudents = sorted(json.loads(N4AKD_final), key=sortFunction)
    print(sortedStudents)
    from github import Github
    print("Pushing to Github")
    g = Github(os.getenv("git_access_token"))
    repo = g.get_repo("oliverwk/wttpknng")
    contents = repo.get_contents("bios.json")
    repo.update_file(contents.path, str(sortedStudents), "updated bios.json from python", contents.sha, branch="master")
    print("Pushed to Github")
multi_movie()
