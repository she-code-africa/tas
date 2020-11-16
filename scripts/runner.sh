#!/usr/bin/env bash
# This script is used to download, execute test scrips and output response for the sca assessment tests.

set -e

readonly DEFAULT_RUNNER_DIR="/tmp/sca_runner/downloads"
readonly DEFAULT_RUNNER_TESTCASE="/opt/sca_runner/testcase"

function print_usage() {
    echo
    echo "Usage: runner.sh [options]"
    echo
    echo "This scripts is used by the SCA TAS runner to run the assessment test."
    echo
    echo "Options:"
    echo
    echo -e " --dir\t\tClone the github assessment repo into this folder. Default: $DEFAULT_RUNNER_DIR."
    echo -e " --repo\t\tGitHub repository url."
    echo -e " --engine\tAssessment engine."
    echo -e " --testcase\tFolder containing the testcase inputs/outputs subfolders. Default: $DEFAULT_RUNNER_TESTCASE."
    echo -e " --help\t\tShow this help text and exit."
    echo
    echo "Example:"
    echo
    echo " runner.sh --dir /tmp/download --link https://github.com/demo_user/demo_repo --engine python"
}

# Log the given message at the given level. All logs are written to stderr with a timestamp.
function log() {
    local -r level="$1"
    local -r message="$2"
    local -r timestamp=$(date +"%Y-%m-%d %H:%M:%S")
    local -r script_name="$(basename "$0")"
    echo >&2 -e "${timestamp} [${level}] [$script_name] ${message}"
}

# Log the given message at INFO level. All logs are written to stderr with a timestamp.
function log_info() {
    local -r message="$1"
    log "INFO" "$message"
}

# Log the given message at WARN level. All logs are written to stderr with a timestamp.
function log_warn() {
    local -r message="$1"
    log "WARN" "$message"
}

# Log the given message at ERROR level. All logs are written to stderr with a timestamp.
function log_error() {
    local -r message="$1"
    log "ERROR" "$message"
}

# Check that the value of the given arg is not empty. If it is, exit with an error.
function assert_not_empty() {
    local -r arg_name="$1"
    local -r arg_value="$2"
    local -r reason="$3"

    if [[ -z "$arg_value" ]]; then
        log_error "The value for '$arg_name' cannot be empty. $reason"
        exit 1
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

function select_engine() {
    main program
    check APP mime-type and set the require caller

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
}

function run() {
    local runner_dir="$DEFAULT_RUNNER_DIR"
    local repo=""
    local engine=""
    local testcase=""

    while [[ $# -gt 0 ]]; do
        local key="$1"

        case "$key" in
        --dir)
            assert_not_empty "$key" "$2"
            runner_dir="$2"
            shift
            ;;
        --repo)
            assert_not_empty "$key" "$2"
            repo="$2"
            shift
            ;;
        --engine)
            assert_not_empty "$key" "$2"
            engine="$2"
            shift
            ;;
        --testcase)
            assert_not_empty "$key" "$2"
            testcase="$2"
            shift
            ;;
        --help)
            print_usage
            exit
            ;;
        *)
            log_error "Unrecognized argument: $key"
            print_usage
            exit 1
            ;;
        esac

        shift
    done

    log_info ">> Starting SCA Assessment Runner"

    # mkdir $dir && cd $dir
    # git clone $repo

    log_info ">> Finished running SCA Assessment"
}

run "$@"
