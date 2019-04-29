#!/usr/bin/python
# coding: UTF-8
import re
import os
from datetime import datetime
from glob import glob
from argparse import ArgumentParser
import shutil

read_file = None
write_file = None

write_file_name = './fake.h'

file_header = """/**
* @file 	fake.h
* @note    This file Created by FakeFunctionCreate.py	
* @author	AshGarden
* @date	{}
*/

#ifndef FAKE_H_
#define FAKE_H_
""".format(datetime.now().strftime("%Y/%m/%d"))

file_foot = r"""
#endif /* FAKE_H_ */"""

macro = r"""
#define		CFAKE_VALUE_FUNC(ret,name,...)	\
    extern	ret	UT_##name(__VA_ARGS__);		\
    FAKE_VALUE_FUNC(ret,name,__VA_ARGS__);
#define		CFAKE_VOID_FUNC(name,...)		\
    extern	void UT_##name(__VA_ARGS__);	\
    FAKE_VOID_FUNC(name,__VA_ARGS__)
#define REAL_FUNC(x) x##_fake.custom_fake = UT_##x;
#define FAKE_FUNC(x) x##_fake.custom_fake = NULL;
#define TEST_CASE_NAME(x)	// x

"""

fakelist_header = r"""
#define  FFF_FAKES_LIST( FAKE ) \
do{ \
"""

fakelist_foot = r"""}while(0)
"""



ptnFunction = r'^extern\s([a-zA-Z1-9_*\s].*)\s(.*)\((.*)\)'

def GetFunctionArgs(fargs):
    #引数の個数分整形する
    arglist = str( fargs ).split(",")
    newarglist = []
    for x in arglist:
        #配列型をポインタ型に変換
        tmp = x.strip()
        ary = tmp.find('[')
        if ary != -1 :
            tmp =  tmp[:ary-1] + '*x'
        
        #ポインタ型から変数名を除去
        tmps = tmp.split()
        ast = tmps[len(tmps)-1].find('*')
        if ast != -1 :
            tmps[len(tmps)-1] = tmps[len(tmps) -1][:ast +1]
        else :
            tmps = tmps[:len(tmps)-1]
        #文字列に戻す
        tmp = ' '.join(tmps)
        #print('fargs type:',tmp)
        newarglist.append(tmp)
    return newarglist

def WriteFakeH( wfile,lst):
    try:
        if os.path.exists(wfile):
            shutil.copyfile(wfile,wfile +".back" + datetime.now().strftime("%Y%m%d%H%M%S"))

        write_file = open(wfile, 'w')
        
        write_file.write(file_header)
        write_file.write(macro)

        for f in lst:
            if f["type"] == "void":
                write_file.write("CFAKE_VOID_FUNC({},{});\n".format(f["name"],f["arg"]))                
            else:
                write_file.write("CFAKE_VALUE_FUNC({},{},{});\n".format(f["type"],f["name"],f["arg"]))                


        write_file.write(fakelist_header)

        for f in lst:
            write_file.write("\t FAKE({})\t\\\n".format(f["name"]));
        
        write_file.write(fakelist_foot)
        write_file.write(file_foot)
    finally:
        write_file.close()


def GetFlist( hfilename, lst ):
    try:
        read_file = open(hfilename, 'r')

        for line in read_file:
            #関数宣言の検索
            m = re.search(ptnFunction,line)
            if m :
                ftype,fname,fargs = m.groups()

                finfo = {"type":ftype,
                        "name" : fname,
                        "arg": ','.join(GetFunctionArgs(fargs))}
                lst.append(finfo)
    finally:
        read_file.close()


def FakeHCreate(rootname):
    lst = []
    targetptn = os.path.join(rootname,'*.h')

    files = glob(targetptn)
    for file_name in files:
        GetFlist(file_name,lst)        
    WriteFakeH(write_file_name,lst)
    return "Done"

def parser():
    usage = 'Usage: python {} DirectoryName [--help]'\
            .format(__file__)
    argparser = ArgumentParser(usage=usage)
    argparser.add_argument('DirectoryName', type=str,
                           help='Directory name where containing C header files')

    args = argparser.parse_args()

    return args.DirectoryName


if __name__ == '__main__':
    dirname = parser()
    dirname = os.path.dirname(dirname)

    result = FakeHCreate(dirname)
    print(result)
