import os
import git
import requests
import webbrowser
import concurrent.futures
from bs4 import BeautifulSoup

from config import name, group


def is_branch_up_to_date(branch_name):
    repo = git.Repo('.')
    remote = repo.remote()
    remote.fetch()
    local_commit = repo.rev_parse(branch_name)
    remote_commit = repo.rev_parse(f'origin/{branch_name}')
    return local_commit == remote_commit


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
def get_tablerow(url, name, osname):
	soup = get_soup(url)
	print(f"----Processing table for {osname}----")
	header = soup.find("tr")
	if header == None:
		raise Exception("Unknown exception, couldn't find rows in table")

	td = soup.find('td', string=name)
	if td == None or td.find_parent('tr') == None: 
		raise NotFoundStudentException(name, url)
		
	return f"<table><tbody>{header}{td.find_parent('tr')}</tbody></table>"

def get_logtable(url, name, group, osname):
	soup = get_soup(url)
	print(f"----Processing logs for {osname}----")
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

def gen_tables_for_os(os):
	html = ""
	table_url = f"https://www.kgeorgiy.info/upload/prog-intro/{os}/table.html"
	log_url = f"https://www.kgeorgiy.info/upload/prog-intro/{os}/logs.html"

	print(f"====Processing {os}====")
	html += f"<h1>{os}</h1>"
	
	with concurrent.futures.ThreadPoolExecutor() as executor:
		table_future = executor.submit(get_tablerow, table_url, name, os)
		log_future = executor.submit(get_logtable, log_url, name, group, os)
		table = table_future.result()
		log = log_future.result()

	html += "<h3>table</h3>"
	html += table

	html += "<h3>log</h3>"
	html += log

	return html


def gen_page():
	html = "<!DOCTYPE html><html><head><link rel=\"stylesheet\" href=\"output.css\"><meta charset=\"UTF-8\"></head><body>"

	if not is_branch_up_to_date("master"):
		html += "<h1>New version published. And your local branch is behind. Pull the latest changes.</h1>"

	with concurrent.futures.ThreadPoolExecutor() as executor:
		results = executor.map(gen_tables_for_os, OSES)
		for result in results:
			html += result
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

# test)