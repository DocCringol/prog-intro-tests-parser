import os
import requests
import webbrowser
from bs4 import BeautifulSoup

from config import name, group


class NotFoundStudentException(Exception):
	def __init__(self, name, url):
		self.name = name
		self.url = url
		self.message = f"Error: Unable to find student {name} in a table in {url}"
		super().__init__(self.message)


def get_soup(url):
	response = requests.get(url)
	if response.status_code == 200:
		response.encoding = "utf-8"
		return BeautifulSoup(response.text, 'html.parser')
	else:
		raise Exception(f"Error: Unable to retrieve content from {url}. Status code: {response.status_code}")

# TODO remove name and group from table
def get_tablerow(url, name) :
	soup = get_soup(url)
	header = soup.find("tr")
	if header == None:
		raise Exception("Uknnown exxception, couldn't find rows in table")

	td = soup.find('td', string=name)
	if td == None or td.find_parent('tr') == None: 
		raise NotFoundStudentException(name, url)
		
	return f"<table><tbody>{header}{td.find_parent('tr')}</tbody></table>"

def get_logtable(url, name, group) :
	soup = get_soup(url)
	header = f"{name} ({group})"
	stripped_url = os.path.dirname(url) + "/"
	result = ""

	table_rows = soup.body.table.find_all("tr")

	i = 0
	th = None
	while th == None:
		if i >= len(table_rows):
			raise NotFoundStudentException(name, url)
		tr = table_rows[i]
		th = tr.find("th", string=header)
		i += 1

	th = None
	while th == None and i < len(table_rows):
		tr = table_rows[i]
		th = tr.find("th")
		if th == None:
			a = tr.find("a")
			if a != None:
				a["href"] = stripped_url + a["href"]
			result += str(tr)
		i += 1

	return f"<table><tbody>{result}</table></tbody>"


def gen_page():
	html = "<!DOCTYPE html><html><head><link rel=\"stylesheet\" href=\"output.css\"></head><body>"
	for os in OSES:
		table_url = f"https://www.kgeorgiy.info/upload/prog-intro/{os}/table.html"
		log_url = f"https://www.kgeorgiy.info/upload/prog-intro/{os}/logs.html"

		print(f"----{os}----")
		html += f"<h1>{os}</h1>"

		print("TABLE")
		html += "<h3>table</h3>"
		table = get_tablerow(table_url, name)
		# print(table)
		html += table

		print("LOG")
		html += "<h3>log</h3>"
		log = get_logtable(log_url, name, group)
		# print(log)
		html += log
	html += "</body></html>"
	return html


def main():
	html = gen_page()

	css = "td, th {\n\tborder: 1px solid;\n}"
	with open("output.css", "w", encoding="UTF-8") as css_file:
		css_file.write(css)
	
	with open("output.html", "w", encoding="UTF-8") as html_file:
		html_file.write(html)

	webbrowser.open_new_tab("output.html")


OSES = [
	"linux",
	"windows",
	"macos"
]

if __name__ == "__main__":
	main()