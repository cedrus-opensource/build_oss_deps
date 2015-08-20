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

gtest_binaries_dir = os.path.abspath(os.getcwd() + '/../../binaries_gtest')
gtest_include_dir = os.path.abspath(
    os.getcwd() + '/cedrus_build_gtest/gtest-1.7.0/include')

# this next path is INTENTIONALLY a relative path. (not absolute path)
relpath_to_reach_gtest_src_from_our_output_dir = '../build_oss_deps/mac/cedrus_build_gtest/gtest-1.7.0/'

# First section:  do a bunch of sanity-checking
ced_py_utils.verify_that_CWD_is_the_enclosing_folder_of_this_script()
ced_py_utils.verify_absence_of_fink()
ced_py_utils.verify_absence_of_homebrew()
ced_py_utils.enforce_dir_exists(gtest_binaries_dir + os.path.sep +
                                relpath_to_reach_gtest_src_from_our_output_dir)
ced_py_utils.enforce_dir_exists(gtest_binaries_dir)
ced_py_utils.enforce_dir_exists(gtest_include_dir)

conf_cmd = relpath_to_reach_gtest_src_from_our_output_dir + os.path.sep + 'configure '
conf_cmd += str(' CXX="clang++ -std=c++11 -stdlib=libc++" ' +
                ' LDFLAGS="-stdlib=libc++" LINKFLAGS="-stdlib=libc++" ' +
                ' LINKERFLAGS="-stdlib=libc++" DYLDFLAGS="-stdlib=libc++" ')

# note that we are SETTING CWD TO THE OUTPUT directory before running 'configure'.
# (in other words, we are NOT running configure from the dir where configure resides.)
# This causes all the build artifacts from running configure and make to go into the OUTPUT (binaries) dir.
ced_py_utils.exec_command_using_given_cwd(conf_cmd, gtest_binaries_dir)

ced_py_utils.exec_command_using_given_cwd('make', gtest_binaries_dir)

# there is no 'make install' for gtest

# this symlink is needed so that our builds can find the gtest header files:
os.symlink(gtest_include_dir, gtest_binaries_dir + '/include')

shutil.copy2(gtest_binaries_dir + '/lib/.libs/libgtest.0.dylib',
             gtest_binaries_dir + '/lib/')

# fix mac install id for dylib
install_id_cmd = 'install_name_tool -id @executable_path/libgtest.0.dylib libgtest.0.dylib'
ced_py_utils.exec_command_using_given_cwd(install_id_cmd,
                                          gtest_binaries_dir + '/lib/')
