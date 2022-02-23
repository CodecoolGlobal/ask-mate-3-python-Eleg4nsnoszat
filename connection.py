import csv


def get_new_id(filename):
    all_items = get_all(filename)
    if all_items:
        last_item = all_items[-1]['id']
        return int(last_item) + 1
    else:
        return 1

def get_all(filename):
    with open(filename, newline="") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        return [record for record in csv_reader]


def add_new(filename, new_item, headers):
    with open(filename, "a", newline="") as csv_file:
        csv_writer = csv.DictWriter(csv_file, headers)
        csv_writer.writerow(new_item)

def delete(filename, delete_id, headers, delete_key):
    all_items = get_all(filename)
    with open(filename, "w", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, headers)
        writer.writeheader()
        for row in all_items:
            for key, value in row.items():
                if key == delete_key and value != delete_id:
                    writer.writerow(row)

def edit(filename, headers, question_id, edit_key, edit_value):
    all_items = get_all(filename)
    with open(filename, "w", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, headers)
        writer.writeheader()
        for row in all_items:
            for key, value in row.items():
                if key == 'id' and value == question_id:
                    row[edit_key] = edit_value
            writer.writerow(row)

