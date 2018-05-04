#!/usr/bin/env python3
#
# Usage: parse.py 
# 

from collections import namedtuple
import sys
import re

DEBUG = False

TEMP = 'template.html'
TEMP_ANCHOR = '<!-- INSERT_HERE -->'
BATCH_SEPARATOR = "<tr style='padding:3px'><td></td><td></td></tr>"
SKIP_LINES = 14
SEP = ' — '


###
##  MAIN
#

def main():
    lines = [convert_specials(a) for a in read_file(sys.argv[1])]
    lines = lines[SKIP_LINES:]
    out = []
    table = []
    lines = iter(lines)
    for line in lines:
        title = get_title(line, lines)
        if title:
            if table:
                out.append(get_table(table))
                table = []
            out.append(title)
            continue
        if re.search('\S+', line):
            table.append(line)
    print(insert_in_template(out))


def get_title(line, lines):
    if line.startswith('####'):
        title = next(lines).strip('# ')
        next(lines)
        return format_title(title, 1)
    elif line.startswith('===='):
        title = next(lines).strip(': ')
        next(lines)
        return format_title(title, 2)
    elif re.match('^[A-Z/]+:\s*$', line):
        title = line.strip(': ')
        return format_title(title, 3)


def format_title(text, a_size):
    return f'<h{a_size}>{text.title()}</h{a_size}>'


###
##  TABLE
#

def get_table(lines):
    lines = [a for a in lines if re.search('\S', a)]
    out = []
    line_batches = get_line_batches(lines)
    line_batches = [parse_batch(a) for a in line_batches]
    out = BATCH_SEPARATOR.join(line_batches)
    out = f'<table width=700><tbody>\n{out}\n</tbody></table>'
    return out


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


Option = namedtuple('Option', ['name', 'desc'])

class Cmd:
    def __init__(s, name):
        s.name = name.strip()
        s.desc = []
        s.options = []
        s.last = s.desc

    def append(s, text):
        s.last.append(text)

    def add_option(s, name):
        s.options.append(Option(name.strip(), []))
        s.last = s.options[-1].desc

    def __repr__(s):
        return str({'name': s.name, 'desc': s.desc, 'options': s.options})

    def __str__(s):
        out = []
        out.append(f'<tr><td valign="top"><strong><code>{s.name}</code>' \
                   f'</strong></td>')
        if s.desc:
            # desc_str = ''.join(s.desc)
            out.append(f'<td>{format_desc(s.desc)}</td></tr>\n')
        options_str = []
        for opt in s.options:
            # desc_str = ''.join(opt.desc)
            options_str.append(f'<tr> <td><strong><code>{opt.name}</code>' \
                               f'</strong></td><td>{format_desc(opt.desc)}</td>' \
                               f'</tr>\n')
        if options_str:
            options = ''.join(options_str)
            out.append(f'<tr> <td></td> <td><table>\n{options}\n' \
                       f'</table> </td> </tr>\n')
        return ''.join(out)



def parse_batch(lines):
    '''
    apt-get — Advanced Package Tool built on top of dpkg. New command called simply
            `apt` is also available. It merges the functionalities of `apt-get` and
            `apt-cache`.
        update — Updates local list of existing packages.
        -u dist-upgrade — Upgrades by intelligently handling changing dependencies 
                with new versions of packages. To regularly update put this line: 
                `apt-get update && apt-get -u dist-upgrade` in `crontab`.
    
    Name and description:
    abc — abc abd ..
            abc abc

    Name and option:
    abc — abc — abd ..
            abc abc

    Option:
        abc — abc abc ...
                 abc abc

    If starts with ch, split:
       if three then option

    If does not contain —:
        continuation
    '''
    out = []
    cmd = None
    for line in lines:
        new_command = re.match('\w', line)
        if not new_command:
            process_desc_or_opt(line, cmd)
            continue
        if cmd:
            out.append(cmd)
        tokens = line.split(SEP, 1)
        cmd = Cmd(tokens[0])
        if len(tokens) > 1:
            process_desc_or_opt(tokens[1], cmd)
    if cmd:
        out.append(cmd)
    out_f = repr if DEBUG else str
    return ''.join(map(out_f, out))


def process_desc_or_opt(line, cmd):
    if SEP not in line:
        cmd.append(line)
        return
    name, desc = line.split(SEP, 1)
    cmd.add_option(name)
    cmd.append(desc)


def insert_in_template(text):
    out = []
    template = read_file(TEMP)
    for line in template:
        if re.search(TEMP_ANCHOR, line):
            out.append('\n'.join(text))
            continue
        out.append(line)
    return '\n'.join(out)


###
##  UTIL
#

def convert_specials(line):
    line = line.replace('<', '&lt;')
    line = line.replace('>', '&gt;')
    return line


def format_desc(lines):
        return ' '.join(a.strip() for a in lines)


def read_file(filename):
    with open(filename, encoding='utf-8') as file:
        lines = file.readlines()
        return [a.strip('\n') for a in lines]


if __name__ == '__main__':
    main()
