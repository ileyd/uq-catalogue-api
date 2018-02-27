"""
Code to scrape University of Queensland program (degree) plan information
"""
import re
from .helpers import get_soup
from typing import List


class Plan:
  """A plan for certain courses to be completed in a program (degree)
  """
  # plan code -- i think it might be an int
  code: str = ""
  # plan title
  title: str = ""
  # program code plan is for -- i think it might be an int
  program: str = ""
  # course list for plan
  courses: List[str] = []
  # plan rules
  rules: List[str] = []
  # whether plan is valid
  valid_internal: bool = False

  def valid(self):
    self.valid_internal = not (self.code == "" or self.title == "" or self.program == "")
    return self.valid_internal

  def __init__(self, code: str):
    if code == "":
      raise ValueError("Plan code cannot be empty.")
    else:
      self.update()

  def update(self, title: str = "NOT IMPLEMENTED"):
    """Updates self based on information scraped from UQ
    """
    base_url = 'https://my.uq.edu.au/programs-courses/plan.html?acad_plan={}'.format(self.code)
    soup = get_soup(base_url)

    self.title = title
    self.program = soup.find(id="plan-field-key").get_text()
    
    alt_base_url = 'https://my.uq.edu.au/programs-courses/plan_display.html?acad_plan={}'.format(self.code)
    alt_soup = get_soup(alt_base_url)

    courses = alt_soup.find_all("a", href=re.compile("course_code"))
    for course in courses:
      course_code = course.get_text().strip()
      if course_code not in self.courses:
        self.courses.append(course_code)

    # rules = soup.find_all("div", "courselist")

    # for section in raw_rules:
    #     rsoup = BeautifulSoup(str(section), "html.parser")
    #     rule = {
    #         'text': rsoup.find("p").get_text().strip().replace('\n', '<br>'),
    #         'courses': []
    #     }

    #     raw_courses = rsoup.find_all("a", href=re.compile("course_code"))
    #     for raw_course in raw_courses:
    #         rule['courses'].append(raw_course.get_text().strip())

    #     if len(rule['text']) != 0 and len(rule['courses']) != 0:
    #         plan_rules['rules'].append(rule)