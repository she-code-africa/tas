import csv
import shlex
import random
import subprocess

REPO_LINK = 'Please submit the URL to your technical assessment solution here'
TRACK = 'What field are you signing up for?'
LEVEL = 'What track level are you signing up for'
SCORE = 'Score'


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
            if not fieldnames.__contains__(SCORE):
                fieldnames.append(SCORE)

            writer = csv.DictWriter(out, fieldnames=fieldnames)
            writer.writeheader()

            for row in reader:
                repo = row[REPO_LINK]
                track = row[TRACK]
                level = row[LEVEL]

                try:
                    score = filter_execute(repo, track, level, tempdir)
                    row.update({SCORE: score})
                except Exception:
                    pass

                writer.writerow(row)

    return output_file_name


def async_json_worker(json, tempdir):
    """ """
    output_file_name = gen_rand_string()[0] + '.csv'
    output_file = f"{tempdir}/{output_file_name}"

    with open(output_file, 'w', newline='') as out:
        fieldnames = json[0]
        if not fieldnames.__contains__(SCORE):
            fieldnames.append(SCORE)

        table = json[1:]
        writer = csv.writer(out)

        count = 0
        for row in table:
            if count == 0:
                writer.writerow(fieldnames)
                count += 1

            repo = get_matrix_value(REPO_LINK, fieldnames, row)
            track = get_matrix_value(TRACK, fieldnames, row)
            level = get_matrix_value(LEVEL, fieldnames, row)

            try:
                score = filter_execute(repo, track, level, tempdir)
                set_matrix_value(SCORE, fieldnames, row, score)
            except Exception:
                pass

            writer.writerow(row)

    return output_file_name


def filter_execute(repo, track, level, tempdir):
    track_clean = track.split(' ')[0].lower()
    level_clean = level.split(' ')[0].lower()
    print(track)
    print(track_clean)
    print(level)
    print(level_clean)

    if not ["beginner"].__contains__(level_clean):
        raise f"Unsupported Level: {level}"

    if not ['python', 'javascript', 'java', 'php'].__contains__(track_clean):
        raise f"Unsupported Track: {track}"

    # return appropiate message on empty repos.
    if not repo:
        return "Empty Repo link, Assessment not evaluated."

    command = f"--engine {str(track_clean)} --repo {repo} --dir {tempdir}"
    response = invoke_runner(command)
    score = 'Fail' if response >= 1 else 'Pass'

    return score


def invoke_runner(command, timeout=500):
    args = shlex.split(f"./scripts/runner.sh {command}")
    response = subprocess.Popen(args)
    status_code = response.wait(timeout)

    return status_code


def get_matrix_value(str, header=[], dict=[]):
    idx = header.index(str)
    return dict[idx]


def set_matrix_value(str, header=[], dict=[], value=''):
    idx = header.index(str)
    try:
        dict[idx] = value
    except Exception:
        # if index out of range insert at value
        dict.insert(idx, value)
