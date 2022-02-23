import csv


def get_new_id(filename):
    all_items = get_all(filename)
    if all_items != None:
        last_item = all_items[-1]['id']
        return int(last_item) + 1
    else:
        return 1

def get_all(filename):
    with open(filename, newline="") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        return [record for record in csv_reader]


def add_new(filename, new_item, headers):
    with open(filename, "a") as csv_file:
        csv_writer = csv.DictWriter(csv_file, headers)
        csv_writer.writerow(new_item)