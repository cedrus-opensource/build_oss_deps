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

sndfile_binaries_dir = os.path.abspath(
    os.getcwd() + '/../../binaries_snd_and_paudio')

sndfile_conf_tmp_dir = sndfile_binaries_dir + os.path.sep + 'tmp' + os.path.sep + 'sndfile'

# this next path is INTENTIONALLY a relative path. (not absolute path)
relpath_to_reach_sndfile_src_from_our_output_dir = '../../../build_oss_deps/mac/cedrus_build_snd_and_paudio/libsndfile-1.0.24/'

flac_inc_dir = os.path.abspath(
    os.getcwd() +
    '/cedrus_build_snd_and_paudio/flac_ogg_vorbis_from_homebrew/flac/1.3.1/include')
flac_lib_dir = os.path.abspath(
    os.getcwd() +
    '/cedrus_build_snd_and_paudio/flac_ogg_vorbis_from_homebrew/flac/1.3.1/lib')

ogg_inc_dir = os.path.abspath(
    os.getcwd() +
    '/cedrus_build_snd_and_paudio/flac_ogg_vorbis_from_homebrew/libogg/1.3.2/include')
ogg_lib_dir = os.path.abspath(
    os.getcwd() +
    '/cedrus_build_snd_and_paudio/flac_ogg_vorbis_from_homebrew/libogg/1.3.2/lib')

vorbis_inc_dir = os.path.abspath(
    os.getcwd() +
    '/cedrus_build_snd_and_paudio/flac_ogg_vorbis_from_homebrew/libvorbis/1.3.5/include')
vorbis_lib_dir = os.path.abspath(
    os.getcwd() +
    '/cedrus_build_snd_and_paudio/flac_ogg_vorbis_from_homebrew/libvorbis/1.3.5/lib')

# First section:  do a bunch of sanity-checking
ced_py_utils.verify_that_CWD_is_the_enclosing_folder_of_this_script()
ced_py_utils.verify_absence_of_fink()
ced_py_utils.verify_absence_of_homebrew()
ced_py_utils.enforce_dir_exists(
    sndfile_conf_tmp_dir + os.path.sep +
    relpath_to_reach_sndfile_src_from_our_output_dir)
ced_py_utils.enforce_dir_exists(sndfile_binaries_dir)
ced_py_utils.enforce_dir_exists(flac_inc_dir)
ced_py_utils.enforce_dir_exists(flac_lib_dir)
ced_py_utils.enforce_dir_exists(ogg_inc_dir)
ced_py_utils.enforce_dir_exists(ogg_lib_dir)
ced_py_utils.enforce_dir_exists(vorbis_inc_dir)
ced_py_utils.enforce_dir_exists(vorbis_lib_dir)

conf_cmd = relpath_to_reach_sndfile_src_from_our_output_dir + os.path.sep + 'configure '
conf_cmd += ' CC="clang -v" '
conf_cmd += ' CXX=clang++ '
conf_cmd += ' LDFLAGS="-stdlib=libc++ -mmacosx-version-min=10.7 -isysroot/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX10.7.sdk"  '
conf_cmd += ' CXXFLAGS="-std=c++11 -stdlib=libc++ -mmacosx-version-min=10.7 -DMAC_OS_X_VERSION_MIN_REQUIRED=1070 -isysroot/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX10.7.sdk"   '
conf_cmd += ' CFLAGS="-mmacosx-version-min=10.7 -DMAC_OS_X_VERSION_MIN_REQUIRED=1070 -isysroot/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX10.7.sdk"   '
conf_cmd += ' CPPFLAGS="-mmacosx-version-min=10.7 -DMAC_OS_X_VERSION_MIN_REQUIRED=1070 -isysroot/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX10.7.sdk" '

conf_cmd += ' FLAC_CFLAGS="-I' + flac_inc_dir + '" '
conf_cmd += ' FLAC_LIBS="-L' + flac_lib_dir + ' -lFLAC.8" '
conf_cmd += ' OGG_CFLAGS="-I' + ogg_inc_dir + '" '
conf_cmd += ' OGG_LIBS="-L' + ogg_lib_dir + ' -logg.0" '
conf_cmd += ' VORBIS_CFLAGS="-I' + vorbis_inc_dir + '" '
conf_cmd += ' VORBIS_LIBS="-L' + vorbis_lib_dir + ' -lvorbis.0" '
conf_cmd += ' VORBISENC_CFLAGS="-I' + vorbis_inc_dir + '" '
conf_cmd += ' VORBISENC_LIBS="-L' + vorbis_lib_dir + ' -lvorbisenc.2 -lvorbisfile.3" '

conf_cmd += ' --enable-external-libs --disable-static --enable-shared  --disable-sqlite --disable-dependency-tracking '

# note that we are SETTING CWD TO THE OUTPUT directory before running 'configure'.
# (in other words, we are NOT running configure from the dir where configure resides.)
# This causes all the build artifacts from running configure and make to go into the OUTPUT (binaries) dir.
ced_py_utils.exec_command_using_given_cwd(conf_cmd, sndfile_conf_tmp_dir)

ced_py_utils.exec_command_using_given_cwd('make', sndfile_conf_tmp_dir)

shutil.copy2(
    sndfile_binaries_dir + '/tmp/sndfile/src/.libs/libsndfile.1.dylib',
    sndfile_binaries_dir + '/lib/')

ced_py_utils.exec_command_using_given_cwd(
    'install_name_tool -id @executable_path/../libsndfile.1.dylib libsndfile.1.dylib',
    sndfile_binaries_dir + '/lib/')

shutil.copy2(sndfile_binaries_dir + '/tmp/sndfile/src/sndfile.h',
             sndfile_binaries_dir + '/include/mac/libsndfile-1.0.24/')

print("reached the end of cedrus_build_libsndfile.py")
