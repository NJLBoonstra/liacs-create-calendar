from . import (read_excel, get_course_entries, get_course_list, write_schedule, create_ical, create_calendar, __PROGRAM_DESCRIPTION__)

def cli():
    import argparse
    import sys

    arg_parser = argparse.ArgumentParser(description=__PROGRAM_DESCRIPTION__)

    arg_parser.add_argument("filename", type=str, 
                            help="Filename of the xls-schedule")
    arg_parser.add_argument("--courses", "-c", help="Single course name, or "
                            "comma separated list of courses", type=str,
                            required=False)
    arg_parser.add_argument("--list-courses", "-l", help="List courses", 
                            action="store_true", dest="dolist", required=False)
    arg_parser.add_argument("--output", "-o", help="Output filename", type=str,
                            required=False, default="schedule.ical")
    arg_parser.add_argument("--exclude", "-e", help="Single course name to exclude,"
                            " or comma seperated list of courses to exclude", type=str,
                            required=False)

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

        
