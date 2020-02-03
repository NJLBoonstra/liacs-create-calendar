__PROGRAM_DESCRIPTION__ = ("Convert the LIACS xls schedule to an iCal for "
                          "easy importation into your personal calendar \n"
                          "If no courses are provided, the whole xls will be "
                          "converted into an iCal file. \n"
                          "")

from .read_schedule import get_course_list, read_excel, get_course_entries
from .create_icals import create_calendar, create_ical, write_schedule
from .cli import cli

import sys

if sys.version_info <= (3, 6):
    print("This script may not function properly with Python versions lower than 3.6.")

if __name__ == "__main__":
    cli()




