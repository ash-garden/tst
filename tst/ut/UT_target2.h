
/**
 * @file 	test1.h
 * @brief	xxx
 * @author	AshGarden
 * @date	2019/04/29
 */

#ifndef target2_H_
#define target2_H_

#define TARGETNAME target2_C

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

TEST_F(TARGETNAME, otameshi_1 )
{
// 名前
	TEST_CASE_NAME( xxx );
// 手順
	int* tmp;

	otameshi(&tmp);

	// 規格


}

#endif  /* target2_H_ */
