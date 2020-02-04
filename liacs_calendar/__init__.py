__PROGRAM_DESCRIPTION__ = """Convert the LIACS xls schedule to an iCal for easy importation into your personal calendar.\n
                          
                          """
import sys

if sys.version_info < (3, 0):
    print("Need at least Python3")
    exit(-1)

#Only tested with this version
if sys.version_info <= (3, 6):
    print("This script may not function properly with Python versions lower than 3.6.")


from .read_schedule import get_course_list, read_excel, get_course_entries
from .create_icals import create_calendar, create_ical, write_schedule
from .cli import cli


if __name__ == "__main__":
    cli()




