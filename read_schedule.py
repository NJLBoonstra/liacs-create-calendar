"""
    The functions that are needed to read the Excel-file and process it into
    Python understandable objects.
"""
from os import path

try:
    import xlrd
except ImportError:
    print("Please install xlrd (pip install xlrd).")
    exit(-1)


__raw_data__ = []

def read_excel(f: str) -> list:
    """Read an Excel file (xls) and process all the content into a list.

    :param f: Filename of the file to process. It helps if this is an 
    absolute path.
    :type f: str


    """
    #Do some sanity checks first
    if type(f) is not str:
        raise TypeError("Parameter file of function read_excel must be str, but was {}".format(str(type(f))))

    if not path.exists(f) or not path.isfile(f):
        raise ValueError("Given file ({}) does not exist, or is not a file.".format(f))

    #Open the wb
    wb = xlrd.open_workbook(filename=f, on_demand=True)
    sheet = wb.sheet_by_index(0)

    return_list = []

    for r in range(sheet.nrows):
        #Add new row in list
        row_result_list = []
        for c in range(sheet.row_len(r)):
            cell = sheet.cell(r,c)

            if cell.ctype == xlrd.XL_CELL_DATE:
                cell_val = xlrd.xldate.xldate_as_tuple(cell.value, 0)
            else:
                cell_val = cell.value

            row_result_list.append(cell_val)

        return_list.append(row_result_list)
    global __raw_data__
    __raw_data__ = return_list

    return return_list

def get_course_entries(course_name: str, data: list = []) ->list:
    if type(course_name) is not str or len()
    global __raw_data__
    if not __raw_data__ and not data:
        raise RuntimeError("Please either run read_excel, or provide data in the data parameter")

    if data:
        d = data
    else:
        d = __raw_data__

    

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

    course_list = []
    #Skip first row, for it is the header row
    for row in range(1, len(d)):
        if d[row][col_activity] not in course_list:
            course_list.append(d[row][col_activity])

    return course_list

