#!/usr/bin/env python3

import string
import datetime
import argparse

from subprocess import Popen, PIPE
from collections import Counter

import lxml.html
import roman

a = argparse.ArgumentParser()
a.add_argument('-F', '--final', default=False, action='store_true', help='Remove draft watermarks')
a.add_argument('-d', '--date', default=[], nargs=1, help='Date string to use (yyyy-mm-dd)')
a.add_argument('-f', '--file', dest='texfile', type=argparse.FileType('r'), default='./constitution.tex')
a.add_argument('-T', '--title', default=[])
a.add_argument('-P', '--parts', default=False, action='store_true')
args = a.parse_args()

with open('resources/draft.png.base64') as f:
    draft_style = """<style>
      .page {
        background: url(data:image/png;base64,%s) repeat !important;
        background-size: 100%% !important;
      }
</style>""" % f.read()

list_depth_tokens = ['1', 'a', 'i', 'A']

list_depth_style = {
    '1': lambda x: str(x),
    'a': lambda x: string.ascii_lowercase[x-1],
    'i': lambda x: roman.toRoman(x).lower(),
    'A': lambda x: string.ascii_uppercase[x-1]
}

def get_list_depth(node):
    i = -1
    if node.tag == "ol" or node.tag == "ul":
        i += 1

    parent = node.getparent()
    while parent is not None:
        if parent.tag == "ol" or parent.tag == "ul":
            i += 1
        parent = parent.getparent()

    return i

def create_para_link(doc, node, id_attr=None):
    a = doc.makeelement('a')
    a.attrib['href'] = "#%s" % (id_attr or node.attrib['id'])
    a.attrib['class'] = 'pilcrow'
    a.text = "¶"
    node.append(a)

def id_str(value, depth, separator):
    if separator == ".":
        return str(value)

    return list_depth_style[list_depth_tokens[depth]](int(value))

def generate_id(counter, depth, separator=".", prefix="part-", suffix=""):
    o = []
    i = depth

    while i >= 1:
        o.append(counter[i])
        i -= 1
        
    if current_level == 0:
        return prefix + roman.toRoman(articles[current_level]).lower()
    elif args.parts:
        return prefix + roman.toRoman(articles[0]).lower() + '-' + separator.join([id_str(x, n, separator) for n, x in enumerate(reversed(o))]) + suffix
    else:
    	return separator.join([id_str(x, n, separator) for n, x in enumerate(reversed(o))]) + suffix
        
def generate_list_id(counter, depth, separator=")(", prefix="(", suffix=")"):
    o = []
    i = depth

    while i >= 0:
        o.append(counter[i])
        i -= 1

    return prefix + separator.join([id_str(x, n, separator) for n, x in enumerate(reversed(o))]) + suffix


def reset_counter_to(counter, depth):
    for k in [k for k in counter.keys() if k > depth]:
        del counter[k]

cmd = r"sed 's/\\part/\\chapter/' | pandoc -f latex -t html5 --section-divs"
process = Popen(cmd, shell=True, stdout=PIPE, stdin=args.texfile)

data = process.communicate()[0].decode()
text = open('template.html').read() % data
if len(args.date) > 0:
    date = datetime.datetime.strptime(args.date[0], "%Y-%m-%d")
else:
    date = datetime.datetime.now()
text = text.replace("{date}", "{0.day} {0:%B} {0:%Y}".format(date))
text = text.replace("{date_iso}", date.strftime("%Y-%m-%d"))

doc = lxml.html.fromstring(text)

if len(args.title) > 0:
    text = text.replace("{title}", args.title)
else:
	text = text.replace("{title}", "")

doc = lxml.html.fromstring(text)

if args.parts:
	text = text.replace("/*!!", "")
	text = text.replace("!!*/", "")
	
doc = lxml.html.fromstring(text)

articles = Counter()
list_items = Counter()

last_id = ""
last_section = None
list_depth = -1
ready = False

if not args.final:
    doc.head.append(lxml.html.fragment_fromstring(draft_style))
    doc.body.cssselect(".title")[0].append(lxml.html.fragment_fromstring(
        "<span style='color: red'> DRAFT</span>"))

# Sub in the logo
with open("resources/logo.png.base64") as f:
    doc.body.cssselect(".logo img")[0].attrib['src'] = "data:image/png;base64," + f.read()

for node in doc.body.iter():
    if not ready:
        if node.tag == "hr":
            ready = True
            node.getparent().remove(node)
        else: continue

    # Catch sections (\part)
    if node.tag == "section":
        last_section = node
        current_level = int(node.attrib['class'][5:]) - 1

        node.attrib.clear()

        articles[current_level] += 1

        last_id = node.attrib['id'] = generate_id(articles, current_level)
            #node.attrib['class'] = 'article'
        node.tag = "div"
        reset_counter_to(articles, current_level)

    elif node.tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
        if node.tag == "h1":
            node.attrib['class'] = 'part'
        create_para_link(doc, node, last_section.attrib['id'])

    elif node.tag == "dt":
        node.attrib['id'] = node.text.strip().lower().replace(" ", '-').replace(":", "")
        create_para_link(doc, node, node.attrib['id'])

    elif node.tag == "ol":
        list_depth = get_list_depth(node)
        reset_counter_to(list_items, list_depth-1)
        node.attrib['type'] = list_depth_tokens[list_depth]
        
    elif node.tag == "ul":
        list_depth = get_list_depth(node)
        reset_counter_to(list_items, list_depth-1)
        node.attrib['type'] = list_depth_tokens[list_depth]

    elif node.tag == "li":
        list_depth = get_list_depth(node)
        list_items[list_depth] += 1
        node.attrib['id'] = last_id + generate_list_id(list_items, list_depth)
        reset_counter_to(list_items, list_depth)
        create_para_link(doc, node[0], node.attrib['id'])

print(lxml.html.tostring(doc, pretty_print=True).decode())
