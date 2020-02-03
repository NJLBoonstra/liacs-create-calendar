"""
    The functions that are needed to read the Excel-file and process it into
    Python understandable objects.
"""
from os import path
from datetime import timezone, datetime, timedelta, time, date

try:
    import xlrd
except ImportError:
    print("Please install all dependencies using `pip install -r requirements.txt`")
    exit(-1)


__raw_data__ = []

def read_excel(f: str) -> list:
    """Read an Excel file (xls) and process all the content into a list.

    :param f: Filename of the file to process. It helps if this is an 
    absolute path.
    :type f: str
    :returns: A list containing all entries of the xls
    :rtype: list

    """
    #Do some sanity checks first
    if type(f) is not str:
        raise TypeError("Parameter file of function read_excel must be str, but was {}".format(str(type(f))))

    if not path.exists(f) or not path.isfile(f):
        raise ValueError("Given file ({}) does not exist, or is not a file.".format(f))

    #Open the wb
    wb = xlrd.open_workbook(filename=f, on_demand=True, formatting_info=True)
    xf = wb.xf_list
    font = wb.font_list
    sheet = wb.sheet_by_index(0)
    do_add = True

    return_list = []

    for r in range(sheet.nrows):
        #Add new row in list
        row_result_list = []
        do_add = True
        for c in range(sheet.row_len(r)):
            if not do_add:
                break

            cell = sheet.cell(r,c)

            curr_xf = xf[cell.xf_index]
            curr_font = font[curr_xf.font_index]

            #skip cells with text struck out
            if curr_font.struck_out:
                do_add = False
                

            if cell.ctype == xlrd.XL_CELL_DATE:
                cell_val = xlrd.xldate.xldate_as_tuple(cell.value, 0)
            else:
                cell_val = cell.value

            row_result_list.append(cell_val)

        if do_add:
            return_list.append(row_result_list)
    global __raw_data__
    __raw_data__ = return_list

    return return_list

def get_course_entries(course_names: list, data: list = []) -> list:
    if not course_names or type(course_names) is not list:
        raise TypeError("Parameter course_name must be a list and may not be an empty list!")
    
    global __raw_data__
    if not __raw_data__ and not data:
        raise RuntimeError("Please either run read_excel, or provide data in the data parameter")

    if data:
        d = data
    else:
        d = __raw_data__

    header = d[0]

    #I'm only interested in these entries
    entry_date = None
    entry_sttime = None
    entry_endtime = None
    entry_building = None
    entry_room = None
    entry_activity = None

    #Find which column corresponds to what
    i = 0
    for h in header:
        #switch stmt would be nice here
        curr_entry = h.lower()
        if curr_entry == "date":
            entry_date = i
        elif curr_entry == "starttime":
            entry_sttime = i
        elif curr_entry == "endtime":
            entry_endtime = i
        elif curr_entry == "building":
            entry_building = i
        elif curr_entry == "room":
            entry_room = i
        elif curr_entry == "activity":
            entry_activity = i
        i = i + 1

    if not entry_activity:
        raise ValueError("Could not find the column containing the activity. This is necessary.")
        
    tzone = timezone(timedelta(hours=1), name="Europe/Amsterdam")

    result = []

    i = 0
    for entry in d[1:]:
        act_date = None
        d = None
        starttime = None
        endtime = None
        dstart = None
        dend = None
        location = ""
        activity = entry[entry_activity].lower()

        #skip all processing if course is not in list
        do_process = False
        for course in course_names:
            if activity.startswith(course):
                do_process = True
                break
        
        if not do_process:
            continue

        i = i + 1

        if entry_date:
            act_date = entry[entry_date]
            d = date(act_date[0], act_date[1], act_date[2])

        if entry_sttime:
            st = entry[entry_sttime]

            if type(st) is tuple:
                starttime = time(st[3], st[4])
            else:
                try:
                    st = st.split(":")
                    starttime = time(int(st[0]), int(st[1]))
                except:
                    print(entry[entry_sttime])
            # starttime = time.fromisoformat(entry[entry_sttime])
        if entry_endtime:
            et = entry[entry_endtime]

            if type(et) is tuple:
                endtime = time(et[3], et[4])
            else:
                try:
                    et = et.split(":")
                    endtime = time(int(et[0]), int(et[1]))
                except:
                    print(entry[entry_endtime])
                
            # endtime = time.fromisoformat(entry[entry_endtime])

        if d and starttime:
            dstart = datetime.combine(d, starttime, tzinfo=tzone)
        
        if d and endtime:
            dend = datetime.combine(d, endtime, tzinfo=tzone)

        if entry_building:
            location = str(entry[entry_building])

        if entry_room:
            location = location + " " + str(entry[entry_room])

        print("Found {} entries.".format(i), end="\r")
        
        result.append([activity, dstart, dend, location])

    print("Found {} entries. Done.".format(i))
    return result 


def get_course_list(data: list = []) -> list:
    global __raw_data__
    if not __raw_data__ and not data:
        raise RuntimeError("Please either run read_excel, or provide data in the data parameter")

    #Here we can safely assume either data or raw_data is used
    if data:
        d = data
    else:
        d = __raw_data__

    #Find the column in which the activity name is stored
    #Most likely in 9th column, so try that first
    col_activity = -1
    if str(d[0][9]).lower() == "activity":
        col_activity = 9
    else:
        for i in len(d[0]):
            if str(i).lower() == "activity":
                #Found it, stop
                col_activity = i
                break

    course_list = set()
    #Skip first row, for it is the header row
    for row in range(1, len(d)):
        # if d[row][col_activity] not in course_list:
        entry = d[row][col_activity]
        if "-" in entry:
            split_entry = entry.split("-")
            entry = split_entry[0].strip() + " - " + split_entry[1].strip()
        course_list.add(entry)

    return list(course_list)
