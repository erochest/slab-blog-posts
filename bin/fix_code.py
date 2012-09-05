#!/usr/bin/env python

import re
import sys


def fix_pre(match):
    buffer = ['\n[sourcecode']
    if match.group('lang'):
        buffer.append(' language="{0}"'.format(match.group('lang')))
    buffer.append(']\n')
    return ''.join(buffer)


for line in sys.stdin:
    line = re.sub(r'<pre(?: class="(?P<lang>\w+)")><code>', fix_pre, line)
    line = re.sub(r'-m &quot;(.*)&quot;', r'-m "\1"', line)
    line = re.sub(r'</code></pre>', '\n[/sourcecode]\n', line)
    sys.stdout.write(line)
