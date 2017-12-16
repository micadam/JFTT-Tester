# maintainer: Adam Budziak
import argparse
import os
import subprocess
from os import walk, path
from tempfile import mkstemp

import tests

tests_dct = tests.main

INPUT_DIR = "./in"
OUTPUT_DIR = "./out"

# You may want to adjust these. Both absolute and relative paths
# are supported
COMPILER_PATH = "../compiler"
INTERPRETER_PATH = "../interpreter/interpreter"


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class NoMetaError(Exception):
    pass


class CompilationFailed(Exception):
    pass


class CompilationException(Exception):
    pass


class Summary():
    def __init__(self):
        self.failed = 0
        self.passed = 0
        self.compilation_failed = 0
        self.no_meta = 0
        self.exceptions = 0

    def __str__(self):
        res = bcolors.BOLD + "Summary: \n" + bcolors.ENDC

        if self.passed > 0:
            res += bcolors.OKGREEN + "Passed: " + str(self.passed) + '\n'

        if self.failed > 0:
            res += bcolors.FAIL + "Failed: " + str(self.failed) + '\n'

        if self.compilation_failed > 0:
            res += (bcolors.FAIL + "Compilation failed: "
                    + str(self.compilation_failed)) + "\n"

        if self.exceptions > 0:
            res += (bcolors.FAIL + "Exceptions thrown: "
                    + str(self.exceptions) + '\n')

        res += bcolors.ENDC
        return res


class TestSubject:
    def __init__(self, *, input_fpath, meta):
        self.input_fpath = input_fpath
        self.meta = meta

    def _compile(self, compiled):
        try:
            compile_to_file(self.input_fpath, compiled)
        except CompilationFailed:
            self.meta['real_output'] = "Compilation failed"
            raise CompilationFailed()
        except Exception as e:
            self.meta['real_output'] = e
            raise CompilationException()

    def test(self, input_, output_):
        self.expected = output_
        compiled = mkstemp()[1]
        self._compile(compiled)
        try:
            result = subprocess.check_output(
                [INTERPRETER_PATH, compiled], input=input_
            )
        except Exception as e:
            # this could be improved, more info would be nice
            self.meta['real_output'] = e
            raise RuntimeError()

        self.meta['real_output'] = parse_output(result.decode('utf-8'))
        os.remove(compiled)
        return self.meta['real_output'] == output_


def compile_to_file(input_fpath, output_fpath):
    with open(input_fpath) as input_f:
        compiled = subprocess.check_output(
            [COMPILER_PATH], stdin=input_f
        )
        if 'Syntax error' in compiled.decode('utf-8'):
            raise CompilationFailed()
        with open(output_fpath, 'wb') as output_f:
            output_f.write(compiled)


def parse_output(raw_output):
    return [line.split('>')[1].strip()
            for line in raw_output.split('\n')
            if len(line.split('>')) > 1]


def load_input(input_):
    return '\n'.join(str(i) for i in input_).encode('utf-8')


def print_no_meta(input_fpath):
    print(bcolors.WARNING, "WARNING: No meta for ", input_fpath, bcolors.ENDC)


def invalid_meta(input_fpath):
    print(bcolors.WARNING, "WARNING: Invalid meta for ",
          input_fpath, bcolors.ENDC)


def print_error(subj, error_name):
    print(bcolors.FAIL, error_name,
          bcolors.ENDC, bcolors.BOLD, subj.input_fpath, bcolors.ENDC, '\n',
          bcolors.BOLD, subj.meta['title'], bcolors.ENDC, '\n',
          "Expected output: ", subj.expected, "\n",
          "Real output: ", subj.meta['real_output'])


errors = {
    'FAIL': "Test failed:",
    'COMP_FAIL': "Unexpected compilation failure:",
    'COMP_EXC': "Unexpected compilation exception:",
    'INTER_EXC': "Unexpected interpreter exception:"
}


def print_passed():
    print(
        bcolors.BOLD, '.', bcolors.ENDC, end=""
    )


def load_meta(input_fpath):
    try:
        meta = tests_dct[input_fpath.split('/', 2)[2]]
    except KeyError:
        raise NoMetaError()
    return meta


class Tester:
    def __init__(self, summary):
        self.last_ok = False
        self.summary = summary

    def handle_exc(self, print_fn, *args):
        print()
        print_fn(*args)
        self.last_ok = False

    def test_imp(self, subj):
        inputs = subj.meta['input']
        outputs = subj.meta['output']

        if len(inputs) != len(outputs):
            self.handle_exc(invalid_meta, subj.input_fpath)
            return

        for in_, out_ in zip(inputs, outputs):
            try:
                result = subj.test(load_input(in_), out_)
                if not result:
                    self.summary.failed += 1
                    self.handle_exc(print_error, subj, errors['FAIL'])
                else:
                    print_passed()
                    self.summary.passed += 1
                    self.last_ok = True
            except NoMetaError:
                self.handle_exc(print_no_meta, subj.input_fpath)
                self.summary.no_meta += 1
            except CompilationFailed:
                self.handle_exc(print_error, subj, errors['COMP_FAIL'])
                self.summary.compilation_failed += 1
            except CompilationException:
                self.handle_exc(print_error, subj, errors['COMP_EXC'])
                self.summary.compilation_failed += 1
            except RuntimeError:
                self.handle_exc(print_error, subj, errors['INTER_EXC'])
                self.summary.exceptions += 1

    def test_dir(self, dir_, fnames):

        print(bcolors.HEADER, "\nTesting dir: ", dir_, bcolors.ENDC)
        for fname in fnames:
            input_fpath = path.join(dir_, fname)
            try:
                meta = load_meta(input_fpath)
            except NoMetaError:
                self.handle_exc(print_no_meta, input_fpath)
                continue

            subj = TestSubject(input_fpath=input_fpath, meta=meta)
            self.test_imp(subj)

    def test_all(self, dir_):
        for (dirpath, dirnames, fnames) in walk(dir_):
            if fnames:
                self.test_dir(dirpath, fnames)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=(
            "Prosty skrypt automatyzujący proces"
            " testowania kompilatora na JFTT."))
    parser.add_argument('--compiler',
                        help="ścieżka do pliku wykonywalnego kompilatora")
    parser.add_argument('--interpreter',
                        help="ścieżka do pliku wykonywalnego interpretera")
    parser.add_argument(
        '--interpreter_bn',
        help=("ścieżka do pliku wykonywalnego interpretera"
              " dla dużych liczb (nie jest jeszcze wspierany)"))

    args = parser.parse_args()

    if args.compiler is not None:
        COMPILER_PATH = args.compiler
    if args.interpreter is not None:
        INTERPRETER_PATH = args.interpreter
    if args.interpreter_bn is not None:
        pass
        #  not supported yet
        #  INTERPRETER_BN_PATH = args.interpreter_bn

    summary = Summary()
    tester = Tester(summary)
    tester.test_all(INPUT_DIR)
    print("\n", summary)
