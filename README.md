**Note**: Due to Leiden University *finally* implementing MyTimeTable, this project is now obsolete.

# liacs-create-calendar

The schedules provided by the LIACS are either in PDF format, or in a very large Excel (.xls) sheet. However, class locations are not included in these PDFs, meaning that if one wants to add all classes to one's personal calendar, all locations have to be looked up in this large, sheet. As this is something that repeats itself every semester, automating this process is only a logical thing to do.

In order to fulfill this goal, this Python Package was created. It takes the Excel sheet, and given a list of courses, it will create an iCal file that contains all classes and tests.

## Usage

First, make sure all dependencies are installed. These are:

* Python3 and pip

    Can be installed via `sudo apt install python3 python3-pip` on Ubuntu/Debian

* icalendar and xlrd packages

    A requirements file is included, which can be read by pip:
    `sudo pip3 -r requirements.txt`


In order to use this package, the latest version of the schedule Excel sheet is needed. This can be downloaded via [the faculty website](https://www.student.universiteitleiden.nl/studie-en-studeren/studie/onderwijsinformatie/roosters/wiskunde-en-natuurwetenschappen/informatica-bsc?cf=wiskunde-en-natuurwetenschappen&cd=informatica-bsc#tab-2)

When all dependencies are satisfied, one can retrieve a list of all courses available in the sheet as follows `python3 liacs-create-calendar.py file.xls -l`

### Creating the iCal

To make it easier to create the iCal for the courses you want, the `-c`/`--courses` argument accepts a comma-separated list of prefixes. For example, the activities for the course `Complexiteit` are as follows:
* `Complexiteit -HG`
* `Complexiteit -WC`
* `Complexiteit 6 EC TEN`

To fetch all activities for this course, simply use `python3 liacs-create-calendar.py file.xls -c"complex"`. The double ticks are not necessary, but allow for spaces in the list. For example, `-c complex,Cont. Wisk` is not valid, whereas `-c "complex, Cont. Wisk." ` is.


