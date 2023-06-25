//
// Created by so81egih on 28/02/2023.
//
#include <cstdint>
#ifndef SGX_ENCRYPTEDDB_RDTSCPWRAPPER_H
#define SGX_ENCRYPTEDDB_RDTSCPWRAPPER_H

inline uint64_t rdtscp(uint32_t &aux) {
uint64_t rax, rdx;
asm volatile ( "rdtscp\n"  : "=a" (rax), "=d" (rdx), "=c" (aux) : : );
return (rdx << 32) + rax;

}

class rdtscpWrapper{
private:
    uint64_t* cntr;
    uint32_t aux;
    uint64_t start;
    uint64_t end;
public:
    rdtscpWrapper(uint64_t *cntr):cntr(cntr) {
        start = rdtscp(aux);
    }

    ~rdtscpWrapper() {
        end = rdtscp(aux);
        *cntr += end - start;
    }

};

/*
class rdtscpCounter{
private:
    uint64_t cntr;
    uint32_t aux;
    uint64_t start;
    uint64_t end;
    bool paused;
public:
    rdtscpCounter(){
        cntr = 0;
        start = 0;
    }
    void start(){
        paused = false;
        start = rdtscp(aux);
    }
    uint64_t stop(){
        cntr += rdtscp(aux) - start;
        return cntr;
    }
    void pause(){
        cntr += rdtscp(aux) - start;
        paused = true;
    }
    void reset(){
        start = 0;
        cntr = 0;
    }
};
*/
#endif //SGX_ENCRYPTEDDB_RDTSCPWRAPPER_H

