#!/usr/bin/python
# coding: UTF-8

import re
import sys
import os
from enum import Enum
from glob import glob
from datetime import datetime
import shutil
from argparse import ArgumentParser


class STATE(Enum):
    ROW = 1
    IFDEF = 2
    ELSE =3

def MakeBackupDir(rootname):
    dirname = os.path.join(rootname , datetime.now().strftime("%Y%m%d%H%M%S"))
    os.mkdir( dirname)
    return dirname

def CopyFile( file_name,dirname):
    dstfilename = os.path.join( dirname,os.path.basename(file_name))
    dstfilename = dstfilename + ".back"
    shutil.copyfile(file_name,dstfilename)
    return dstfilename


definename = "UT"
ptnIfdef = '#ifdef ' + definename
ptnElse  = '#else //' + definename
ptnEndif = '#endif //' + definename
pattern = '^([a-zA-Z].*\s)(.*)\('
repstr = r'\t\1'+ definename +r'_\2('


def UtUnRename( read_file_name, write_file_name ):
    read_file = None
    write_file = None

    state = STATE.ROW
    try:
        read_file = open(read_file_name, 'r')
        write_file = open(write_file_name, 'w')
        for line in read_file:
            if state == STATE.ROW :
                #ifdef検索
                if re.match(ptnIfdef,line):
                    state = STATE.IFDEF
                else:
                    write_file.write(line)
            elif state == STATE.IFDEF :
                #endif　検索
                if re.match(ptnElse,line):
                    state = STATE.ELSE
            elif state == STATE.ELSE :
                #endif　検索
                if re.match(ptnEndif,line):
                    state = STATE.ROW
                else:
                    write_file.write(line)
                
    finally:
        read_file.close()
        write_file.close()
     

def UtRename( read_file_name, write_file_name ):
    read_file = None
    write_file = None

    state = STATE.ROW

    try:
        read_file = open(read_file_name, 'r')
        write_file = open(write_file_name, 'w')
        for line in read_file:
            if state == STATE.ROW :
                #ifdef検索
                if re.match(ptnIfdef,line):
                    write_file.write(line)
                    state = STATE.IFDEF
                elif re.match(pattern,line):
                    #関数実体
                    write_file.write(ptnIfdef+'\n')
                    write_file.write(  re.sub(pattern,repstr,line) )
                    write_file.write(ptnElse+'\n')
                    write_file.write(line)
                    write_file.write(ptnEndif+'\n')
                else:
                    write_file.write(line)
            elif state == STATE.IFDEF:
                #endif　検索
                if re.match(ptnEndif,line):
                    state = STATE.ROW
                write_file.write(line)

    finally:
        read_file.close()
        write_file.close()
     

def UtRenamer(rootname , revers):
    dirname = MakeBackupDir(rootname)

    targetptn = os.path.join(rootname,'*.c')

    files = glob(targetptn)
    for file_name in files:
        read_file = CopyFile( file_name , dirname )
        write_file = file_name
        print("Process:{}\n".format(write_file))
        if revers == False :
            UtRename( read_file, write_file )
        else :
            UtUnRename ( read_file , write_file)

    return "Done"

def parser():
    usage = 'Usage: python {} [--reverse] DirectoryName [--help]'\
            .format(__file__)
    argparser = ArgumentParser(usage=usage)
    argparser.add_argument('-r', '--reverse',
                            action='store_true',
                            help='reverse convert')
    argparser.add_argument('DirectoryName', type=str,
                           help='Directory name where containing C source code')

    args = argparser.parse_args()

    return args.DirectoryName,args.reverse

if __name__ == '__main__':
    dirname,revers = parser()
    dirname = os.path.dirname(dirname)

    result = UtRenamer(dirname , revers)
    print(result)