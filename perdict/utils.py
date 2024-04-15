import re

def space_to_under(s):
    return re.sub(r'\s+', '_', s)