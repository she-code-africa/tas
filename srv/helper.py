import csv
import shlex
import random
import subprocess

from werkzeug.utils import secure_filename


def gen_rand_string(char_length=10, has_special_character=True):
    """Generate random string with the specificed character char_length"""
    random_str = ''

    for _ in range(char_length):
        if has_special_character == False:
            random_int = random.randint(0, 255)
        else:
            random_int = random.randint(97, 97 + 26 - 1)
            flip_bit = random.randint(0, 1)
            random_int = random_int - 32 if flip_bit == 1 else random_int
        random_str += (chr(random_int))

    return (random_str, len(random_str))


def async_csv_worker(file, tempdir):
    """ """

    input_file_name = gen_rand_string()[0] + '.csv'
    output_file_name = gen_rand_string()[0] + '.csv'

    input_file = f'{tempdir}/{input_file_name}'
    output_file = f'{tempdir}/{output_file_name}'

    file.save(input_file)

    with open(output_file, 'w', newline='') as out:
        with open(input_file) as file:
            reader = csv.DictReader(file)
            writer = csv.DictWriter(out, fieldnames=reader.fieldnames)

            writer.writeheader()
            for row in reader:
                if row['GITHUB LINK'] == '':
                    continue

                command = f"--engine {str(row['TRACK']).lower()} --repo {row['GITHUB LINK']} --dir {tempdir}"
                response = invoke_runner(command)

                if response >= 1:
                    row.update({'Score': 'Fail'})
                else:
                    row.update({'Score': 'Pass'})

                writer.writerow(row)

    return output_file_name


def invoke_runner(command, timeout=500):
    args = shlex.split(f"./scripts/runner.sh {command}")
    response = subprocess.Popen(args)
    return response.wait(timeout)
