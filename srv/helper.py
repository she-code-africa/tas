import csv
import shlex
import subprocess


def find_needed_column(row, search_str):
    row_index = 0
    for i in row:
        if str(i).__contains__(search_str):
            return row_index
        row_index += 1


def gen_get_link(path):
    with open(path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        row_number = 0
        link_column = None
        track_column = None

        for row in csv_reader:
            if row_number == 0:
                # print(f'Column names are {", ".join(row)}')
                track_column = find_needed_column(row, 'TRACK')
                link_column = find_needed_column(row, 'GITHUB LINK')
            else:
                yield {'row': row_number, 'track': row[track_column], 'repo': row[link_column]}

            row_number += 1


def invoke_runner(command, timeout=500):
    args = shlex.split(f"./scripts/runner.sh {command}")
    response = subprocess.Popen(args)
    return response.wait(timeout)
