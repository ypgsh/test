
CREATE_FUNCTION = {
                    "name": "calc_len",
                    "desc": "计算长度",
                    "input_args": ["dim", "length"],
                    "code_content": "def calc_len(dim, length):\n    return dim * length"
                }

TEST_FUNCTION_ARGS = {
    "dim": 2,
    "length": 4
}

TEST_FUNCTION_RESULT = 8