#!/usr/bin/env python
# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE

###################### DO NOT TOUCH THIS (HEAD TO THE SECOND PART) ######################

import os
import sys

try:
    import DistUtilsExtra.auto
    from DistUtilsExtra.command import build_extra
except ImportError:
    print >> sys.stderr, 'To build unity-dilmaj you need https://launchpad.net/python-distutils-extra'
    sys.exit(1)
assert DistUtilsExtra.auto.__version__ >= '2.18', 'needs DistUtilsExtra.auto >= 2.18'

def update_config(values = {}):

    oldvalues = {}
    try:
        fin = file('unity_dilmaj/unity_dilmajconfig.py', 'r')
        fout = file(fin.name + '.new', 'w')

        for line in fin:
            fields = line.split(' = ') # Separate variable from value
            if fields[0] in values:
                oldvalues[fields[0]] = fields[1].strip()
                line = "%s = %s\n" % (fields[0], values[fields[0]])
            fout.write(line)

        fout.flush()
        fout.close()
        fin.close()
        os.rename(fout.name, fin.name)
    except (OSError, IOError), e:
        print ("ERROR: Can't find unity_dilmaj/unity_dilmajconfig.py")
        sys.exit(1)
    return oldvalues


class InstallAndUpdateDataDirectory(DistUtilsExtra.auto.install_auto):
    def run(self):
        values = {'__unity_dilmaj_data_directory__': "'%s'" % (self.prefix + '/share/unity-dilmaj/'),
                  '__version__': "'%s'" % (self.distribution.get_version())}
        previous_values = update_config(values)
        DistUtilsExtra.auto.install_auto.run(self)
        update_config(previous_values)


        
##################################################################################
###################### YOU SHOULD MODIFY ONLY WHAT IS BELOW ######################
##################################################################################

DistUtilsExtra.auto.setup(
    name='unity-dilmaj',
    version='0.5',
    license='GPL-2',
    author='Farid Ahmadian',
    author_email='pesarkhobeee@gmail.com',
    description='English To Persian Dictionary',
    long_description='Dilmaj is a small and fast english to Persian dictionary for unity dash',
    url='https://github.com/pesarkhobeee/unity-dilmaj',
    data_files=[
        ('share/unity/lenses/dilmaj', ['dilmaj.lens']),
        ('share/dbus-1/services', ['unity-lens-dilmaj.service']),
        ('share/unity/lenses/dilmaj', ['unity-lens-dilmaj.svg']),
        ('bin', ['bin/unity-dilmaj']),
    ],
    cmdclass={"build":  build_extra.build_extra, 'install': InstallAndUpdateDataDirectory}
    )

