import csv
import shlex
import random
import subprocess


def gen_rand_string(char_length=10, has_special_character=False):
    """Generate random string with the specificed character char_length"""
    random_str = ''

    for _ in range(char_length):
        if has_special_character == True:
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

            fieldnames = list.copy(reader.fieldnames)
            if fieldnames.__contains__('Score') == False:
                fieldnames.append('Score')

            writer = csv.DictWriter(out, fieldnames=fieldnames)
            writer.writeheader()

            for row in reader:
                repo = row['Please submit the URL to your technical assessment solution here']
                track = row['What field are you signing up for?']
                # level = row['What track level are you signing up for']

                if repo == '':
                    continue

                command = f"--engine {str(track.split(' ')[0]).lower()} --repo {repo} --dir {tempdir}"
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
