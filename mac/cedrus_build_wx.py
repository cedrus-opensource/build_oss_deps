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

wx_src_dir = os.path.abspath(os.getcwd() + '/../../wx_src')
binaries_wx_dir = os.path.abspath(os.getcwd() + '/../../binaries_wx')

cedrus_build_script = os.path.abspath(
    os.getcwd() + '/cedrus_build_wx/cedrus_build_wx.sh')
cedrus_dylib_script = os.path.abspath(
    os.getcwd() + '/cedrus_build_wx/cedrus_wx_mach-o_dylib_fixer.sh')
#cedrus_wx_patch = os.path.abspath(
#    os.getcwd() + '/cedrus_build_wx/cedrus_patch_for_wx_v3.0.2.patch')
#cedrus_wx_patch2 = os.path.abspath(
#    os.getcwd() + '/cedrus_build_wx/fix_from_http_trac.wxwidgets.org_changeset_78144.patch')
#cedrus_wx_patch3 = os.path.abspath(
#    os.getcwd() + '/cedrus_build_wx/cedrus_patch_for_less_wxStackWalker.patch')

# First section:  do a bunch of sanity-checking
ced_py_utils.verify_that_CWD_is_the_enclosing_folder_of_this_script()
ced_py_utils.verify_absence_of_fink()
ced_py_utils.verify_absence_of_homebrew()
ced_py_utils.enforce_dir_exists(wx_src_dir)
ced_py_utils.enforce_dir_exists(binaries_wx_dir)

# Second section:  begin actual work towards building wx binaries

ced_py_utils.git_repo_checkout_revision(wx_src_dir, 'f5977dee2123a342601250b9a87bc2549c13cdd0')

shutil.copy2(cedrus_build_script, wx_src_dir)
shutil.copy2(cedrus_dylib_script, wx_src_dir)
#shutil.copy2(cedrus_wx_patch, wx_src_dir)
#shutil.copy2(cedrus_wx_patch2, wx_src_dir)
#shutil.copy2(cedrus_wx_patch3, wx_src_dir)

# if applying the patch FAILS, it could just mean that you already applied it. reset to a clean revision and try again.
#ced_py_utils.git_repo_apply_patch(wx_src_dir,
#                                  'cedrus_patch_for_wx_v3.0.2.patch')
#ced_py_utils.git_repo_apply_patch(wx_src_dir,
#                                  'fix_from_http_trac.wxwidgets.org_changeset_78144.patch')
#ced_py_utils.git_repo_apply_patch(wx_src_dir,
#                                  'cedrus_patch_for_less_wxStackWalker.patch')

ced_py_utils.exec_command_using_given_cwd('./cedrus_build_wx.sh', wx_src_dir)

# this symlink is needed so that 'wxrc' can launch after we ran install_name_tool on the wx dylibs:
os.symlink(binaries_wx_dir + '/built_libs/bin/wxrc',
           binaries_wx_dir + '/built_libs/lib/wxrc')

print("reached the end of cedrus_build_wx.py")
