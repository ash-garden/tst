/**
 * @file 	target2.c
 * @brief	xxx
 * @author	AshGarden
 * @date	2019/04/28
 */

#include "target.h"

#ifdef UT
	void UT_otameshi( int* *a){
#else //UT
void otameshi( int* *a){
#endif //UT

	int y;
	*a = &y;
}
