/**
 * @file 	test.cpp
 * @brief	xxx
 * @author	AshGarden
 * @date	2019/04/07
 */


// テストケース記述ファイル
#include "gtest/gtest.h" // googleTestを使用するおまじないはこれだけでOK
// テスト対象関数を呼び出せるようにするのだが
// extern "C"がないとCと解釈されない、意外とハマりがち。
extern "C" {
#include "src/target.h"
#include "fff.h"
#include "fake.h"

DEFINE_FFF_GLOBALS;
}

#define TEST_CASE_NAME(x)	// x


// fixtureNameはテストケース群をまとめるグループ名と考えればよい、任意の文字列
// それ以外のclass～testing::Testまではおまじないと考える
class fixtureName : public ::testing::Test {
protected:
	// fixtureNameでグループ化されたテストケースはそれぞれのテストケース実行前に
	// この関数を呼ぶ。共通の初期化処理を入れておくとテストコードがすっきりする
	virtual void SetUp(){
		FFF_FAKES_LIST(RESET_FAKE);
		FFF_RESET_HISTORY();
	}
	// SetUpと同様にテストケース実行後に呼ばれる関数。共通後始末を記述する。
	virtual void TearDown(){
	}
};
#if 0
// 成功するテストケース。細かい説明はGoogleTestのマニュアルを見てね。
TEST_F(fixtureName, testOk)
{
    EXPECT_EQ(0, function(0));
    EXPECT_EQ(1, function(100));
}
// あえて失敗するテストケースも書いておく。
TEST_F(fixtureName, testNg)
{
    EXPECT_EQ(1, function(0));
    EXPECT_EQ(0, function(100));
}
#endif




TEST_F(fixtureName, functionAsub_1)
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

TEST_F(fixtureName, functionAsub_2 )
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
void custmfunctionC(int cc , T_STRUCT* ss){
	ss->hight = 0xAB;
}
TEST_F(fixtureName, functionA_1 )
{
// 名前
	TEST_CASE_NAME( "functionAsub の戻り値が1" );
// 手順
	int a;
	int ret;
	a = 0;
	functionAsub_fake.return_val = 1;

	functionC_fake.custom_fake = custmfunctionC;

	ret = UT_functionA(a);

// 規格
	EXPECT_EQ(a,functionAsub_fake.arg0_val);
	EXPECT_EQ(*((int*)(functionAsub_fake.arg1_val)),functionC_fake.arg0_val);
	EXPECT_EQ(ret,0xAB);

}

TEST_F(fixtureName, functionA_2 )
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


TEST_F(fixtureName, functionC_1 )
{
// 名前
	TEST_CASE_NAME( "" );
// 手順
	T_STRUCT st;

	UT_functionC(0x12345678,&st);

// 規格
	EXPECT_EQ(st.hight,0x56);
	EXPECT_EQ(st.low  ,0x78);
}

