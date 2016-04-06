import glob
import os
import subprocess
import sys

commit = subprocess.check_output(['git', 'log', '-1'])

if b'+UPLOAD' not in commit:
    print('Not uploading')
    sys.exit(0)

# There should be exactly one .whl
filename = glob.glob('*.whl')[0]

pypirc_template = """\
[distutils]
index-servers =
    pypi

[pypi]
repository: https://pypi.python.org/pypi
username: {username}
password: {password}
"""

with open('pypirc', 'w') as f:
    f.write(pypirc_template.format(
        username=os.environ['PYPI_USERNAME'],
        password=os.environ['PYPI_PASSWD'],
    ))

try:
    subprocess.check_call(['twine', 'upload', '--config-file', 'pypirc', filename])
finally:
    os.unlink('pypirc')
