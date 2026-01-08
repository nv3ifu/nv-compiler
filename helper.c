#include <stdio.h>

void print_i32(int val) { printf("print_i32: %d\n", val); }

void print_f64(double val) { printf("print_f64: %f\n", val); }

void print_i1(int val) { printf("print_i1: %s\n", (val ? "true" : "false")); }
