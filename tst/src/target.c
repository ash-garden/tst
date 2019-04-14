/**
 * @file 	target.c
 * @brief	xxx
 * @author	AshGarden
 * @date	2019/04/07
 */
#include "target.h"

// テスト対象関数
// 0を入れたら0、それ以外は1を返す


#ifdef UT
	int UT_function(int a)
#else
int function(int a)
#endif
{
	if (a == 0){
		return 0;
	} else {
		return 1;
	}
}



#ifdef UT
	int UT_functionA(int a)
#else
int functionA(int a)
#endif
{
	int ret;
	int b;
	T_STRUCT s;
	ret = functionAsub(a,&b);
	if( ret == 1 ){
		functionC(b,&s);
		return s.hight;
	}
	else{
		return ret;
	}
}

#ifdef UT
	int UT_functionAsub(int a,int *b)
#else
int functionAsub(int a,int *b)
#endif
{
	int ret;
	if(a > 0)
	{
		*b = 0x5678;
		return 0;
	}
	else{
		*b = 0x1234;
		return 1;
	}

}

#ifdef UT
	void UT_functionC(int a, T_STRUCT *s)
#else
void functionC(int a, T_STRUCT *s)
#endif
{
	s->hight = (0xFF00 & a)>>8;
	s->low   = (0xFF   & a);
}



