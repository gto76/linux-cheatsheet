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
BATCH_SEPARATOR = "<tr style='padding:3px'><td width=155px></td><td></td></tr>"
SKIP_LINES = 14
SEP = ' — '
TOP_PADDING = 10


###
##  MAIN
#

def main():
    # Paragraph and code block do not contain ' — ' and begin at the start of
    # line. Code block is bounded by '```'
    lines = [convert_specials(a) for a in read_file(sys.argv[1])]
    lines = lines[SKIP_LINES:]
    out = []
    table = []
    code_block = []
    in_code = False
    paragraph = []
    lines = iter(lines)
    for line in lines:
        if line.startswith('```'):
            check_par_and_table(out, paragraph, table)
            # if paragraph:
                # out.append(get_paragraph(paragraph))
                # paragraph = []
            # if in_code:
                # out.append(get_code(code_block)) 
                # code_block = []               
            in_code = not in_code
            continue
        if in_code:
            code_block.append(line)
            continue
        title = get_title(line, lines)
        if title:
            check_par_and_table(out, paragraph, table)
            # if paragraph:
                # out.append(get_paragraph(paragraph))
                # paragraph = []
            # if table:
                # out.append(get_table(table))
                # table = []
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
        check_par_and_table(out, paragraph, table)

    # if table:
        # out.append(get_table(table))
    # if paragraph:
        # out.append(get_paragraph(paragraph))
    check_par_and_table(out, paragraph, table)
    out = parse_inline_code(out)
    print(insert_in_template(out))


def check_par_and_table(out, paragraph, table):
    if paragraph:
        out.append(get_paragraph(paragraph))
        paragraph.clear()
    if table:
        out.append(get_table(table))
        table.clear()


def parse_inline_code(lines):
    return [re.sub('`(.*?)`', '<code>\\1</code>', a) for a in lines]


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
        if first_h1:
            pre = ''
            first_h1 = False
        return pre + format_title(title, 1)
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
    # out = ''.join(line_batches)
    out = f'<table width=780><tbody>\n{out}\n</tbody></table><br>'
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
        out = []
        out.append(f'<tr><td style="padding-right: 10px;padding-top: {TOP_PADDING}px" valign="top"><strong><code>{s.name}</code>' \
                   f'</strong></td>')
        if s.desc:
            out.append(f'<td style="padding-top: 10px" valign="top">{format_desc(s.desc)}</td></tr>\n')
        options_str = []
        top_padding = 0
        for i, opt in enumerate(s.options):
            if not s.desc and i == 0:
                top_padding = TOP_PADDING
            options_str.append(f'<tr> <td style="width:1px;white-space:nowrap;padding-right:10px;padding-top:{top_padding}px" valign="top"><strong><code>{opt.name}</code>' \
                               f'</strong></td><td style="padding-top:{top_padding}px" valign="top">{format_desc(opt.desc)}</td>' \
                               f'</tr>\n')
            top_padding = 0
        if options_str:
            options = ''.join(options_str)
            if s.desc:
                out.append(f'<tr> <td></td> <td><table>\n{options}\n' \
                           f'</table> </td> </tr>\n')
            else:
                out.append(f'<td><table>\n{options}\n' \
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
        new_command = re.match('\S', line)
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
        return ' '.join(a.strip() for a in lines)


def read_file(filename):
    with open(filename, encoding='utf-8') as file:
        lines = file.readlines()
        return [a.strip('\n') for a in lines]


if __name__ == '__main__':
    main()
