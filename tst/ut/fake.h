/**
* @file 	fake.h
* @note    This file Created by FakeFunctionCreate.py	
* @author	AshGarden
* @date	2019/04/28
*/

#ifndef FAKE_H_
#define FAKE_H_

#define		CFAKE_VALUE_FUNC(ret,name,...)	\
    extern	ret	UT_##name(__VA_ARGS__);		\
    FAKE_VALUE_FUNC(ret,name,__VA_ARGS__);
#define		CFAKE_VOID_FUNC(name,...)		\
    extern	void UT_##name(__VA_ARGS__);	\
    FAKE_VOID_FUNC(name,__VA_ARGS__)
#define REAL_FUNC(x) x##_fake.custom_fake = UT_##x;
#define FAKE_FUNC(x) x##_fake.custom_fake = NULL;
#define TEST_CASE_NAME(x)	// x

CFAKE_VALUE_FUNC(int,function,int);
CFAKE_VALUE_FUNC(int,functionA,int);
CFAKE_VALUE_FUNC(int,functionAsub,int,int *);
CFAKE_VOID_FUNC(functionC,int,T_STRUCT *,unsigned long,unsigned int *);
CFAKE_VOID_FUNC(otameshi,int* *);

#define  FFF_FAKES_LIST( FAKE ) \
do{ \
	 FAKE(function)	\
	 FAKE(functionA)	\
	 FAKE(functionAsub)	\
	 FAKE(functionC)	\
	 FAKE(otameshi)	\
}while(0)

#endif /* FAKE_H_ */