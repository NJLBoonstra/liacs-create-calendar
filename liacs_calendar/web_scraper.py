import requests, time
from termcolor import cprint
from pprint import pprint
from bs4 import BeautifulSoup, Tag
from datetime import datetime
from cache_to_disk import cache_to_disk, delete_disk_caches_for_function

CACHE_VALID_DAYS = 1
BASE_URL = "https://studiegids.universiteitleiden.nl/search"
MAJOR_NAMES = {
  # Displayable name: search name
  "INFORMATICA": "Informatica",
  "INFORMATICA+KI": "Informatica: Variant Kunstmatige intelligentie",
  "BIOINFORMATICA": "Bioinformatica",
  "INFORMATICA+ECONOMIE": "Informatica & Economie",
}
ACADEMIC_YEAR = datetime.now().year
# 2020 before August is 2019-2020, after August is 2020-2021
if datetime.now().month < 8:
  ACADEMIC_YEAR -= 1


def course_in_semester(table_row: Tag, semester: int) -> bool:
  """Check whether the course of this table_row is in the selected semester
  """
  blocks = table_row.find_all("span", {"class", "block"})
  for block in blocks:
    classes = block["class"]
    if semester == 1 and ("block-1" in classes or "block-2" in classes):
      if "block-on" in classes:
        return True
    elif semester == 2 and ("block-3" in classes or "block-4" in classes): 
      if "block-on" in classes:
        return True
  return False

@cache_to_disk(CACHE_VALID_DAYS)
def scrape_courses_cached(major: str, year: int, semester: int, silent=False):
  """Same as scrape_courses, but results are cached to the disk for CACHE_VALID_DAYS days.
  """
  result = scrape_courses(major, year, semester)
  if not silent:
    print("Caching results of requests...")
  return result

def remove_courses_cache():
  """Remove cached results of scrape_courses_cached
  """
  delete_disk_caches_for_function("scrape_courses_cached")

def scrape_courses(major: str, year: int, semester: int, silent=False) -> dict:
  """Return a dictionary of all courses of of a specific major, year (1~3), and semester.
  Example for scrape_courses('Informatica', 1, 1):
  {
    'Continue Wiskunde 1': '4031CW103',
    'Fundamentals of Digital Systems Design': '4031FDSD6',
    'Fundamentele Informatica 1': '4031FINF1',
    'Linear Algebra for Computer Scientists 1': '4031LACS1',
    'Oriëntatie Informatica': '4031ORINC',
    'Programmeermethoden': '4031PRGR6',
    'Studying and Presenting': '4031STPEV'
  }
  """
  if major not in MAJOR_NAMES:
    raise ValueError(f"{major} is not in the list of majors")
  courses_and_codes = {}
  if not silent:
    print(f"Searching for URL to {ACADEMIC_YEAR}-{ACADEMIC_YEAR+1} {major}...")
  try:
    search_query = requests.get(BASE_URL, params={
      "for": "programmes",
      "q": MAJOR_NAMES[major],
      "edition": f"{ACADEMIC_YEAR}-{ACADEMIC_YEAR+1}"
    })
    if search_query.status_code == 404:
      cprint("ERROR: Course page URL was invalid. The website may have been updated, which breaks this tool :(", 'red')
      raise Exception("404: Page not found")
    search_soup = BeautifulSoup(search_query.content, 'html.parser')
    full_page_url = search_soup.findAll("a", string=MAJOR_NAMES[major])[1]["href"]
    if not silent:
      print("Found URL: " + full_page_url)
    full_page = requests.get(full_page_url)
  except requests.ConnectionError:
    cprint("ERROR: Could not obtain course page. Are you connected to the internet?", 'red')
    raise
  soup = BeautifulSoup(full_page.content, 'html.parser')
  content_tables = soup("section", {"class": "tab"})
  # Table of courses for 'year'
  current_table = content_tables[year-1].find("tbody")
  all_rows = current_table.findAll("tr")
  for tr in all_rows:
    time.sleep(0.5)
    if course_in_semester(tr, semester):
      link = tr.find("a")["href"]
      course = str(tr.find("a").string)
      link = tr.find("a")["href"]
      if not silent:
        print(f"Requesting page for {course}...")
      course_page = requests.get(link)
      course_soup = BeautifulSoup(course_page.content, 'html.parser')
      course_code = str(course_soup.find("aside").findAll("dd")[2].string)
      courses_and_codes[course] = course_code
  return courses_and_codes

if __name__ == "__main__":
  result = scrape_courses("Informatica", 1, 1)
  pprint(result)