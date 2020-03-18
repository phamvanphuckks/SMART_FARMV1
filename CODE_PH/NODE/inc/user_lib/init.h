#ifndef __INIT_H__
#define __INIT_H__

#include "stm32l1xx_rcc.h"
#include "stm32l1xx_gpio.h"
#include "stm32l1xx_usart.h"

extern GPIO_InitTypeDef gpio_Init;
extern USART_InitTypeDef usart_Init;

void InitPinEN_config(void);
void Uart1_config(void);
void Uart2_config(void);
void Uart3_config(void);

void Lora_PowerOn(void);
void ADC_Enable(uint8_t en);
void LORA_Enable(uint8_t en);


#endif
