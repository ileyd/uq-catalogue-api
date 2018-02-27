"""
Code relating to assessment tasks
"""

class Assessment:
  # course code the assessment is for
  course_code: str = ""
  # semester id the assessment is for
  semester_id: int = -1
  # profile id for the offering
  profile_id: int = -1

  # name of the assessment task
  name: str = ""
  # weighting of the assessment task
  weight: float = 0
  # compulsory hurdle?
  hurdle: bool = False
  # due date text
  due_text: str = ""

  def valid(self):
    """Whether the Assessment object represents a valid assessment piece"""
    return not (self.course_code == "" or self.semester_id < 6000 or self.profile_id < 1 or self.weight < 0 or self.weight > 1 or self.name == "")

  def __init__(self, course_code: str, semester_id: int, profile_id: int, name: str, weight: float, hurdle: bool = False, due_text: str = ""):
    if course_code == "":
      raise ValueError('Invalid course code provided')
    elif semester_id < 6000:
      raise ValueError('Invalid semester ID provided')
    elif profile_id < 1:
      raise ValueError('Invalid profile ID provided')
    elif name == "":
      raise ValueError('Empty assessment task name provided')
    elif not (0 <= weight <= 1):
      raise ValueError('Invalid assessment weight provided')
    else:
      self.course_code = course_code
      self.semester_id = semester_id
      self.profile_id = profile_id
      self.name = name
      self.weight = weight
      self.hurdle = hurdle
      self.due_text = due_text