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
#else //UT
int function(int a)
#endif //UT
{
	if (a == 0){
		return 0;
	} else {
		return 1;
	}
}



#ifdef UT
	int UT_functionA(int a)
#else //UT
int functionA(int a)
#endif //UT
{
	int ret;
	int b;
	unsigned int tmp[][3]={{0,1,0},{2,3,2},{4,5,4}};
	T_STRUCT s;
	ret = functionAsub(a,&b);
	if( ret == 1 ){
		functionC(b,&s,0,tmp);
		return s.hight;
	}
	else{
		return ret;
	}
}

#ifdef UT
	int UT_functionAsub(int a,int *b)
#else //UT
int functionAsub(int a,int *b)
#endif //UT
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
	void UT_functionC(int a, T_STRUCT *s,unsigned long b,unsigned int abc[3][3])
#else //UT
void functionC(int a, T_STRUCT *s,unsigned long b,unsigned int abc[3][3])
#endif //UT
{
	s->hight = (0xFF00 & a)>>8;
	s->low   = (0xFF   & a);
	int *x;
	otameshi(&x);
}

