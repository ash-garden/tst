/**
 * @file 	target.h
 * @brief	xxx
 * @author	AshGarden
 * @date	2019/04/07
 */

#ifndef TARGET_H_
#define TARGET_H_


typedef struct{
	int hight;
	int low;
}T_STRUCT;


extern int function(int a);
extern int functionA(int a);
extern int functionAsub(int a,int *b);
extern void functionC(int a, T_STRUCT *s);

#endif /* TARGET_H_ */
