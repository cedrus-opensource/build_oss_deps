from __future__ import print_function
from __future__ import division  # py3 style. division promotes to floating point.
from __future__ import unicode_literals
from __future__ import absolute_import

import os
import sys
import datetime
import subprocess


def verify_that_CWD_is_the_enclosing_folder_of_this_script():
    enclosing_dir = os.path.dirname(sys.argv[0])
    abs_enclosing_dir = os.path.abspath(enclosing_dir)
    abs_cwd = os.path.abspath(os.getcwd())

    if abs_enclosing_dir != abs_cwd:
        print(
            "We need the CWD and enclosing folder of the py script to be the same directory.")
        print("CWD is: " + abs_cwd)
        print("Enclosing is: " + abs_enclosing_dir)
        raise Exception("Cedrus script aborted due to wrong CWD value.")


def verify_absence_of_fink():
    if (os.path.exists('/sw/lib')) or (os.path.isdir('/sw/lib')):
        print(
            'FAIL. you must temporarily hide (rename) your /sw/lib directory to build. linking to libs in /sw will not work for customers.')
        print(
            '      (NOTE: it is simplest to hide the base [sw] dir, otherwise [/sw/bin] is there but [/sw/lib] is not, leading to issues.)')
        exit()


def verify_absence_of_homebrew():
    if (os.path.exists('/usr/local/Cellar')) or (os.path.isdir(
            '/usr/local/Cellar')):
        print(
            'FAIL. you must temporarily hide (rename) your /usr/local/Cellar directory to build. linking to libs in homebrew will not work for customers.')
        exit()


def enforce_dir_exists(the_dir_path):
    if (False == os.path.exists(the_dir_path)) or (
            False == os.path.isdir(the_dir_path)):
        print('FAIL. Cedrus script cannot verify that "' + str(the_dir_path) +
              '" is a directory')
        exit()


def _git_exec_and_return_stdout(command_string, repo_path):

    git_output = ''
    today_datestr = datetime.date.today().strftime("%Y-%m-%d") + ': '

    try:
        """
        On Unix, with shell=True: If args is a string, it specifies the
        command string to execute through the shell. This means that the
        string must be formatted exactly as it would be when typed at the
        shell prompt. This includes, for example, quoting or backslash
        escaping filenames with spaces in them.

        when we set 'shell=True', then the command is one long string.  if
        we use 'shell=False', then command_string should be =
        ['git','log','-5'], or something similar
        """
        git_process = subprocess.Popen(command_string,
                                       shell=True,
                                       stdin=subprocess.PIPE,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE,
                                       cwd=repo_path)

        git_output_bytes, git_errors_bytes = git_process.communicate()
        git_output = git_output_bytes.decode('utf-8')
        git_errors = git_errors_bytes.decode('utf-8')

        # one example of git output that goes to STDERR:
        # if you run 'git checkout XXX' while on XXX, the stderr is:
        #    Already on 'XXX'
        # Furthermore, according the git mailing list, they use STDERR for 'verbose' messages,
        # that are not always errors. that is intentional on their part.
        if len(git_errors) > 0:
            print(today_datestr + 'stderr calling git (' + command_string +
                  ') from path \'' + str(repo_path) + '\':')
            print(git_errors)
        else:
            print(str(today_datestr + 'no git stderr in \'' + str(repo_path) +
                      '\' (' + command_string + ')'))

        # according to the git devs, return code is the proper indicator of success (not checking stderr)
        if git_process.returncode != 0:
            err_msg = str(
                'return code ' + str(git_process.returncode) + ' calling git ('
                + command_string + ') from path \'' + str(repo_path) + '\'')
            raise Exception(err_msg)

    except:
        print(today_datestr + 'python exception calling git (' + command_string
              + ') from path \'' + str(repo_path) + '\'')
        raise  # re-throw the same exception that got us here in the first place

    return git_output


def git_repo_checkout_revision(repopath, revision):
    _git_exec_and_return_stdout('git checkout ' + revision, repopath)


def git_repo_apply_patch(repopath, patchfile):
    _git_exec_and_return_stdout('git apply ' + patchfile, repopath)


def exec_command_using_given_cwd(command_string, working_dir):
    """
    On Unix, with shell=True: If args is a string, it specifies the
    command string to execute through the shell. This means that the
    string must be formatted exactly as it would be when typed at the
    shell prompt. This includes, for example, quoting or backslash
    escaping filenames with spaces in them.

    when we set 'shell=True', then the command is one long string.  if
    we use 'shell=False', then command_string should be =
    ['git','log','-5'], or something similar
    """
    the_process = subprocess.Popen(command_string,
                                   shell=True,
                                   stdin=subprocess.PIPE,
                                   # do not pipe stdout. user wants to view it live in actual time
                                   #stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE,
                                   cwd=working_dir)

    the_output_bytes, the_errors_bytes = the_process.communicate()
    #the_output = the_output_bytes.decode('utf-8') # we did not pipe stdout, so this would fail
    the_errors = the_errors_bytes.decode('utf-8')

    if len(the_errors) > 0:
        print('stderr calling (' + command_string + ') from path \'' +
              str(working_dir) + '\':')
        print(the_errors)

    if the_process.returncode != 0:
        err_msg = str(
            'return code ' + str(the_process.returncode) + ' calling (' +
            command_string + ') from path \'' + str(working_dir) + '\'')
        raise Exception(err_msg)
