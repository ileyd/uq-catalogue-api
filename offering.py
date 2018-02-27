"""
Code relating to offerings: specific instances of courses in a particular semester
"""
from .semester import Semester
from .course import Course, CourseSemestersOffered
from .assessment import Assessment
from .helpers import get_soup
from lxml import html, etree
from html.parser import HTMLParser
from typing import List
import requests


def valid_percentage(percentage: float):
  return 0 <= percentage <= 1


def vp(percentage: float):
  return valid_percentage(percentage)


class OfferingCutoffs:
  """Describes the cut offs for each mark for a particular Offering"""
  one: float = 0.00
  two: float = 0.30
  three: float = 0.45
  four: float = 0.50
  five: float = 0.65
  six: float = 0.75
  seven: float = 0.85

  def valid(self):
    """Whether the OfferingCutoffs object represents valid cutoffs"""
    sane = self.one < self.two < self.three < self.four < self.five < self.six < self.seven
    valid = vp(self.one) and vp(self.two) and vp(self.three) and vp(
        self.four) and vp(self.five) and vp(self.six) and vp(self.seven)
    return sane and valid

  def __init__(self, one: float = 0.00, two: float = 0.30, three: float = 0.45, four: float = 0.50, five: float = 0.65, six: float = 0.75, seven: float = 0.85):
    if not (vp(one) and vp(two) and vp(three) and vp(four) and vp(five) and vp(six) and vp(seven) and one < two < three < four < five < six < seven):
      raise ValueError(
          'An invalid cutoff has been provided that is outside the range of 0 to 1.')
    else:
      self.one = one
      self.two = two
      self.three = three
      self.four = four
      self.five = five
      self.six = six
      self.seven = seven


class Offering:
  # code of the course the offering relates to
  course_code: str = ""
  # id of the semester the offering relates to
  semester_id: int = -1
  # not sure what this is exactly
  linear: bool = True
  # not sure what this is exactly
  calculable: bool = True
  # not sure what this is exactly
  message: str = ""
  # cutoffs for each mark
  cutoffs: OfferingCutoffs = OfferingCutoffs()
  # id for the course profile
  profile_id: int = -1
  # assessment for this offering
  assessment: List[Assessment] = []

  def semester(self):
    """Returns a Semester object for the semester this Offering corresponds to"""
    return Semester(self.semester_id)

  def course(self):
    """Returns a Course object for the course this Offering corresponds to"""
    return Course(self.course_code)

  def __init__(self, course_code: str, semester_id: int, profile_id: int):
    if course_code == '':
      raise ValueError('Empty course code provided')
    elif semester_id < 6000:
      raise ValueError('Invalid semester ID provided')
    elif profile_id < 1:
      raise ValueError('Invalid profile ID provided')
    else:
      self.course_code = course_code
      self.semester_id = semester_id
      self.profile_id = profile_id
      self.update()

  def update(self):
    """Updates self based on information scraped from UQ"""
    profile_url = 'http://www.courses.uq.edu.au/student_section_loader.php?profileId={}&section={}'
    profile_url_5 = profile_url.format(self.profile_id, 5)
    soup_5 = get_soup(profile_url_5)

    assessment_table = soup_5.find('table', attrs={'class':'tblborder'})
    assessment_tasks = []
    assessment_table_rows = assessment_table.find_all('tr')
    for row in assessment_table_rows:
      cols = row.find_all('td')
      cols = [ele.text.strip() for ele in cols]
      assessment_tasks.append([ele for ele in cols if ele])

    if len(assessment_tasks) < 1:
      # TODO implement more specific error
      print("ATASKS:")
      print(assessment_tasks)
      raise ValueError('Invalid course profile')

    self.assessment = []
    for atask in assessment_tasks[1:]:
      hurdle = False
      if 'hurdle' in atask[2].lower():
        hurdle = True
      weight = float(atask[2].split('%')[0]) / 100
      ass = Assessment(course_code=self.course_code, semester_id=self.semester_id,
                       profile_id=self.profile_id, name=atask[0], weight=weight, hurdle=hurdle, due_text=atask[1])
      self.assessment.append(ass)
