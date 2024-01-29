import pytest
import glob
import os

def load_parameterize():
    inputs = glob.glob("tests/data/*.in")
    params = []
    for input in inputs:
        output = input.replace(".in", ".out")
        if not os.path.exists(output):
            continue
        with open(input, "r") as fin:
            test_input = fin.read().strip()
            with open(output, "r") as fout:
                test_output = int(fout.read().strip())
                params.append((test_input, test_output))

    return params

@pytest.mark.parametrize("test_input,expected", load_parameterize())
def test_eval(test_input, expected):
    assert eval(test_input) == expected
