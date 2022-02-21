import csv

def get_new_id(filename):
    all_items = get_all(filename)
    return len(all_items) + 1

def get_all(filename):
    with open(filename, newline="") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        return [record for record in csv_reader]

def add_new(filename, new_item, headers):
    with open(filename, "w") as csv_file:
        csv_writer = csv.DictWriter(csv_file, headers)
        csv_writer.writeheader()
        csv_writer.writerows(new_item)