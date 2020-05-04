#!/usr/bin/env python

from __future__ import print_function
from __future__ import division  # py3 style. division promotes to floating point.
from __future__ import unicode_literals
from __future__ import absolute_import

import os
import sys
import inspect
import shutil

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(
    inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

import ced_py_utils

portaudio_binaries_dir = os.path.abspath(
    os.getcwd() + '/../../binaries_snd_and_paudio')

portaudio_conf_tmp_dir = portaudio_binaries_dir + os.path.sep + 'tmp' + os.path.sep + 'portaudio'

# this next path is INTENTIONALLY a relative path. (not absolute path)
relpath_to_reach_portaudio_src_from_our_output_dir = '../../../build_oss_deps/mac/cedrus_build_snd_and_paudio/pa_stable_v190600_20161030/'

# First section:  do a bunch of sanity-checking
ced_py_utils.verify_that_CWD_is_the_enclosing_folder_of_this_script()
ced_py_utils.verify_absence_of_fink()
ced_py_utils.verify_absence_of_homebrew()
ced_py_utils.enforce_dir_exists(
    portaudio_conf_tmp_dir + os.path.sep +
    relpath_to_reach_portaudio_src_from_our_output_dir)
ced_py_utils.enforce_dir_exists(portaudio_binaries_dir)

conf_cmd = relpath_to_reach_portaudio_src_from_our_output_dir + os.path.sep + 'configure '
conf_cmd += ' CC="clang -v -Wno-deprecated-declarations -Wno-newline-eof" '
conf_cmd += ' CXX=clang++ '
conf_cmd += ' LDFLAGS="-stdlib=libc++ -mmacosx-version-min=10.11 -isysroot/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX10.13.sdk"  '
conf_cmd += ' CXXFLAGS="-std=c++11 -stdlib=libc++ -mmacosx-version-min=10.11 -DMAC_OS_X_VERSION_MIN_REQUIRED=101100 -isysroot/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX10.13.sdk"   '
conf_cmd += ' CFLAGS="-mmacosx-version-min=10.11 -DMAC_OS_X_VERSION_MIN_REQUIRED=101100 -isysroot/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX10.13.sdk"   '
conf_cmd += ' CPPFLAGS="-mmacosx-version-min=10.11 -DMAC_OS_X_VERSION_MIN_REQUIRED=101100 -isysroot/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX10.13.sdk" '

conf_cmd += ' --enable-shared --disable-static '

prefix_dir = portaudio_binaries_dir + os.path.sep + 'tmp'

conf_cmd += ' --prefix=' + prefix_dir

# note that we are SETTING CWD TO THE OUTPUT directory before running 'configure'.
# (in other words, we are NOT running configure from the dir where configure resides.)
# This causes all the build artifacts from running configure and make to go into the OUTPUT (binaries) dir.
ced_py_utils.exec_command_using_given_cwd(conf_cmd, portaudio_conf_tmp_dir)

ced_py_utils.exec_command_using_given_cwd('make', portaudio_conf_tmp_dir)

ced_py_utils.exec_command_using_given_cwd('make install',
                                          portaudio_conf_tmp_dir)

shutil.copy2(portaudio_binaries_dir + '/tmp/lib/libportaudio.2.dylib',
             portaudio_binaries_dir + '/lib/')

ced_py_utils.exec_command_using_given_cwd(
    'install_name_tool -id @executable_path/../Frameworks/libportaudio.2.dylib libportaudio.2.dylib',
    portaudio_binaries_dir + '/lib/')

shutil.copy2(portaudio_binaries_dir + '/tmp/include/portaudio.h',
             portaudio_binaries_dir + '/include/mac/pa_stable_v190600_20161030/')

print("reached the end of cedrus_build_portaudio.py")
