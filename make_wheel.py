from base64 import urlsafe_b64encode
import hashlib
import os
import sys
import zipfile

wheel_template = """\
Wheel-Version: 1.0
Generator: custom (0.1)
Root-Is-Purelib: false
Tag: {tag}
"""

metadata_template = """\
Metadata-Version: 1.2
Name: PyQt4
Version: {version}
Summary: Intelligently search Python source code
Home-page: https://github.com/takluyver/pyqt4_windows_whl
License: UNKNOWN
Author: Riverbank Computing
Author-email: info@riverbankcomputing.com
Classifier: Development Status :: 5 - Production/Stable
Classifier: Environment :: MacOS X
Classifier: Environment :: Win32 (MS Windows)
Classifier: Environment :: X11 Applications :: Qt
Classifier: Intended Audience :: Developers
Classifier: License :: OSI Approved :: GNU General Public License (GPL)
Classifier: License :: Other/Proprietary License
Classifier: Operating System :: MacOS :: MacOS X
Classifier: Operating System :: Microsoft :: Windows
Classifier: Operating System :: POSIX
Classifier: Operating System :: Unix
Classifier: Programming Language :: C++
Classifier: Programming Language :: Python
Classifier: Programming Language :: Python :: 2
Classifier: Programming Language :: Python :: 3
Classifier: Topic :: Software Development :: User Interfaces
Classifier: Topic :: Software Development :: Widget Sets

PyQt4 is a comprehensive set of Python bindings for Digia’s Qt cross platform
GUI toolkit. PyQt4 supports Python v2 and v3.
"""

def make_wheel(folder, pyqt_version, python_version, bitness):
    tag = 'cp{py_version_nodot}-none-{win_tag}'.format(
        py_version_nodot=python_version.replace('.', ''),
        win_tag=('win_amd64' if bitness==64 else 'win32'),
    )
    filename = 'PyQt4-{version}-{tag}.whl'.format(
        version=pyqt_version, tag=tag,
    )

    records = []
    def record_file(path_on_fs, path_in_archive):
        sha256 = hashlib.sha256()
        size = 0
        with open(path_on_fs, 'rb') as f:
            while True:
                chunk = f.read(1024*8)
                if not chunk:
                    break
                sha256.update(chunk)
                size += len(chunk)
        records.append((path_in_archive, sha256, size))

    def record_data(data, path_in_archive):
        sha256 = hashlib.sha256(data)
        size = len(data)
        records.append((path_in_archive, sha256, size))

    with zipfile.ZipFile(filename, 'w', compression=zipfile.ZIP_DEFLATED) as zf:
        print('Compressing package files...')
        for dirpath, dirnames, filenames in os.walk(folder):
            reldirpath = os.path.relpath(dirpath, start=folder)
            for filename in sorted(filenames):
                path_on_fs = os.path.join(dirpath, filename)
                path_in_archive = os.path.normpath(os.path.join('PyQt4', reldirpath, filename))
                zf.write(path_on_fs, path_in_archive)
                record_file(path_on_fs, path_in_archive)
            # Sorting to give a stable order
            dirnames.sort()

        dist_info = 'PyQt4-{version}.dist-info/'.format(version=pyqt_version)

        print('Adding WHEEL file...')
        wheel_file = wheel_template.format(tag=tag).encode('utf-8')
        zf.writestr(dist_info+'WHEEL', wheel_file)
        record_data(wheel_file, dist_info+'WHEEL')

        print('Adding METADATA file...')
        metadata_file = metadata_template.format(version=pyqt_version).encode('utf-8')
        zf.writestr(dist_info+'METADATA', metadata_file)
        record_data(metadata_file, dist_info+'METADATA')

        print('Creating RECORD...')
        record_lines = [
            '{},sha256={},{}'.format(path,
                urlsafe_b64encode(hashobj.digest()).decode('ascii').rstrip('='),
                size)
            for (path, hashobj, size) in records
        ]
        record_lines.append(dist_info+'RECORD,,')
        record_file = ('\n'.join(record_lines)+'\n').encode('utf-8')
        zf.writestr(dist_info+'RECORD', record_file)

def main(argv=None):
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('directory')
    args = ap.parse_args(argv)

    if 'PYQT_VERSION' not in os.environ:
        sys.exit('PYQT_VERSION environment variable not specified')

    if 'PY_VERSION' not in os.environ:
        sys.exit('PY_VERSION environment variable not specified')

    if 'PY_BITNESS' not in os.environ:
        sys.exit('PY_BITNESS environment variable not specified')

    make_wheel(args.directory,
                pyqt_version=os.environ['PYQT_VERSION'],
                python_version=os.environ['PY_VERSION'],
                bitness=int(os.environ['PY_BITNESS'])
    )

if __name__ == '__main__':
    main()
