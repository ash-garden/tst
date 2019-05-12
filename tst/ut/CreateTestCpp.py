#!/usr/bin/python
# coding: UTF-8
import os
from datetime import datetime
from glob import glob
from argparse import ArgumentParser
import shutil

CppFileHeader = """
/**
 * @file 	test.cpp
 * @brief	xxx
 * @author	AshGarden
 * @date	{}
 */
""".format(datetime.now().strftime("%Y/%m/%d"))

CppFileBody = r"""
#include "gtest/gtest.h"

extern "C" {
// xxx include Your Header
#include "fff.h"
#include "fake.h"
DEFINE_FFF_GLOBALS;
}

//TEST START
"""

HFileHeader = """
/**
 * @file 	test1.h
 * @brief	xxx
 * @author	AshGarden
 * @date	{0}
 */

#ifndef {1}_H_
#define {1}_H_
"""
HFileBody2 = """
#define TARGETNAME {0}_C
"""

HFileBody3 = r"""
class TARGETNAME : public ::testing::Test {
protected:
	virtual void SetUp(){
		FFF_FAKES_LIST(RESET_FAKE);
		FFF_RESET_HISTORY();
		FFF_FAKES_LIST(REAL_FUNC);
	}
	virtual void TearDown(){
	}
};

// Custom Fake 


// Test Case
#if 0
TEST_F(TARGETNAME, functionC_1 )
{
// 名前
	TEST_CASE_NAME( "WriteTestCaseName" );
// 手順
	T_STRUCT st;

	UT_functionC(0x12345678,&st,0,NULL);

// 規格
	EXPECT_EQ(st.hight,0x56);
	EXPECT_EQ(st.low  ,0x78);
}
#endif
"""

HFileFoot = """
#endif  /* {0}_H_ */
"""


def CreateTestH( filename ):
    basenameNoExt = os.path.splitext( os.path.basename(filename) )[0] 
    targetHname = "UT_" + basenameNoExt + ".h" 
    targetHpath = os.path.join( "./", targetHname )
    if os.path.exists(targetHpath):
        shutil.copyfile(targetHpath,targetHpath +".back" + datetime.now().strftime("%Y%m%d%H%M%S"))
    try:
        obj_testH = open(targetHpath, 'w')
        obj_testH.write( HFileHeader.format(datetime.now().strftime("%Y/%m/%d"),basenameNoExt) )
        # obj_testH.write( HFileBody )
        obj_testH.write( HFileBody2.format(basenameNoExt))
        obj_testH.write( HFileBody3)
        obj_testH.write( HFileFoot.format(basenameNoExt))

    finally :
        obj_testH.close()
        return targetHname

def CreateTestCpp( dirname ):
    testcpp = "./test.cpp"
    if os.path.exists(testcpp):
        shutil.copyfile(testcpp,testcpp +".back" + datetime.now().strftime("%Y%m%d%H%M%S"))
    try:
        obj_testcpp = open(testcpp, 'w')
        obj_testcpp.write( CppFileHeader )
        obj_testcpp.write( CppFileBody )

        targetptn = os.path.join(dirname,'*.c')
        files = glob(targetptn)
        for file_name in files:
            hfilename = CreateTestH(file_name)        

            obj_testcpp.write( "#include \"{}\"\n".format( hfilename ))

        
    finally:
        obj_testcpp.close()
        return "Done"
    

def parser():
    usage = 'Usage: python {} DirectoryName [--help]'\
            .format(__file__)
    argparser = ArgumentParser(usage=usage)
    argparser.add_argument('DirectoryName', type=str,
                           help='Directory name where containing C source files')

    args = argparser.parse_args()

    return args.DirectoryName


if __name__ == '__main__':
    dirname = parser()
    dirname = os.path.dirname(dirname)

    result = CreateTestCpp(dirname)
    print(result)
