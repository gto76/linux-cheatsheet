#!/usr/bin/env python3
#
# Usage: parse.py [filename]
# Converts text to html file.

from collections import namedtuple
import sys
import re

DEBUG = False

FILENAME = 'linux-cheatsheet.txt'
TEMP = 'web/template.html'
TEMP_ANCHOR = '<!-- INSERT_HERE -->'
BATCH_SEPARATOR = "<tr><td width=155px></td><td></td></tr>"
SKIP_LINES = 14
SEP = ' — '
TOP_PADDING = 7
SMALL_TOP_PADDING = 1


###
##  MAIN
#

def main():
    # Paragraph and code block do not contain ' — ' and begin at the start of
    # line. Code block is bounded by '```'
    filename = FILENAME if len(sys.argv) < 2 else sys.argv[1]
    lines = [convert_specials(a) for a in read_file(filename)]
    lines = lines[SKIP_LINES:]
    out = []
    table = []
    code = []
    in_code = False
    paragraph = []
    lines = iter(lines)
    for line in lines:
        if line.startswith('```'):
            check_par_and_table(out, paragraph, table, code)
            in_code = not in_code
            continue
        if in_code:
            code.append(line)
            continue
        title = get_title(line, lines)
        if title:
            check_par_and_table(out, paragraph, table, code)
            out.append(title)
            continue
        in_paragraph = re.match('\S', line) and SEP not in line
        if in_paragraph:
            paragraph.append(line)
            continue
        if re.search('\S+', line):
            if paragraph:
                out.append(get_paragraph(paragraph))
                paragraph = []
            table.append(line)
            continue
        check_par_and_table(out, paragraph, table, code)

    check_par_and_table(out, paragraph, table, code)
    out = parse_inline_code(out)
    print(insert_in_template(out))


def check_par_and_table(out, paragraph, table, code):
    if paragraph:
        out.append(get_paragraph(paragraph))
        paragraph.clear()
    if table:
        out.append(get_table(table))
        table.clear()
    if code:
        out.append(get_code(code)) 
        code.clear()


def parse_inline_code(lines):
    return [re.sub('`(.*?)`', '\'<code>\\1</code>\'', a) for a in lines]


def get_code(lines):
    code = '\n'.join(lines)
    return f'<pre><code>{code}</code></pre>'


def get_paragraph(lines):
    code = ' '.join(lines)
    return f'<p>{code}</p>'


first_h1 = True

def get_title(line, lines):
    if line.startswith('####'):
        global first_h1
        title = next(lines).strip('# ')
        next(lines)
        pre = '\n<p><br><p>\n'
        post = '\n<br>\n' if title == 'GNOME' else ''
        if first_h1:
            pre = ''
            first_h1 = False
        return f'{pre}{format_title(title, 5)}{post}'
    elif line.startswith('===='):
        title = next(lines).strip(': ')
        next(lines)
        link_id = title.replace(' ', '_').lower()
        link = f'<a href="#{link_id}" name="{link_id}">#</a>'
        return format_title(title, 2, a=link)
    elif re.match('^[A-Z\(\) /]+:\s*$', line):
        title = line.strip(': ')
        return format_title(title, 3)


def format_title(text, a_size, a=''):
    return f'<h{a_size}>{text.title()}{a}</h{a_size}>'


###
##  TABLE
#

def get_table(lines):
    lines = [a for a in lines if re.search('\S', a)]
    out = []
    line_batches = get_line_batches(lines)
    line_batches = [parse_batch(a) for a in line_batches]
    out = BATCH_SEPARATOR.join(line_batches)
    out = f'<table width=780 style="border-spacing: 0px"><tbody>\n{out}\n' \
          f'</tbody></table><br>'
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
        return str({'name': s.name, 'desc': format_desc(s.desc), 
                   'options': s.options})

    def __str__(s):
        big_pad = s.options and (len(s.options) > 1 or s.desc)
        top_padding_this = TOP_PADDING if big_pad else SMALL_TOP_PADDING
        out = []
        name = f'<tr><td style="padding-right: 10px;padding-top: ' \
               f'{top_padding_this}px;width: 155px" valign="top"><strong>' \
               f'<code>{s.name}</code></strong></td>'
        out.append(name)
        if s.desc:
            desc = f'<td style="padding-top: {top_padding_this}px" ' \
                   f'valign="top">{format_desc(s.desc)}</td></tr>\n'
            out.append(desc)
        options_str = []
        top_padding = 0
        for i, opt in enumerate(s.options):
            if not s.desc and i == 0:
                top_padding = top_padding_this
            option = f'<tr> <td style="width:1px;white-space:nowrap' \
                     f';padding-right:10px;padding-top:{top_padding}px" '\
                     f'valign="top"><strong><code>{opt.name}</code></strong>' \
                     f'</td><td style="padding-top:{top_padding}px" ' \
                     f'valign="top">{format_desc(opt.desc)}</td></tr>\n'
            options_str.append(option)
            top_padding = 0
        if options_str:
            options = ''.join(options_str)
            options_table = f'<table style="border-spacing: 0px">\n' \
                            f'{options}\n</table>'
            if s.desc:
                out.append(f'<tr> <td></td> <td> {options_table} </td> </tr>\n')
            else:
                out.append(f'<td valign="top"> {options_table} </td> </tr>\n')
        return ''.join(out)


def parse_batch(lines):
    '''
    Input example
    -------------
    apt-get — Advanced Package Tool built on top of dpkg. New command called 
            simply `apt` is also available. It merges the functionalities of 
            `apt-get` and `apt-cache`.
        update — Updates local list of existing packages.
        -u dist-upgrade — Upgrades by intelligently handling changing 
                dependencies with new versions of packages. To regularly update 
                put this line: `apt-get update && apt-get -u dist-upgrade` in 
                `crontab`.
    
    Elements
    --------
    ### Name and description
    abc — abc abd ..
            abc abc

    ### Name and option
    abc  abc — abd ..
            abc abc

    ### Option
        abc — abc abc ...
                abc abc
    '''

    out = []
    cmd = None
    for line in lines:
        new_command = re.match('\S', line)
        if not new_command:
            process_desc_or_opt(line, cmd)
            continue
        if cmd:
            out.append(cmd)
        tokens = line.split(SEP, 1)
        name = tokens[0]
        if '  ' in name:
            name, option = name.split('  ', 1)
            if len(tokens) < 2:
                tokens.append('')
            tokens[1] = f'{option} — {tokens[1]}'
        cmd = Cmd(name)
        if len(tokens) > 1:
            process_desc_or_opt(tokens[1], cmd)
    if cmd:
        out.append(cmd)
    out_f = repr if DEBUG else str
    return ''.join(map(out_f, out))


def process_desc_or_opt(line, cmd):
    if line.endswith(' —'):
        cmd.add_option(line[:-2])
        return
    if SEP not in line:
        try:
            cmd.append(line)
        except AttributeError:
            print('line is not str', line, file=sys.stderr)
            sys.exit()
        return
    name, desc = line.split(SEP, 1)
    try:
        cmd.add_option(name)
    except AttributeError:
        print('cmd is none', line, file=sys.stderr)
        sys.exit()
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
    out = []
    for line in lines:
        line = re.sub('  $', '<br>', line)
        out.append(line)
    return ' '.join(a.strip() for a in out)


def read_file(filename):
    with open(filename, encoding='utf-8') as file:
        lines = file.readlines()
        return [a.strip('\n') for a in lines]


if __name__ == '__main__':
    main()
