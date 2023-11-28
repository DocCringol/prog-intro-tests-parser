import json
import requests
from bs4 import BeautifulSoup

def get_soup(url):
	response = requests.get(url)
	if response.status_code == 200:
		response.encoding = "utf-8"
		return BeautifulSoup(response.text, 'html.parser')
	else:
		raise Exception(f"Error: Unable to retrieve content from {url}. Status code: {response.status_code}")

soup = get_soup(f"https://www.kgeorgiy.info/upload/prog-intro/linux/logs.html")

headers = soup.body.table.find_all("th")

d = dict()
for th in headers:
	s = th.string
	num = s.find("(")
	name = s[:num-1]
	group = s[num+1:num+6]
	d[name] = group

with open("names.json", "w", encoding="utf-8") as outfile: 
    json.dump(d, outfile, ensure_ascii=False)