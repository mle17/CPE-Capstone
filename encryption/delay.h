#ifndef DELAY_H_
#define DELAY_H_
#include "msp.h"

void set_HFXT() // decrease this and decrease key size to allow for more accurate scope capture (maybe)
                //also should make sure LED doesnt pull from 3.3v line if tapping out
{
    /* Enable LDO high-power mode (3V, not DC-DC cause DC-DC has switching noise */
    /* Step 1: Transition to VCORE Level 1: AM0_LDO --> AM1_LDO */
    while ((PCM->CTL1 & PCM_CTL1_PMR_BUSY));
    PCM->CTL0 = PCM_CTL0_KEY_VAL | PCM_CTL0_AMR__AM_LDO_VCORE1;
    //PCM->CTL0 = PCM_CTL0_KEY_VAL | PCM_CTL0_AMR__AM_DCDC_VCORE1; // this is tapped out. doesnt work
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

    while(CS->IFG & CS_IFG_HFXTIFG)
        CS->CLRIFG |= CS_CLRIFG_CLR_HFXTIFG;

    CS->CTL1 = CS_CTL1_SELM__HFXTCLK | CS_CTL1_DIVM__128; /* set MCLK as output. also need to output to pin to check freq. no division */
    CS->KEY = 0;
}

void configure_unused_ports()
{
    /* initialize all pins so power isn't wasted on possible floating pins.
     * sets all pins to output mode. output bit is don't care but initialized to 0
     * see section 12.3.2 revision H (Configuration of Unused Ports) for more information */
    P1->DIR = 0x00; /* set all as input */
    P1->REN = 0xFF; /* enable resistor pull up / pull down */
    P1->OUT = 0x00; /* pull down to ground */
    P2->DIR = 0x00; /* set all as input */
    P2->REN = 0xFF; /* enable resistor pull up / pull down */
    P2->OUT = 0x00; /* pull down to ground */
    P3->DIR = 0x00; /* set all as input */
    P3->REN = 0xFF; /* enable resistor pull up / pull down */
    P3->OUT = 0x00; /* pull down to ground */
    P4->DIR = 0x00; /* set all as input */
    P4->REN = 0xFF; /* enable resistor pull up / pull down */
    P4->OUT = 0x00; /* pull down to ground */
    P5->DIR = 0x00; /* set all as input */
    P5->REN = 0xFF; /* enable resistor pull up / pull down */
    P5->OUT = 0x00; /* pull down to ground */
    P6->DIR = 0x00; /* set all as input */
    P6->REN = 0xFF; /* enable resistor pull up / pull down */
    P6->OUT = 0x00; /* pull down to ground */
    P7->DIR = 0x00; /* set all as input */
    P7->REN = 0xFF; /* enable resistor pull up / pull down */
    P7->OUT = 0x00; /* pull down to ground */
    P8->DIR = 0x00; /* set all as input */
    P8->REN = 0xFF; /* enable resistor pull up / pull down */
    P8->OUT = 0x00; /* pull down to ground */
    P9->DIR = 0x00; /* set all as input */
    P9->REN = 0xFF; /* enable resistor pull up / pull down */
    P9->OUT = 0x00; /* pull down to ground */
    P10->DIR = 0x00; /* set all as input */
    P10->REN = 0xFF; /* enable resistor pull up / pull down */
    P10->OUT = 0x00; /* pull down to ground */
}

/* Arbitrary busy delay function recycled from previous projects */
void delayMs(int n,int f) {
    int i, j;

    for (j = 0; j < n; j++)
        for (i = f; i > 0; i--);
}

#endif /* DELAY_H_ */
