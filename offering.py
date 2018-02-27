"""
Code relating to offerings: specific instances of courses in a particular semester
"""
from .semester import Semester
from .course import Course, CourseSemestersOffered
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
    valid = vp(self.one) and vp(self.two) and vp(self.three) and vp(self.four) and vp(self.five) and vp(self.six) and vp(self.seven)
    return sane and valid

  def __init__(self, one: float = 0.00, two: float = 0.30, three: float = 0.45, four: float = 0.50, five: float = 0.65, six: float = 0.75, seven: float = 0.85):
    if not (vp(one) and vp(two) and vp(three) and vp(four) and vp(five) and vp(six) and vp(seven) and one < two < three < four < five < six < seven):
      raise ValueError('An invalid cutoff has been provided that is outside the range of 0 to 1.')
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

  def semester(self):
    """Returns a Semester object for the semester this Offering corresponds to"""
    return Semester(self.semester_id)

  def course(self):
    """Returns a Course object for the course this Offering corresponds to"""
    return Course(self.course_code)

