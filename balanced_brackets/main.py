import re
import sys

def validate_bracket_input(brack_input):
    result = True
    if len(brack_input) % 2:
        result = False
    elif not re.match('[\[\]{}\(\)]*$', brack_input):
        result = False
    else:
        matching_list = []
        matching_pattern = {
            '}': '{',
            ')': '(',
            ']': '['
        }
        for char in brack_input:
            if char in matching_pattern.values():
                matching_list.append(char)
            elif matching_list.pop() != matching_pattern[char]:
                result = False
    return result

if __name__ == '__main__':
    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            print('{} - {}'.format(arg, 'VALID' if validate_bracket_input(arg) else 'INVALID'))
    else:
        print('Please provide an input')
        sys.exit(1)