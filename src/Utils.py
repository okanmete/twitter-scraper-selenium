import re


def find_between(start, end, s):
    try:
        return (s.split(start))[1].split(end)[0]
    except Exception as e:
        print(e)


def find_all_between(start, end, content):
    liste = []
    while start in content:
        each = find_between(start, end, content)
        liste.append(each)
        content = str_after(content, start)
    return liste


def str_after(s, delim):
    return s.partition(delim)[2]


def clean_html(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext
