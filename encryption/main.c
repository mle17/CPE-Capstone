#include <stdio.h>
#include <stdlib.h>
#include "imath.h"
#include "msp.h"
#include "delay.h"

#define BASE    16

/**
 * main.c
 * Only needs imath.c
 */
const int freq = FREQ_24_MHz;

void main(void) {
    WDT_A->CTL = WDT_A_CTL_PW | WDT_A_CTL_HOLD;     // stop watchdog timer

    printf("Init\n");
    set_HFXT();
    printf("HFXT enabled\n");
    //configure_unused_ports();
    printf("Disabled unused ports\n");
    /* imath stuff */
    mpz_t  input, e, n, d, encrypt, decrypt;
//    char  *buf;
//    int    len;

    /* Initialize a new zero-valued mpz_t structure */
    mp_int_init(&n);
    mp_int_init(&d);
    mp_int_init(&encrypt);
    mp_int_init(&decrypt);

    /* Initialize a new mpz_t with a small integer value */
    mp_int_init_value(&input, 123456);
    mp_int_init_value(&e, 65537);

    /* N and d for different sizes
     * Works:
     * 64   N: 8ff3d1240677272eb239818d5a080b97
     * 64   d: 1b626019fa5416d3007fdf09c216b9
     * 128  N: 99766c280d75d2e1dcb3f5cc878e61a858fa60c6c2de2befa63c202a8b0fcf83
     * 128  d: a36ffa1d012c0c56e2c1997458a3cc5f74532248cc36759d346ee18ef80179d
     * 256  N: 8e7075a2a26c7dee7b67b63e62cad1a8d141dc18e4d6315e998147b56c2fdb788b49e73d90e16e4cc49f580825076054e6ee08e69fcad21491c2885522daf2a9
     * 256  d: a97de87cbe099b504c47fcf3ff5a9860e9a014e70a665618db509aa3a738cb4dbe2123fde5ba07c081b0ebf8fc37e98b326ac61f7e1655c71cc18ead2ecec01
     * Doesn't work:
     * 512  N: 96072e1e996ae4ff4ced88b87ed2fd809d3759d4d674c7a64f08f04c456a6a2c257b791cf9f8832510cc386002a8525aed665bce943ab548d760d8a7214ed0fadf334c5ee7f01f3288f017291faf5cb434a0d423475f4143b8f513b67df15e05ea1feee3e08f14463f0fc37869c0e1897f240c9d603bda544654785460adad51
     * 512  d: 1723d1def9da452a447701a6b536fd4f2450987c2dbcb2db89a6af0b908c56866b1c95845ce0d1f77a55095ff3a0fb1cd7af793b0e5d54bf40ab09179419583d90b5a07030a9377564335b447d7fe7f767efddcd24940482e0a5a1cece8f9e13d1f6b3bca4ac296f21d9a83b20e7fa51e97c3c0d92fa2c54746faafe4766593d
     * 1024 N: 880305c7a47899cd394ef9e802214ad996478b85077952b31f4250332d8b675189bd398c21795f8f72dae11084d69ebe0bca34810f395d857a8fc49fc389e2d4467ab9404f019d56f246f4eab9e05acf42153ab6f1422758e6c92787324acfb0fc5b4d49c4cb5be2ed3e72e8511e86b132ef2db4c65fb7d5f367617752c1714937569add661be61f3cc37ffcb88b79640f4d5944d996a0f38e79ff9cb944d930e04ac0b13240f11e1fef842ac63c7713061d6e54ac8c5272da2efbe73c4f62e1af3df4b8016c1fc4bedb9c7ecf6bdd91f78c81b3882b4c976aadc356b68261311ec10e058ab9795a3e2e545017fdd2966dec1e7fa7c559e2dc32d0b591734d65
     * 1024 d: 1cec079e9c6ac8c9cb15f02e55c59e95064fd06b495b932a63cb46229bdcb8ebadce7f1e3d4002020efa5c4196fdcc63bd3e124c1f60a3726ecd839235926c99972321a17b2b6cb9c06b3649739d31b240eb22c1242c5d119a81cbd603ebc49e6e0b3c342394dac5368dc10185be6805e63ed6094ae5afc1df306c99630f9f77128c878f82ca0c6c410003aacfc6489d4582ce1c529af0f3cd9f9de6abc70391d37d474e73da0a6c50d6a89540cf10d5a0d1f7c7ac6300ce6eb241fbb760bd74ed0680fe152f97e8b7dc351ee2e469e382461959e33d576fe64a3574414283ab37052db0ea1dc19dad14abb2eab2c6b5d768f4ace9d104c263c30576eb49d41
     */

    /* Initialize a new mpz_t with a string value in base BASE */
//    printf("Read in N\n");
    mp_int_read_string(&n, BASE, "8ff3d1240677272eb239818d5a080b97");
//    printf("Read in d\n");
    mp_int_read_string(&d, BASE, "1b626019fa5416d3007fdf09c216b9");

    P2->SEL1 &= ~BIT1;
    P2->SEL0 &= ~BIT1;
    P2->DIR |= BIT1;

    // set_DCO(freq);
    //TIMER_A0->CCTL[0] = TIMER_A_CCTLN_CCIE; // TACCR0 interrupt enabled
    //TIMER_A0->CCR[0] = 7500;
    //TIMER_A0->CTL = TIMER_A_CTL_SSEL__SMCLK | // SMCLK, continuous mode
            //TIMER_A_CTL_MC__CONTINUOUS;

    SCB->SCR &= ~SCB_SCR_SLEEPONEXIT_Msk;   // Wake up on exit from ISR

    // Enable global interrupt
    // __enable_irq();

    // NVIC->ISER[0] = 1 << ((TA0_0_IRQn) & 31);

//    printf("Encrypting\n");
    //mp_int_exptmod(&input, &e, &n, &encrypt); /* encrypt = input^e % n */
//    mp_int_free(&e);
//    mp_int_free(&input);
//    printf("Decrypting\n");
    //mp_int_exptmod(&encrypt, &d, &n, &decrypt); /* decrypt = encrypt^d % n */

//    printf("Trying to print\n");

//    len = mp_int_string_len(&encrypt, BASE);
//    buf = calloc(len, sizeof(*buf));
//    mp_int_to_string(&encrypt, BASE, buf, len);
//
//    printf("Encrypted : %s\n", buf);

//    len = mp_int_string_len(&decrypt, BASE);
//    buf = calloc(len, sizeof(*buf));
//    mp_int_to_string(&decrypt, BASE, buf, len);
//
//    printf("Decrypted : %s ?= 1E240\n", buf); // 123456 = 0x1E240

//    free(buf);

    while(1) {
        // printf("LED on\n");
        // __sleep();
        P2->OUT |= BIT1;
//        printf("loop\n");
        //mp_int_zero(&decrypt);
        mp_int_exptmod(&input, &e, &n, &encrypt);
        // mp_int_exptmod(&encrypt, &d, &n, &decrypt);
        P2->OUT &= ~BIT1;
    }
}

void TA0_0_IRQHandler(void) {
    TIMER_A0->CCTL[0] &= ~TIMER_A_CCTLN_CCIFG;
    TIMER_A0->CCR[0] += 7500;              // Add Offset to TACCR0
}
