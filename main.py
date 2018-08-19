import csv

def import_data(csv_file):
    """Import a csv-file and present it as a table.  
    The function returns [] if the table is empty, or if it cannot locate the file.  
    
    Keyword arguments:  
    csv_file -> the name of the file that is to be imported."""

    try:
        with open(csv_file, 'r') as csvfile:
            reader = csv.reader(csvfile)
            table = [[e for e in r] for r in reader]
            while [] in table:
                table.remove([])
        return table
    except FileNotFoundError:
        print("ERROR: The program called a file that did not exist: {} does not appear to exist.".format(csv_file))
        return []

def save(table,csv_file):
    """Write a table to a given file, effectively overwriting the file's previous contents."""

    with open(csv_file, 'w') as csvfile:
        writer = csv.writer(csvfile)
        for r in table:
            if r:
                writer.writerow(r)

def check_for_int(s):
    """Check if a value can be converted to an integer. The function returns a boolean."""
    try:
        int(s)
        return True
    except ValueError:
        return False

def ask_for_value(value):
    """Asks for a number between 0 and 10 (boundaries included) from the user."""
    answer = -1
    while answer < 0 or answer > 10:
        request = input("On a scale from 0 to 10, how much priority does '{}' have? ".format(value))
        if check_for_int(request):
            answer = int(request)
    return answer

def in_table(row,table):
    for table_row in table:
        if row[0] == table_row[0]:
            if row[1] == table_row[1]:
                if row[2] == table_row[2]:
                    return True
    return False

def update_progress(input_file,progress_file):
    progress = import_data(progress_file)

    updates = 0
    for row in import_data(input_file):
        if not in_table(row,progress):
            progress.append(row)
            updates += 1
    if updates > 0:
        s = ''
        if updates > 1:
            s = 's'
        print('{} new column{} detected! They have been added to the table.'.format(updates,s))
    save(progress,progress_file)

def main(input_file,progress_file,output_file):
    update_progress(input_file,progress_file)

    category_1 = []
    category_2 = []
    category_3 = []
    progress = import_data(progress_file)

    for row in progress:
        if row != progress[0]:
            if row[0] not in category_1:
                category_1.append(row[0])
            if row[1] not in category_2:
                category_2.append(row[1])
            if row[2] not in category_3:
                category_3.append(row[2])
    
    priorities = [[0,row[0],row[1],row[2],row[3],row[4]] for row in progress]
    priorities[0][0] = 31

    print('=======================================')
    for category in category_1:
        priority = ask_for_value(category)
        for task in priorities:
            if task[1] == category:
                task[0] += priority
    
    print('=======================================')
    for category in category_2:
        priority = ask_for_value(category)
        for task in priorities:
            if task[2] == category:
                task[0] += priority
    
    print('=======================================')
    for category in category_3:
        priority = ask_for_value(category)
        for task in priorities:
            if task[3] == category:
                task[0] += priority

    print('=======================================')
    print('Very well! You can find your results in {}!'.format(output_file))
    priorities.sort(reverse=True)
    save(priorities,output_file)
    
    


if __name__ == "__main__":
    input_file = 'input.csv'
    output_file = 'output.csv'
    progress_file = 'progress.csv'

    main(input_file,progress_file,output_file)