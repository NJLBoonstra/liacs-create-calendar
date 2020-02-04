from . import (read_excel, get_course_entries, get_course_list, write_schedule, create_ical, create_calendar, __PROGRAM_DESCRIPTION__, web_scraper)
from termcolor import cprint
def cli():
    import argparse
    import sys

    arg_parser = argparse.ArgumentParser(description=__PROGRAM_DESCRIPTION__)

    arg_parser.add_argument("filename", type=str, 
                            help="Filename of the xls-schedule")
    arg_parser.add_argument("--courses", "-c", help="Single course name, or "
                            "comma separated list of courses", type=str,
                            required=False)
    arg_parser.add_argument("--list-courses", "-l", help="List courses (when you want to provide courses manually, e.g. a CSV-file, use this list)", 
                            action="store_true", dest="dolist", required=False)
    arg_parser.add_argument("--output", "-o", help="Output filename", type=str,
                            required=False, default="schedule.ical")
    arg_parser.add_argument("--study-programme", "-s", help="Study programme (for automatic web scraping). Format: {Major-name}_{Academic-year-start}_{Year-you-are-in}_{Semester}", 
                            type=str, required=False, dest="study_programme")
    arg_parser.add_argument("--list-programmes", "-L", help="List all available study programmes", action="store_true", dest="list_programmes", required=False)
    arg_parser.add_argument("--no-cache", "-N", help="Deletes the current cache and performs all study programme requests without caching", action="store_true", dest="no_cache", required=False)
    if len(sys.argv) < 2:
        arg_parser.print_help()
        exit(-1)

    args = arg_parser.parse_args()

    outputfile = "schedule.ical"

    if args.output:
        outputfile = args.output

    try:
        read_excel(args.filename)
    except Exception as err:
        print(err)
        exit(-1)

    if args.dolist:
        print("The following courses are available: ")
        courses = get_course_list()
        for course in courses:
            print(course)

    if args.courses:
        courses = args.courses.split(sep=",")
        clean_courses = []

        print("Creating iCal object with data for the following courses: ")
        for course in courses:
            #Remove preceding and trailing spaces, make lowercase
            clean_courses.append(course.strip().lower())
            print("* " + course.strip().lower())

        x = get_course_entries(clean_courses)

        cal = create_calendar()

        for course in x:
            create_ical(course[0], course[1], course[2], course[3], cal)

        write_schedule(outputfile, cal)

    if args.study_programme:
        try:
            parts = args.study_programme.split("_")
            print(parts)
            major = parts[0]
            uni_year = int(parts[1])
            year = int(parts[2])
            semester = int(parts[3])
        except:
            cprint("ERROR: Invalid format for study programme. Should be {Major-name}_{Academic-year-start}_{Year-you-are-in}_{Semester}", "red")
            print("Example:  `--study-programme Informatica_2019_2_1` for all courses of bachelor Informatica in the academic year 2019-2020, for a 2nd year student, first semester.")
            exit(-1)
        result = None
        if args.no_cache:
            print("Deleting current cache, not using any cached results, and not caching any results")
            web_scraper.delete_disk_caches_for_function("scrape_courses_cached")
            result = web_scraper.scrape_courses(major, uni_year, year, semester)
        else:
            result = web_scraper.scrape_courses_cached(major, uni_year, year, semester)
        print(result)
    if args.list_programmes:
        print("Available study programmes:")
        for programme in web_scraper.MAJOR_NAMES.keys():
            print(programme)