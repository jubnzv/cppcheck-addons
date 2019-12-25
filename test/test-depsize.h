#include <stdint.h>

struct A {
    int a;
    unsigned int b;
    uint32_t c;
};

struct B {
    struct A a;
    uint32_t b;
};

typedef struct {
    int a;
    unsigned int b;
} A_t;
