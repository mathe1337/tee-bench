#ifndef RADIX_SORTMERGE_JOIN_H
#define RADIX_SORTMERGE_JOIN_H
#ifdef TIME_MUTEX
result_t* RSM (struct table_t * relR, struct table_t * relS, int nthreads, uint64_t * cpu_cntr);
#else
result_t* RSM (struct table_t * relR, struct table_t * relS, int nthreads);
#endif
#endif //RADIX_SORTMERGE_JOIN_H
