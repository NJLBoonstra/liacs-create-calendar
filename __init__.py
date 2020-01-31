__PROGRAM_DESCRIPTION__ = ("Convert the LIACS xls schedule to an iCal for "
                          "easy importation into your personal calendar \n"
                          "If no courses are provided, the whole xls will be "
                          "converted into an iCal file. \n"
                          "")

from read_schedule import get_course_list, read_excel

if __name__ == "__main__":
    import argparse

    arg_parser = argparse.ArgumentParser(description=__PROGRAM_DESCRIPTION__)

    arg_parser.add_argument("filename", type=str, 
                            help="Filename of the xls-schedule", required=True)
    arg_parser.add_argument("--courses", "-c", help="Single course name, or "
                            "comma separated list of courses", type=str,
                            required=False)
    arg_parser.add_argument("--list-courses", "-l", help="List courses", 
                            action="store_true", dest="dolist", required=False)

    args = arg_parser.parse_args()

    try:
        read_excel(args.filename)
    except Exception as err:
        print(err)
        exit(-1)

    if args.dolist:
        print("The following courses are available: ")
        courses = get_courses()
        for course in courses:
            print(course)


