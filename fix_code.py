#!/usr/bin/env python

import re
import sys


def fix_pre(match):
    buffer = ['\n[sourcecode']
    if match.group(1) and match.group(2):
        buffer.append('{0}"{1}"'.format(match.group(1), match.group(2)))
    buffer.append(']')
    return ''.join(buffer)


for line in sys.stdin:
    line = re.sub(r'<pre><code>\[sourcecode(\s+\w+=)?(\w+)?\]', fix_pre, line)
    line = re.sub(r'-m &quot;(.*)&quot;', r'-m "\1"', line)
    line = re.sub(r'\[/sourcecode\]</code></pre>', '[/sourcecode]\n', line)
    sys.stdout.write(line)
