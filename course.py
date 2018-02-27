"""
Course scraper
"""
import helpers as helpers
from typing import List

class CourseSemestersOffered:
  """An object describing which semesters a course is offered in
  """
  one: bool = False
  two: bool = False
  summer: bool = False

  # init with appropriate values
  def __init__(self, one: bool, two: bool, summer: bool):
    self.one = one
    self.two = two
    self.summer = summer

  # whether course is offered at all
  def offered(self):
    return self.one or self.two or self.summer

  # string representation
  def __str__(self):
    # for brevity
    one = self.one
    two = self.two
    summer = self.summer

    if one and two and summer:
      return "This course is offered in semester one, semester two, and the summer semester."
    elif one and two and not summer:
      return "This course is offered in semester one and semester two."
    elif one and not two and not summer:
      return "This course is offered in semester one."
    elif not one and two and not summer:
      return "This course is offered in semester two."
    elif not one and not two and summer:
      return "This course is offered in the summer semester."
    elif one and not two and summer:
      return "This course is offered in semester one and the summer semester."
    elif not one and two and summer:
      return "This course is offered in semester two and the summer semester."
    elif not one and not two and not summer:
      return "This course is not offered in any semester."

class Course:
  """
  A subject that is offered by the university
  """

  # whether the course is valid
  valid_internal: bool = False
  # 8 character course code of form ABCD1234
  code: str = ""
  # name of course
  title: str = ""
  # description of course
  description: str = ""
  # unit value of the course
  units: int = 0
  # which semesters course is offered in
  semesters_offered: CourseSemestersOffered = CourseSemestersOffered(False, False, False)
  # which course codes are prerequisites for this course
  prerequisites: List[str] = []
  # which course codes are incompatible with this course
  incompatibilities: List[str] = []
  # which programs this course is restricted to
  restricted: List[str] = []

  # whether the course is valid
  def valid(self):
    """Whether the course object represents a valid course
    
    Returns:
      bool -- whether the course is valid
    """

    self.valid_internal = not (self.code == "" or self.title == "" or self.units < 1)
    return self.valid_internal

  # init based on course code with rest populated by scraping
  def __init__(self, code: str):
    if code == "":
      raise ValueError("The course code cannot be empty.")
    else:
      self.code = code
      self.update()

  # update self based on information scraped from UQ
  def update(self):
    """Updates self based on information scraped from UQ
    """
    base_url = 'http://www.uq.edu.au/study/course.html?course_code={}'.format(self.code)
    soup = helpers.get_soup(base_url)

    if soup is None or soup.find(id="course-notfound"):
      return None

    description = soup.find(
      id="course-summary").get_text().replace('"', '').replace("'", "''")
    # apparent edge case; see STAT2203
    if '\n' in description:
      description = description.split('\n')[0]
    self.description = description

    self.title = soup.find(id="course-title").get_text()[:-11].replace("'","''")
    self.units = int(soup.find(id="course-units").get_text())

    try:
      raw_prerequisites = soup.find(id="course-prerequisites").get_text()
      print("Raw prerequisites for {} are {}".format(self.code, raw_prerequisites))
      # TODO parse this
    except AttributeError:
      raw_prerequisites = None

    try:
      self.incompatibilities = soup.find(id="course-incompatible").get_text()\
            .replace(' and ', ', ') \
            .replace(' or ', ', ') \
            .replace(' & ', ', ') \
            .replace('; ', ', ') \
            .split(', ')
    except AttributeError:
      self.incompatibilities = []

    try:
      restricted = soup.find(id="course-restricted").get_text()\
            .replace(' and ', ', ') \
            .replace(' or ', ', ') \
            .replace(' & ', ', ') \
            .replace('; ', ', ') \
            .split(', ')
      self.restricted = restricted
    except AttributeError:
      self.restricted = []

    semester_offerings = str(soup.find_all(id="course-current-offerings"))
    sem_one = False
    sem_two = False
    sem_sum = False
    if "Semester 1, " in semester_offerings:
      sem_one = True
    if "Semester 2, " in semester_offerings:
      sem_two = True
    if "Summer Semester, " in semester_offerings:
      sem_sum = True
    self.semesters_offered = CourseSemestersOffered(sem_one, sem_two, sem_sum)