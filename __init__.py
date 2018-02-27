"""
Scraper for University of Queensland course and program data
"""

from .catalogue import Catalogue
from .course import Course, CourseSemestersOffered
from .plan import Plan
from .program import Program
from .semester import Semester, get_all_semesters, get_semester_by_name
from .assessment import Assessment
from .offering import Offering