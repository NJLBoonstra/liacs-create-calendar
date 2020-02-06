from . import (read_excel, get_course_entries, get_course_list, write_schedule, create_ical, create_calendar, __PROGRAM_DESCRIPTION__, web_scraper)
from termcolor import cprint, colored
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
    arg_parser.add_argument("--exclude", "-e", help="Single course name to exclude,"
                            " or comma seperated list of courses to exclude", type=str,
                            required=False)
    arg_parser.add_argument("--study-programme", "-s", help="Use courses from a specific study programme (by web scraping). Format: {Major-name}_{Year}_{Semester}", 
                            type=str, required=False, dest="study_programme")
    arg_parser.add_argument("--list-programmes", "-L", help="List all available study programmes", action="store_true", dest="list_programmes", required=False)
    arg_parser.add_argument("--no-cache", "-N", help="Don't use the cache (request everything again)", action="store_true", dest="no_cache", required=False)
    arg_parser.add_argument("--delete-cache", "-D", help="Delete current cache for study programmes", action="store_true", dest="del_cache", required=False)
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

        if args.exclude:
            exclude = args.exclude.split(sep=",")
            clean_exclude = []
            
            print("And excluding the following courses: ")
            for ex in exclude:
                clean_exclude.append(ex.strip().lower())
                print("* " + ex.strip().lower())
            
            x = get_course_entries(clean_courses, exclude_names=clean_exclude)
        
        else:
            x = get_course_entries(clean_courses)

        cal = create_calendar()

        for course in x:
            create_ical(course[0], course[1], course[2], course[3], cal)

        write_schedule(outputfile, cal)

    if args.del_cache:
        print("Deleting cache...")
        web_scraper.delete_disk_caches_for_function("scrape_courses_cached")

    if args.study_programme:
        try:
            parts = args.study_programme.split("_")
            major = parts[0].upper()
            year = int(parts[1])
            semester = int(parts[2])
        except:
            cprint("ERROR: Invalid format for study programme", "red")
            print("Should be " + colored("{Major-name}_{Year}_{Semester}", "cyan"))
            print("Example: " + colored("--study-programme informatica_2_1", "cyan") + " for all courses of bachelor Informatica for a 2nd year student, first semester.")
            exit(-1)
        course_codes = None
        if args.no_cache:
            course_codes = web_scraper.scrape_courses(major, year, semester)
        else:
            course_codes = web_scraper.scrape_courses_cached(major, year, semester)
        print(course_codes)

    if args.list_programmes:
        print("Available study programmes:")
        for programme in web_scraper.MAJOR_NAMES.keys():
            print(programme.lower().capitalize())
