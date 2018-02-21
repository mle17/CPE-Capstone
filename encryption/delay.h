/*
 * delay.h
 *
 *  Created on: Apr 12, 2017
 *      Author: Jalfredo
 */

#ifndef DELAY_H_
#define DELAY_H_
#include "msp.h"
#define FREQ_1_5_MHz 150
#define FREQ_3_MHz 300
#define FREQ_6_MHz 600
#define FREQ_12_MHz 1200
#define FREQ_24_MHz 2400
#define FREQ_48_MHz 4800

void set_HFXT()
{
    /* Enable LDO high-power mode (3V, not DC-DC cause DC-DC has switching noise */
    /* Step 1: Transition to VCORE Level 1: AM0_LDO --> AM1_LDO */
    while ((PCM->CTL1 & PCM_CTL1_PMR_BUSY));
        PCM->CTL0 = PCM_CTL0_KEY_VAL | PCM_CTL0_AMR__AM_LDO_VCORE1;
    while ((PCM->CTL1 & PCM_CTL1_PMR_BUSY));

    /* Step 2: Configure Flash wait-state to 1 for both banks 0 & 1 */
    FLCTL->BANK0_RDCTL = (FLCTL->BANK0_RDCTL & ~(FLCTL_BANK0_RDCTL_WAIT_MASK)) |
            FLCTL_BANK0_RDCTL_WAIT_1;
    FLCTL->BANK1_RDCTL  = (FLCTL->BANK0_RDCTL & ~(FLCTL_BANK1_RDCTL_WAIT_MASK)) |
            FLCTL_BANK1_RDCTL_WAIT_1;

    /* Configure pins J.2/3 for HFXT function (HFXTIN, HFXTOUT) */
    PJ->SEL0 |= BIT2 | BIT3;
    PJ->SEL1 &= ~(BIT2 | BIT3);

    /* defines arent representative of the actual frequency but don't really care
     * since we'll be using this at 24 or 48 MHz.
     */
    CS->KEY = CS_KEY_VAL;
    // CS->CTL = 0;

    /* CS_CTL2_HFXTDRIVE required for HFTX higher than HFTXFREQ */
    CS->CTL2 = CS_CTL2_HFXTFREQ_6 | CS_CTL2_HFXT_EN | CS_CTL2_HFXTDRIVE;
    CS->CTL2 &= ~CS_CTL2_HFXTBYPASS; /* for readability. don't bypass built-in HFXT crystal */

    while(CS->IFG & CS_IFG_HFXTIFG)
        CS->CLRIFG |= CS_CLRIFG_CLR_HFXTIFG;

    CS->CTL1 = CS_CTL1_SELM__HFXTCLK & ~CS_CTL1_DIVM__1; /* set MCLK as output. also need to output to pin to check freq. no division */
    // CS->CLKEN &= ~(CS_CLKEN_HSMCLK_EN | CS_CLKEN_SMCLK_EN); /* disable SMCLK and HSMCLK */
    CS->KEY = 0;

    // output MCLK and ACLK on Port4 for verification
    // ACLK - 4.2, MCLK - 4.3
    P4->DIR |= BIT2 | BIT3;
    P4->SEL0 |= BIT2 | BIT3;                // Output ACLK & MCLK
    P4->SEL1 &= ~(BIT2 | BIT3);
}

void configure_unused_ports()
{
    /* initialize all pins so power isn't wasted on possible floating pins.
     * sets all pins to output mode. output bit is don't care but initialized to 0
     * see section 12.3.2 revision H (Configuration of Unused Ports) for more information
     */
    P1->DIR = 0xFF;
    P1->OUT = 0x00;
    P2->DIR = 0xFF;
    P2->OUT = 0x00;
    P3->DIR = 0xFF;
    P3->OUT = 0x00;
    P4->DIR = 0xFF;
    P4->OUT = 0x00;
    P5->DIR = 0xFF;
    P5->OUT = 0x00;
    P6->DIR = 0xFF;
    P6->OUT = 0x00;
    P7->DIR = 0xFF;
    P7->OUT = 0x00;
    P8->DIR = 0xFF;
    P8->OUT = 0x00;
    P9->DIR = 0xFF;
    P9->OUT = 0x00;
    P10->DIR = 0xFF;
    P10->OUT = 0x00;
}

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
