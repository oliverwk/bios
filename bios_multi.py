import os
os.system('clear')
import threading
import requests, sys
from bs4 import BeautifulSoup
import csv, xlsxwriter
import json, datetime


urls = ["https://www.pathe.nl/bioscoop/utrechtleidscherijn?date=24-08-2020","https://www.pathe.nl/bioscoop/utrechtleidscherijn?date=25-08-2020","https://www.pathe.nl/bioscoop/utrechtleidscherijn?date=26-08-2020","https://www.pathe.nl/bioscoop/utrechtleidscherijn?date=27-08-2020","https://www.pathe.nl/bioscoop/utrechtleidscherijn?date=28-08-2020","https://www.pathe.nl/bioscoop/utrechtleidscherijn?date=29-08-2020","https://www.pathe.nl/bioscoop/utrechtleidscherijn?date=30-08-2020","https://www.pathe.nl/bioscoop/utrechtleidscherijn?date=31-08-2020"]

csv_file = open("/Users/MWK/Desktop/bios/bios.csv","w")
fieldnames = ['titel', 'Start tijd', 'img_url']
writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
writer.writeheader()
xlsx = '/Users/MWK/Desktop/bios/bios.xlsx'
workbook = xlsxwriter.Workbook(xlsx)
worksheet = workbook.add_worksheet()
N1AKD = open("/Users/MWK/Desktop/bios/bios.json","w")
jsonx = open("/Users/MWK/Desktop/bios/bios.json","w")

def do_shit(URL):
    print(URL)
    URL = "https://www.pathe.nl/bioscoop/utrechtleidscherijn"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.5 Safari/605.1.15'}
    page = requests.get(URL, headers=headers )
    soup = BeautifulSoup(page.content, 'html.parser')
    body = soup.find(id="js-cinema-schedule")
    N1AKD.writelines("[")
    items = body.find_all("div", class_="schedule-simple__item")
    count = 1
    datas=[]

    Naam = 0
    Start_tijd = 1
    img_url = 2

    for item in items:
        p_data = item.find("a", class_="poster")
        print("\n"+p_data["title"])
        start_times = item.find("span", class_="schedule-time__start")
        print("De film begint om: "+start_times.get_text())
        hd_img = p_data.find("img")
        print("\n"+hd_img["src"])
        worksheet.write(count, Naam, str(p_data["title"]))
        worksheet.write(count, Start_tijd, str(start_times.get_text()))
        worksheet.write(count, img_url, str(hd_img["src"]))
        writer.writerow({'titel': p_data["title"] , 'Start tijd': start_times.get_text(), 'img_url': hd_img["src"]})
        data = {}
        data["title"] = p_data["title"]
        data["tijd"] = start_times.get_text()
        data["img_url"] = hd_img["src"].replace(" ", "%20")
        data["id"] = count
        json.dumps(data)
        datas.append(data)
        count += 1




    def sortFunction(value):
    	return value["tijd"]

    sorteds = sorted(json.loads(str(datas).replace("'", '"')), key=sortFunction)

    jsonx.writelines(str(json.dumps(sorteds, indent=4)))



import time
start = time.time()



if __name__ == "__main__":
    threads = list()
    for URL in urls:
        print("Gemaakt Theard")
        x = threading.Thread(target=do_shit, args=(URL,))
        threads.append(x)
        x.start()

    for index, thread in enumerate(threads):
        print("Main    : before joining thread %d.", URL)
        thread.join()
        print("Main    : thread %d done", index)


end = time.time()
print("\n\n -- tijd hoelang het duurde -- \n")
print(end - start)
jsonx.close()
csv_file.close()
workbook.close()
N1AKD.close()
