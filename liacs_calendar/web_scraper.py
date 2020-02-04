import requests, time
from termcolor import cprint
from pprint import pprint
from bs4 import BeautifulSoup, Tag
from cache_to_disk import cache_to_disk, delete_disk_caches_for_function

CACHE_VALID_DAYS = 1
URL_BASE = "https://studiegids.universiteitleiden.nl/studies/"
MAJOR_URI = {
  "Informatica": "6901/informatica",
  "Bioinformatica": "7889/bioinformatica",
  "Informatica en Economie": "7887/informatica-economie",
}


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
  if not silent:
    print("Caching results of requests")
  return scrape_courses(major, year, semester)

def remove_courses_cache():
  """Remove cached results of scrape_courses_cached
  """
  delete_disk_caches_for_function("scrape_courses")

def scrape_courses(major: str, year: int, semester: int) -> dict:
  """Return a dictionary of all courses of a specific major, year, and semester.
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
  if major not in MAJOR_URI:
    raise ValueError(f"{major} is not in the list of majors")
  courses_and_codes = {}
  try:
    full_page = requests.get(URL_BASE + MAJOR_URI[major])
  except requests.ConnectionError:
    cprint("ERROR: Could not obtain course page. Are you connected to the internet?", 'red')
    raise
  if full_page.status_code == 404:
    cprint("ERROR: Course page URL was invalid. The website may have been updated, which breaks this tool :(", 'red')
    raise Exception("404: Page not found")
  soup = BeautifulSoup(full_page.content, 'html.parser')
  content_tables = soup("section", {"class": "tab"})
  # Table of courses for 'year'
  current_table = content_tables[year-1].find("tbody")
  all_rows = current_table.findAll("tr")
  for tr in all_rows:
    time.sleep(0.5)
    course = str(tr.find("a").string)
    link = tr.find("a")["href"]
    if course_in_semester(tr, semester):
      link = tr.find("a")["href"]
      print(f"Requesting page for {course}...")
      course_page = requests.get(link)
      course_soup = BeautifulSoup(course_page.content, 'html.parser')
      course_code = str(course_soup.find("aside").findAll("dd")[2].string)
      courses_and_codes[course] = course_code
  return courses_and_codes

if __name__ == "__main__":

  result = scrape_courses("Informatica", 1, 1)
  pprint(result)