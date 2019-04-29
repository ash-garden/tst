
/**
 * @file 	test1.h
 * @brief	xxx
 * @author	AshGarden
 * @date	2019/04/29
 */

#ifndef target_H_
#define target_H_

#define TARGETNAME target_C

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

TEST_F(TARGETNAME, functionC_1 )
{
// 名前
	TEST_CASE_NAME( "" );
// 手順
	T_STRUCT st;

	UT_functionC(0x12345678,&st,0,NULL);

// 規格
	EXPECT_EQ(st.hight,0x56);
	EXPECT_EQ(st.low  ,0x78);

}

TEST_F(TARGETNAME, functionAsub_1)
{
// 名前
	TEST_CASE_NAME("a>0");
// 手順
	int b;
	int ret;
	ret = UT_functionAsub(1,&b);
// 規格
	EXPECT_EQ(0,ret);
	EXPECT_EQ(0x5678,b);
}

TEST_F(TARGETNAME, functionAsub_2 )
{
// 名前
	TEST_CASE_NAME( "a<=0" );
// 手順
	int a;
	int b;
	int ret;
	a = 0;
	ret = UT_functionAsub(a,&b);

// 規格
	EXPECT_EQ(ret,1);
	EXPECT_EQ(b,0x1234);

}
void custmfunctionC(int cc , T_STRUCT* ss,unsigned long b,unsigned int *){
	ss->hight = 0xAB;
}
TEST_F(TARGETNAME, functionA_1 )
{
// 名前
	TEST_CASE_NAME( "functionAsub の戻り値が1" );
// 手順
	int a;
	int ret;
	a = 0;
	functionAsub_fake.return_val = 1;

	//functionC_fake.custom_fake = custmfunctionC;

	ret = UT_functionA(a);

// 規格
	EXPECT_EQ(a,functionAsub_fake.arg0_val);
	EXPECT_EQ(*((int*)(functionAsub_fake.arg1_val)),functionC_fake.arg0_val);
	EXPECT_EQ(ret,0xAB);

}

TEST_F(TARGETNAME, functionA_2 )
{
// 名前
	TEST_CASE_NAME( "functionAsubの戻り値が0以外" );
// 手順
	int ret;
	int a;
	a=1;
	functionAsub_fake.return_val = 0;
	ret = UT_functionA(a);

// 規格
	EXPECT_EQ(functionAsub_fake.arg0_val,a);
	EXPECT_EQ(ret,0);

}

TEST_F(TARGETNAME, functionA_3 )
{
// 名前
	TEST_CASE_NAME( "functionAsubの戻り値が0以外" );
// 手順
	int ret;
	int a;
	a=1;
	FAKE_FUNC(functionAsub)
	functionAsub_fake.return_val = 0;
	ret = UT_functionA(a);

// 規格
	EXPECT_EQ(functionAsub_fake.arg0_val,a);
	EXPECT_EQ(ret,0);

}


#endif  /* target_H_ */
