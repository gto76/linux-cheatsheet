#!/usr/bin/env python3
#
# Usage: parse.py 
# 

import sys
import re

BATCH_SEPARATOR = "<tr style='padding:3px'><td></td><td></td></tr>"

def main():
    lines = [a for a in read_file(sys.argv[1]) if re.search('\S', a)]
    lines = [convert_specials(a) for a in lines]
    out = []
    line_batches = get_line_batches(lines)
    line_batches = [parse_batch(a) for a in line_batches]
    out = BATCH_SEPARATOR.join(line_batches)
    out = f'<table width=700><tbody>\n{out}\n</tbody></table>'
    print(out)


def convert_specials(line):
    line = line.replace('<', '&lt;')
    line = line.replace('>', '&gt;')
    return line


def get_line_batches(lines):
    out, batch = [], []
    for line in lines:
        no_whitespace = re.match('\S', line)
        if no_whitespace and batch:
            out.append(batch)
            batch = []
        batch.append(line)
    if batch:
        out.append(batch)
    return out


def parse_batch(lines):
    out = parse_description(lines[0].strip())
    if len(lines) > 1:
        out += parse_options(lines[1:])
    return out


def parse_description(line):
    command, description = line.split(' - ', 1)
    description = format_desc(description)
    return f'<tr><td valign="top"><strong><code>{command}</code></strong>' \
           f'</td><td>{description}</td></tr>\n'


def parse_options(lines):
    options = [parse_option(a.strip()) for a in lines]
    options = '\n'.join(options)
    return f'<tr> <td></td> <td><table>\n{options}\n</table> </td> </tr>\n'


def parse_option(line):
    tokens = line.split(' - ', 1)
    if len(tokens) == 2:
        option, description = tokens
        description = format_desc(description)
        return f'<tr> <td><strong><code>{option}</code></strong></td> <td>{description}</td> </tr>\n'
    return f'<tr> <td></td> <td>{tokens[0]}</td> </tr>\n'


###
##  UTIL
#

def format_desc(line):
    return line[0].upper() + line[1:] + '.'
    

def read_file(filename):
    with open(filename, encoding='utf-8') as file:
        return file.readlines()


if __name__ == '__main__':
    main()
