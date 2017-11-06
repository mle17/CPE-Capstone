#include <stdio.h>
#include "msp.h"
#include "delay.h"


/**
 * main.c
 */


int PowerMod (int x , int p, int N){
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


void main(void)
{
	WDT_A->CTL = WDT_A_CTL_PW | WDT_A_CTL_HOLD;		// stop watchdog timer

	const int HARD_INPUT = 123;
	// const int EXPECTED_OUTPUT = 5275;

	const int varE = 449;
	const int varN = 9797;
	// const int varR = 9600;

	printf("%d\n",PowerMod( HARD_INPUT, varE, varN ));

	int freq = FREQ_24_MHz;
	P2->SEL1 &= ~2;
	P2->SEL0 &= ~2;
	P2->DIR |= 2;

	while( 1 ){
	    P2->OUT |= 2;
	    delayNs(5000, freq);
	    P2->OUT &= ~2;
	    delayNs(5000,freq);

	}
}

