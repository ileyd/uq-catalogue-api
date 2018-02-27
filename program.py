"""
Program scraper
"""
import re
from .helpers import get_soup
from typing import List


class Program:
  """A degree that the university offers
  """

  # program code -- i think its an int
  code: int = 0
  # program title
  title: str = ""
  # program level -- e.g. Bachelor, Bachelor Honours, etc
  level: str = ""
  # official abbreviation -- e.g. BBiomedSc
  abbreviation: str = ""
  # duration in years
  duration: float = 0
  # total unit value
  units: int = 0
  # list of plan IDs
  plans: list = []
  # courses for this program
  courses: List[str] = []
  # whether program object is valid
  valid_internal: bool = False

  def valid(self):
    self.valid_internal = not (self.code == "" or self.title == "" or self.duration <= 0 or self.units < 1)
    return self.valid_internal

  def __init__(self, code: str):
    self.code = code
    self.update()

  def update(self):
    """Update self based on information scraped from UQ
    """
    base_url = 'https://my.uq.edu.au/programs-courses/program.html?acad_prog={}'.format(str(self.code))
    soup = get_soup(base_url)

    self.title = soup.find(id="program-title").get_text()
    self.level = soup.find(id="program-title").get_text().split(' ')[0].lower()
    self.abbreviation = soup.find(id="program-abbreviation").get_text()
    self.duration = float(soup.find(id="program-domestic-duration").get_text()[0])
    self.units = int(soup.find(id="program-domestic-units").get_text())
    
    plans = soup.find_all('a', href=re.compile("acad_plan"))
    for plan in plans:
      plan_code = plan['href'][-10:]
      # title = plan.text
      self.plans.append(plan_code)
    
    alt_base_url = 'https://my.uq.edu.au/programs-courses/program_list.html?acad_prog={}'.format(self.code)
    alt_soup = get_soup(alt_base_url)

    courses = alt_soup.find_all("a", href=re.compile("course_code"))
    for course in courses:
      self.courses.append(course.get_text().strip())