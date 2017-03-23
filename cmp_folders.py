#!/usr/bin/env python

import sys
import getopt
import os

#########################
def usage():
    print "[Usage]: python cmp_folders.py folder1 folder2"

#########################
class OutputToFileSwitch:
    __fd = ''
    __origin = ''

    def begin(self, fileToWrite, mode = 'w'):
        if not self.__fd:
            self.__fd = open(fileToWrite, mode)
            if self.__fd:
                self.__origin = sys.stdout
                sys.stdout = self.__fd

    def end(self):
        if self.__fd:
            sys.stdout = self.__origin
            self.__fd.close()
            self.__fd = ''

#########################
def check_args(l):
    # print l
    # for i in range(0, l):
    #     print sys.argv[i]
    # opts, args = getopt.getopt(sys.argv[1:], "hi:o:")
    if l != 3:
        print "invalid parameters."
        usage()
        sys.exit()
    if not os.path.exists(sys.argv[1]):
        print "folder " + sys.argv[1] + " not exists."
        usage()
        sys.exit()
    if not os.path.exists(sys.argv[2]):
        print "folder " + sys.argv[2] + " not exists."
        usage()
        sys.exit()

#########################
import subprocess
def grep(filename, arg):
    process = subprocess.Popen(['grep', '-E', arg, filename], stdout=subprocess.PIPE)
    stdout, stderr = process.communicate()
    return stdout, stderr

#########################
def cmp_folders(leftFdr, rightFdr):
    import filecmp
    ofSwitch = OutputToFileSwitch()
    try:
        #all
        dirobj=filecmp.dircmp(leftFdr, rightFdr)
        ofSwitch.begin('my_result_all.log')
        dirobj.report_full_closure()
        ofSwitch.end()
        #diff
        ofSwitch.begin('my_result_diff.log')
        o, r = grep('my_result_all.log', 'Only')
        print o
        ofSwitch.end()

    except Exception as err:
        print 'somthing error.'
        print err
    finally:
        ofSwitch.end()

#########################
def main():
    arg_len=len(sys.argv)
    check_args(arg_len)
    cmp_folders(sys.argv[1], sys.argv[2])

#########################
main()
# print grep('my_result_all.log', 'Only')