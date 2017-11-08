#include <stdio.h>
#include "msp.h"
#include "delay.h"


/**
 * main.c
 */


int PowerMod(int x , int p, int N) {
    int A = 1;
    int m = p;
    int t = x;
    int k ,r;

    while( m > 0 ){
        k = m / 2;
        r = m - 2 * k;
        if ( r == 1 ){
            A = (A * t) % N;
        }
        t = (t * t) % N;
        m = k;
    }

    return A;
}


void main(void) {
    WDT_A->CTL = WDT_A_CTL_PW | WDT_A_CTL_HOLD;     // stop watchdog timer

    const int HARD_INPUT = 123;
    const int EXPECTED_OUTPUT = 5275;

    const int varE = 449;
    const int varN = 9797;
    // const int varR = 9600;
    int freq = FREQ_24_MHz;
    int encrypt, decrypt;

    P2->SEL1 &= ~BIT1;
    P2->SEL0 &= ~BIT1;
    P2->DIR |= BIT1;

    P4->SEL1 &= ~BIT2;
    P4->SEL0 &= ~BIT2;
    P4->DIR |= BIT3;
    P4->OUT &= ~BIT3;

    set_DCO(freq);

    encrypt = PowerMod(HARD_INPUT, varE, varN);
    decrypt = PowerMod(encrypt, varE, varN);

//    printf("Encrypted : %d, Expected : %d\n", encrypt, EXPECTED_OUTPUT);
//    printf("Decrypted : %d, Expected : %d\n", decrypt, HARD_INPUT);

    while(1) {
        delayMs(500, freq);
        P2->OUT |= BIT1;
        encrypt = PowerMod(HARD_INPUT, varE, varN);
        // printf("Encrypted : %d, Expected : %d\n", encrypt, EXPECTED_OUTPUT);
        P2->OUT &= ~BIT1;
        encrypt = 0;
        // printf("Reset\n");

    }
}
