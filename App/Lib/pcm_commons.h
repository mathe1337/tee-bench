#ifndef SGXJOINEVALUATION_PCM_COMMONS_H
#define SGXJOINEVALUATION_PCM_COMMONS_H


#ifdef PCM_COUNT
#include "cpucounters.h"
using namespace pcm;
void ensurePmuNotBusy(PCM *m, bool forcedProgramming);
#endif

#ifdef NATIVE_COMPILATION
void ocall_set_system_counter_state(const char *message);
void ocall_get_system_counter_state(const char *message, int start_to_end);
#endif

#endif //SGXJOINEVALUATION_PCM_COMMONS_H
