#!/usr/bin/python
# coding: UTF-8
import os
import re
from enum import Enum
import markdown
import pdfkit
from argparse import ArgumentParser


ptnTESTSTART = "//TEST START"
ptnInclude = "^#include\s\"(.*?)[.]h\""

ptnCustamFake = "// Custom Fake"
ptnTestCase = "// Test Case"
ptnTest = "^TEST_F[(].*?[,](.*?)[)]"
ptnTestName = "\sTEST_CASE_NAME.*?[\"](.*?)[\"].*?"
ptnTestAction = "^// Test Action"
ptnTestExpectedResult = "^// Expected Result"
ptnTestExpRsltExit = "^[}]"
class tcd_state(Enum):
    RAW = 1
    CUSTUMFAKE = 2
    TESTCASE =3
    TESTNAME = 4
    TESTACTIONWAIT = 5
    TESTACTION = 6
    TESTEXPRESULT = 7

class TestCase :
    def __init__(self,targetFile,Title):
        self.targetFile = targetFile
        self.Title = Title.strip()
        self.Name = ""
        self.Action = ""
        self.ExpectedResult = ""
        self.ActualResult = ""
        self.Status = ""
        self.testresult = ""

    def AddName(self,name):
        self.Name = name

    def AddAction( self ,act):
        
        self.Action = act.replace("\n","<br>")
    def AddExpRslt( self , exprslt ):
        
        self.ExpectedResult = exprslt.replace("\n","<br>")
    
    def AddActualResult(self, testResult, tester,testdate,jp):
        if len(testResult) != 0 :
            name ,ext = os.path.splitext(self.targetFile)
            # ptn_OK = r"^[\[]\s*OK\s*[\]]\s*"+ name + r"[_cChH]*[.]"+self.Title
            # ptn_NG = r"^[\[]\s*FAILED\s*[\]]\s*"+ name + r"[_cChH]*[.]"+self.Title

            ptn_OK = re.compile( r"^[\[]\s*OK\s*[\]]\s*"+ name + r"[_cChH]*[.]"+self.Title , re.MULTILINE | re.DOTALL)
            ptn_NG = re.compile( r"^[\[]\s*FAILED\s*[\]]\s*"+ name + r"[_cChH]*[.]"+self.Title , re.MULTILINE | re.DOTALL)

            result = ptn_OK.search( testResult )
            if result :
                if jp is True:
                    self.ActualResult = "同左"
                else :
                    self.ActualResult = "Same as the Left."

                self.Status = testdate + "<br>" + tester + "<br>" + "OK"
                self.testresult = "OK"
            else:
                result = ptn_NG.search( testResult )
                if result :
                    self.ActualResult = ""
                    self.Status = testdate + "<br>" + tester + "<br>" + "NG"
                    self.testresult = "NG"
        
    def CreateHeader(self,jp):
        if jp is True :
            ret  = "|No.|File|Title|Name|手順|規格 | 結果 | 合否 | Note |\n"

        else:
            ret  = "|No.|File|Title|Name|Action|Expected result | Actual result | Status (Pass/Fail) | Note |\n"

        ret += "|:--|:---|:----|:---|:-----|:---------------|:--------------|:-------------------|:-----|\n"
        return ret

    def Create(self,no):
        return "|"+ str(no) + "|"+ self.targetFile + "|" + self.Title + "|" + self.Name + "|" + self.Action + "|" + self.ExpectedResult +"|"+ self.ActualResult+" |"+ self.Status +" |"+" |"+"\n"

class TestCaseDoc :
    def __init__(self,anaFile,targetCFile,resultFile,testername,testdate):
        self.tcd_state = tcd_state.RAW
        self.anaFile = anaFile
        self.targetCFile = targetCFile
        self.custom_func = ""
        self.testcase = []
        if resultFile is not None:
            if( len(resultFile) != 0):
                f = open(resultFile)
                self.testresult =  f.read()
                f.close()
                self.tester = testername
                self.testdate = testdate
        else:
            self.testresult = None

    def GetCount(self):
        return len(self.testcase)
    def Create(self,jp):
        try:
            read_file = open(self.anaFile, 'r')
            for line in read_file:
                if tcd_state.RAW == self.tcd_state :
                    if re.match(ptnCustamFake,line):
                        self.tcd_state = tcd_state.CUSTUMFAKE
                elif tcd_state.CUSTUMFAKE == self.tcd_state :
                    if re.match(ptnTestCase,line) :
                        self.tcd_state = tcd_state.TESTCASE
                    else:
                        self.custom_func += line + "\n"
                elif tcd_state.TESTCASE == self.tcd_state :
                    result =  re.match(ptnTest,line)
                    if result :
                        self.activeCase = TestCase(self.targetCFile,result.group(1))
                        self.tcd_state = tcd_state.TESTNAME
                elif tcd_state.TESTNAME == self.tcd_state :
                    result =  re.match(ptnTestName,line)
                    if result :
                        print(line)
                        print(result.group(1))
                        self.activeCase.AddName(result.group(1))
                        self.tcd_state = tcd_state.TESTACTIONWAIT
                elif  tcd_state.TESTACTIONWAIT == self.tcd_state :
                    if re.match(ptnTestAction,line):
                        self.temp = ""
                        self.tcd_state = tcd_state.TESTACTION
                elif tcd_state.TESTACTION == self.tcd_state :
                    if re.match(ptnTestExpectedResult,line):
                        self.activeCase.AddAction(self.temp)
                        self.tcd_state = tcd_state.TESTEXPRESULT
                        self.temp = ""
                    else:
                        self.temp += line
                elif tcd_state.TESTEXPRESULT == self.tcd_state:
                    if re.match(ptnTestExpRsltExit,line):
                        self.activeCase.AddExpRslt(self.temp)
                        if self.testresult is not None:
                            self.activeCase.AddActualResult(self.testresult,self.tester,self.testdate,jp)
                        self.tcd_state = tcd_state.TESTCASE
                        self.testcase.append(self.activeCase)
                    else:
                        self.temp += line
            
            ret = self.testcase[0].CreateHeader(jp)
            num = 1
            for x in self.testcase:
                ret += x.Create(num)
                num += 1

        finally:
            read_file.close()
            return ret

    def GetSummary(self,jp):
        if jp is True:
            TestTargetFileName =    "試験対象ファイル名      :"
            NumberOfTestCase =      "試験項目数              : "
            NumberOfPassedTestCase ="合格試験項目数          :" 
            NumberOfFailedTestCaes ="不合格試験項目数        :" 
        else:
            TestTargetFileName =    "Test target file name       :"
            NumberOfTestCase =      "Number of test case         :"
            NumberOfPassedTestCase = "Number of test case        :"
            NumberOfFailedTestCaes = "Number of Failed testcaes  :" 

        if self.testresult is None:
            testSummary = TestTargetFileName + self.targetCFile + "\n"
            testSummary += NumberOfTestCase  + str( len(self.testcase) )+ "\n"
        else:
            okcases = 0
            ngcases = 0
            for c in self.testcase:
                if (c.testresult == "OK") :
                    okcases +=1
                elif (c.testresult == "NG"):
                    ngcases +=1
                
            testSummary = TestTargetFileName + self.targetCFile + "\n"
            testSummary += NumberOfTestCase  + str( len(self.testcase) )+ "\n"
            testSummary += NumberOfPassedTestCase + str( okcases ) + "\n"
            testSummary += NumberOfFailedTestCaes + str( ngcases ) + "\n"

        return testSummary.replace("\n","<br>")

    def GetCustomFunction(self):
        return self.custom_func.replace("\n","<br>")

class STATE(Enum):
    RAW = 1
    TESTCASE = 2
    ELSE =3


def CreateTestCaseDoc(resultFile,tester,date,jp):
    state = STATE.RAW
    read_file = open("./test.cpp", 'r')
    for line in read_file:
        if state == STATE.RAW :
            if re.match(ptnTESTSTART,line):
                state = STATE.TESTCASE
        elif state == STATE.TESTCASE:
            result =  re.match(ptnInclude,line)
            if result :
                if jp is True :
                    strSummary = "# 概要"
                    strDetails = "#詳細"
                    strCustomFunction = "#カスタム関数"
                else:
                    strSummary = "# Summar"
                    strDetails = "#Details"
                    strCustomFunction = "#CustomFunction"

                print(line)
                print (result.group(1))
                targetFileName = result.group(1)[3:]
                TCD = TestCaseDoc( "./"+result.group(1)+".h",targetFileName +".c" ,resultFile,tester,date)
                text = TCD.Create(jp)

                md = markdown.Markdown(extensions=["tables"]) 
                body2 = md.convert(text) 
                Summary = strSummary + "\n" + TCD.GetSummary(jp)  +"\n" + strDetails + "\n"


                md1 = markdown.Markdown()
                body1 = md1.convert(Summary)

                CustFunc = "\n"+strCustomFunction+"\n" + TCD.GetCustomFunction()
                body3 = md1.convert(CustFunc)


                html = '<html lang="ja"><meta charset="utf-8">'
                html += r"""<head><style type="text/css">
<!--
table { page-break-inside:auto; border: 1px #808080 solid; border-collapse: collapse; }
tr    { page-break-inside:avoid; page-break-after:auto ;border: 1px #808080 solid;}
td, th { border: 1px #808080 solid; }
thead { display:table-header-group }
tfoot { display:table-footer-group }
h1 { font-size:25%; border-bottom: double 5px #808080; }
h2,h3,h4,h5,h6,p {  font-size: 20%;　}

-->
</style>
</head>
<body>"""
                html += '<style> body { font-size: 8em; } </style>'
                html +=  body1 + body2 + body3 +'</body></html>'
                print(html)
                
                #html出力
                write_file = open(targetFileName+".html", 'w')
                write_file.write(html)
                write_file.close()

                # PDF出力
                # オプションを指定
                options = {
                    'page-size': 'A4',
                    'margin-top': '0.75in',
                    'margin-right': '0.75in',
                    'margin-bottom': '0.75in',
                    'margin-left': '0.75in',
                    'encoding': "UTF-8",
                    'footer-center': 'Page  [page]  of  [toPage]',
                    'footer-line':None,
                    'zoom':'1'
                }            
                pdfkit.from_string(html, targetFileName+".pdf",options = options) # --- (*4)



def parser():
    usage = 'Usage: python {} [--result TestResultText] [--tester TesterName] [--date TestDate] [--japanese] [--help]'\
            .format(__file__)
    argparser = ArgumentParser(usage=usage)
    argparser.add_argument('--result','-r', type=str,
                           help='Execution result of googletest. This is a text file obtained by redirect')
    argparser.add_argument('--tester','-t', type=str,
                           help='Tester name(your name)')
    argparser.add_argument('--date','-d', type=str,
                           help='Test Date()')
    argparser.add_argument('--japanese','-j', action='store_true',
                           help='Output Lang Japanese')

    args = argparser.parse_args()
    return args.result,args.tester,args.date,args.japanese


if __name__ == '__main__':
    result,tester,date,jp = parser()
    if result is not None:
        if  False == os.path.isfile(result) :
            print("Input --result is not file. ")
            exit()
    CreateTestCaseDoc(result,tester,date,jp)
    
    
    print(result)
