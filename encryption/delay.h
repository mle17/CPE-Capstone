/*
 * delay.h
 *
 *  Created on: Apr 12, 2017
 *      Author: Jalfredo
 */

#ifndef DELAY_H_
#define DELAY_H_
#define FREQ_1_5_MHz 150
#define FREQ_3_MHz 300
#define FREQ_6_MHz 600
#define FREQ_12_MHz 1200
#define FREQ_24_MHz 2400
#define FREQ_48_MHz 4800

void set_DCO(int f)
{
    CS->KEY = CS_KEY_VAL;
    CS->CTL0 = 0;

    /* set the clock freq */
    switch(f)
    {
        case FREQ_1_5_MHz:
            CS->CTL0 = CS_CTL0_DCORSEL_0;
            break;
        case FREQ_3_MHz:
            CS->CTL0 = CS_CTL0_DCORSEL_1;
            break;
        case FREQ_6_MHz:
            CS->CTL0 = CS_CTL0_DCORSEL_2;
            break;
        case FREQ_12_MHz:
            CS->CTL0 = CS_CTL0_DCORSEL_3;
            break;
        case FREQ_24_MHz:
            CS->CTL0 = CS_CTL0_DCORSEL_4;
            break;
        case FREQ_48_MHz:
            CS->CTL0 = CS_CTL0_DCORSEL_5;
            break;
        default:
            CS->CTL0 = CS_CTL0_DCORSEL_1;
    }

    CS->CTL1 = CS_CTL1_SELA_2 | CS_CTL1_SELS_3 | CS_CTL1_SELM_3;
    CS->KEY = 0;
}
/* delay milliseconds when system clock is at 3 MHz for Rev C MCU */
void delayMs(int n,int f) {
    int i, j;

    for (j = 0; j < n; j++)
        for (i = f; i > 0; i--);      /* Delay 1 ms*/
}

void delayNs(int n,int f) {
    n /= 10000; /* assuming minimal input is 10000ns as lower input will be impossible*/
    f /= 100;   /* faster than 10us which too close to max speed of 1us with 24Mhz clock speed */
    int j,i;

    for (j = 0; j < n; j++)
        for (i = f; i > 0; i--);      /* Delay 1 ns-ish */
    /* delay 1ns */
}



#endif /* DELAY_H_ */
