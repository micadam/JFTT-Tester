main = {
    'basic/read_put.imp': {
        'title': "Tests assignment, read and put",
        'input': [['10']],
        'output': [['10']]
    },
    'basic/assign.imp': {
        'title': "Tests assignment by :=",
        'input': [[]],
        'output': [['13']]
    },
    'basic/assign_ident.imp': {
        'title': "Tests assignment of a variable to another variable",
        'input': [[]],
        'output': [['5']]
    },
    'basic/add_multi.imp': {
        'title': "Multiple addition of identifiers and numbers",
        'input': [[]],
        'output': [['20']]
    },
    'basic/add_nums.imp': {
        'title': "Tests addition of two numbers",
        'input': [[]],
        'output': [['8']]
    },
    'basic/sum.imp': {
        'title': "Tests simple addition of two numbers",
        'input': [[]],
        'output': [['12']]
    },
    'basic/multi_subs.imp': {
        'title': "Tests all kinds of substraction",
        'input': [[]],
        'output': [['35']]
    },
    'basic/sum2.imp': {
        'title': "Another test for addition",
        'input': [
            ['0', '5'],
            ['7', '101'],
            ['4', '20'],
            ['17', '8']
        ],
        'output': [
            ['5', '10', '20', '12', '8'],
            ['108', '113', '20', '115', '8'],
            ['24', '29', '20', '31', '8'],
            ['25', '30', '20', '32', '8']
        ]
    },
    'basic/sub2.imp': {
        'title': "Broad test for substraction",
        'input': [
            ['5', '0'],
            ['7', '101']
        ],
        'output': [
            ['5', '0', '495', '0', '0', '2'],
            ['0', '94', '392', '0', '0', '2']
        ]
    },
    'basic/constants.imp': {
        'title': "Simple check for constants",
        'input': [
            []
        ],
        'output': [
            ['0', '1', '2', '7', '13']
        ]
    },
    'comments/comments.imp': {
        'title': "Tests comments in most combinations",
        'input': [[]],
        'output': [['5']]
    },
    'conditions/simple_if.imp': {
        'title': "Tests all conditions in simple ifs",
        'input': [['1', '2', '3', '4']],
        'output': [['2', '3']]
    },
    'conditions/if_then_else.imp': {
        'title': "Tests simple if-then-else",
        'input': [['1', '2']],
        'output': [['1']]
    },
    'conditions/all_conditions.imp': {
        'title': "Tests all kinds of condition in ifs",
        'input': [['1', '2', '3']],
        'output': [['2', '1', '2']]
    },
    'conditions/nested_if_else.imp': {
        'title': "Tests 3 nested if-then-else",
        'input': [['3', '1', '2', '4']],
        'output': [['4']]
    },
    'conditions/more_conditions.imp': {
        'title': "Another test for conditions",
        'input': [
            ['10', '20'],
            ['21', '15'],
            ['2', '2'],
            ['2', '1']
        ],
        'output': [
            ['11', '11', '20', '11', '10', '11', '33'],
            ['11', '21', '11', '11', '21', '11', '33'],
            ['11', '11', '2', '11', '11', '33'],
            ['11', '2', '11', '11', '11', '33']
        ]
    }
}
