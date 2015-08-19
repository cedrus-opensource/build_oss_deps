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

boost_src_dir = os.path.abspath(os.getcwd() + '/../../boost_github')
boost_binaries_dir = os.path.abspath(os.getcwd() + '/../../binaries_boost')

cedrus_build_script = os.path.abspath(
    os.getcwd() + '/cedrus_build_boost/cedrus_build_boost.sh')
cedrus_boost_patch = os.path.abspath(
    os.getcwd() + '/cedrus_build_boost/patch_submodule_tools_build_1_58.patch')

# First section:  do a bunch of sanity-checking
ced_py_utils.verify_that_CWD_is_the_enclosing_folder_of_this_script()
ced_py_utils.verify_absence_of_fink()
ced_py_utils.verify_absence_of_homebrew()
ced_py_utils.enforce_dir_exists(boost_src_dir)
ced_py_utils.enforce_dir_exists(boost_binaries_dir)

# ---------- Begin 2nd section: make sure SUBMODULES inside boost were populated!! -------

# Note: this list of submodules is NOT exhaustive!  please populate ALL SUBMODULES.

# if anything in this section fails, you need to:
#    1. go into the boost_src_dir directory.
#    2. run the command: git submodule init
#    3. run the command: git submodule update --init

submod_msg = 'If this fails, you need to GO INTO YOUR checked-out boost.org repo and do: {git submodule update --init}'
ced_py_utils.enforce_dir_exists(boost_src_dir + '/libs/asio/include',
                                submod_msg)
ced_py_utils.enforce_dir_exists(boost_src_dir + '/libs/lambda/include',
                                submod_msg)
ced_py_utils.enforce_dir_exists(boost_src_dir + '/libs/function/include',
                                submod_msg)
ced_py_utils.enforce_dir_exists(boost_src_dir + '/libs/smart_ptr/include',
                                submod_msg)

# ------------ End 2nd section: make sure SUBMODULES inside boost were populated!! -------

# Third section:  begin actual work towards building boost binaries

print('about to set the boost git repo to a specific tag.')
ced_py_utils.git_repo_checkout_revision(boost_src_dir, 'boost-1.58.0')
print('about to sync boost submodules (one per boost lib).' +
      'This could take a minute...')
ced_py_utils.git_submodule_update(boost_src_dir)

shutil.copy2(cedrus_build_script, boost_src_dir)
shutil.copy2(cedrus_boost_patch, boost_src_dir + '/tools/build')

# if applying the patch FAILS, it could just mean that you already applied it. reset to a clean revision and try again.
ced_py_utils.git_repo_apply_patch(boost_src_dir + '/tools/build',
                                  'patch_submodule_tools_build_1_58.patch')

ced_py_utils.exec_command_using_given_cwd('./cedrus_build_boost.sh',
                                          boost_src_dir)

print("reached the end of cedrus_build_boost.py")
