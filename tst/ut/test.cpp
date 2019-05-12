
/**
 * @file 	test.cpp
 * @brief	xxx
 * @author	AshGarden
 * @date	2019/04/29
 */

#include "gtest/gtest.h"

extern "C" {
#include "src/target.h"
#include "fff.h"
#include "fake.h"
DEFINE_FFF_GLOBALS;
}

//TEST START
#include "UT_target.h"
#include "UT_target2.h"
