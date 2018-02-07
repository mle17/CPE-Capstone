#include <stdio.h>
#include "msp.h"
#include "delay.h"


/**
 * main.c
 */


const int freq = FREQ_24_MHz;

unsigned long long PowerMod(unsigned long long x , unsigned long long p, unsigned long long N) {
    unsigned long long A = 1;
    unsigned long long m = p;
    unsigned long long t = x;
    unsigned long long k ,r;

    while( m > 0 ){
        k = m / 2;
        r = m - 2 * k;
        if ( r == 1 ){
            A = (A * t) % N;
        }
//        delayMs(10, freq);
        t = (t * t) % N;
        m = k;
    }

    return A;
}

/*
/*
32 bit
P:2835473779

Q:3154257031

N:8943813103626890149

Mod:1490635516272859890

d:636903973735029413

cipher:1120636163711549706
123456

16 bit
P:61627

Q:45757

N:2819866639

Mod:469959876

d:265897313

cipher:1236341142
123456
*/

void main(void) {
    WDT_A->CTL = WDT_A_CTL_PW | WDT_A_CTL_HOLD;     // stop watchdog timer

    const unsigned long long HARD_INPUT = 123456;
    const unsigned long long EXPECTED_OUTPUT = 1236341142;

    const unsigned long long varE = 65537;
    const unsigned long long varN = 2819866639;
    const unsigned long long varMod = 469959876;
    const unsigned long long varD = 265897313;
    unsigned long long encrypt, decrypt;

    P2->SEL1 &= ~BIT1;
    P2->SEL0 &= ~BIT1;
    P2->DIR |= BIT1;

    P4->DIR |= BIT3;
    P4->OUT &= ~BIT3;

    set_DCO(freq);

    TIMER_A0->CCTL[0] = TIMER_A_CCTLN_CCIE; // TACCR0 interrupt enabled
    TIMER_A0->CCR[0] = 7500;
    TIMER_A0->CTL = TIMER_A_CTL_SSEL__SMCLK | // SMCLK, continuous mode
            TIMER_A_CTL_MC__CONTINUOUS;

    SCB->SCR &= ~SCB_SCR_SLEEPONEXIT_Msk;   // Wake up on exit from ISR

    // Enable global interrupt
    __enable_irq();

    NVIC->ISER[0] = 1 << ((TA0_0_IRQn) & 31);

    encrypt = PowerMod(HARD_INPUT, varE, varN);
    decrypt = PowerMod(encrypt, varD, varN);

//    printf("64 bits? : %d", (int)sizeof(unsigned long long));
    printf("Encrypted : %d, Expected : %d\n", encrypt, EXPECTED_OUTPUT);
    printf("Decrypted : %d, Expected : %d\n", decrypt, HARD_INPUT);

    while(1) {
        __sleep();
        P2->OUT |= BIT1;
        encrypt = PowerMod(HARD_INPUT, varE, varN);
        // printf("Encrypted : %d, Expected : %d\n", encrypt, EXPECTED_OUTPUT);
        P2->OUT &= ~BIT1;
        encrypt = 0;
        TIMER_A0->CCR[0] += 7500;              // Add Offset to TACCR0
        // printf("Reset\n");
    }
}

void TA0_0_IRQHandler(void) {
    TIMER_A0->CCTL[0] &= ~TIMER_A_CCTLN_CCIFG;
}
