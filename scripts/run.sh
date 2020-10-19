#!/bin/bash

APP=$1    # main.js or app.py ...
INPUT=$2  # input.txt or input02.txt
OUTPUT=$3 # output.txt or input02.txt

# print_usage example and exit with zero status
function print_usage() {
    echo "Example:\n\t./run_accessment.sh app.py input.txt output.txt\n"
    exit 0
}

function check_args_is_file() {
    if [ ! -f $1 ]; then
        echo "\n>> fileTypeError: invalid fileType required. expected fileType: *.{py, js, txt} got: $1\n"
        print_usage
    fi
}

# assert arg is_equal to expected output
function assert() {
    result="$(echo $1 | sed -e "s/ //g")"
    expected="$($(echo cat $OUTPUT) | sed -e 's/ //g')"
    echo $result
    echo $expected

    if test $result = $expected; then
        echo "Passed"
    else
        echo "Failed"
    fi
}

check_args_is_file $APP
check_args_is_file $INPUT
check_args_is_file $OUTPUT

# main program
# check APP mime-type and set the require caller
case $(echo ${APP} | awk -F. '{print $2}') in
py)
    assert "$(python $APP <$INPUT)"
    ;;
js)
    assert "$(node $APP "$(cat $INPUT)")"
    ;;
*)
    echo "\n>> languageSupportError: solution file language not supported. Require executable file type."
    exit 3
    ;;
esac
