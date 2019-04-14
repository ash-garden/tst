/**
 * @file 	fake.h
 * @brief	xxx
 * @author	AshGarden
 * @date	2019/04/13
 */

#ifndef FAKE_H_
#define FAKE_H_

#if 0
extern int UT_functionA(int a);
extern int UT_functionAsub(int a,int *b);

FAKE_VALUE_FUNC(int,functionA,int );
FAKE_VALUE_FUNC(int,functionAsub,int ,int*);
#else
#define		CFAKE_VALUE_FUNC(ret,name,...)	\
	extern	ret	UT_##name(__VA_ARGS__);		\
	FAKE_VALUE_FUNC(ret,name,__VA_ARGS__);
#define		CFAKE_VOID_FUNC(name,...)		\
	extern	void UT_##name(__VA_ARGS__);	\
	FAKE_VOID_FUNC(name,__VA_ARGS__)

CFAKE_VALUE_FUNC(int,functionA,int);
CFAKE_VALUE_FUNC(int,functionAsub,int ,int*);
CFAKE_VOID_FUNC(functionC,int,T_STRUCT*);

#endif

#define  FFF_FAKES_LIST( FAKE ) \
do{ \
	FAKE ( functionA )		\
	FAKE ( functionAsub )	\
	FAKE ( functionC )		\
}while(0)

#endif /* FAKE_H_ */
