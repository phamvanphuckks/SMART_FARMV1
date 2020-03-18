#include <stdio.h>
#include <stdlib.h>

#include "delay.h"
#include "init.h"
#include "usart.h"
#include "lora.h"
#include "stm32l1xx_adc.h"

#define SIZE                256
#define Offset              0.0           // deviation compensate - Check to ensure the error does not exceed 0.3.
#define ArrayLenth          50    

int pHArray[ArrayLenth];   // Store the average value of the sensor feedback
void ADC_Configuration(void);
double avergearray(int* arr, int number);

double voltage = 0.0, pHValue = 0.0, getvalue = 0.0;


/*define pin LEDs*/
#define         LED             GPIO_Pin_8 

char UID_TX[SIZE]= "G01";
char TX_buf[SIZE];

volatile uint8_t old_buf  = 0x00;
volatile uint8_t RxBuffer = 0x00, array[8];
int i = 0, j=0;
char Buffer[7], Battery[7], Battery_1[7]="0";
uint8_t en = 1, start = 0;


int main(){
    
	SystemClock_Config();
	SystemCoreClockUpdate();
	Systick_init();

	InitPinEN_config();
	
	Uart1_config();
	Uart2_config();
	delay_ms(1500);
	Uart3_config();
	
/*
		Hàm LORA_Enable() và ADC_Enable()
		Chua biet truyen vao 0 hay 1 no moi enable
		Kha nang cao la 2 cai lech nhau 
		Do 1 chan MOSFET cua Lora - VCC,  1 chan dau voi VDK
			 1 chan MOSFET cua ADC  - GND,  1 chan dau voi VDK
	
		Test 4 TH : 11,10,01,00
*/	
	
	Lora_PowerOn();	
	LORA_Enable(1);
	lora_enterTestMode();

	ADC_Enable(1);
	ADC_Configuration();
	delay_ms(1000);
	
	while(1){
			/*doc pin*/
			UART_PutStr(USART2, "AT+VDD\r\n");
			delay_ms(100);	
			if(en==1){
					memcpy(Battery, Buffer + 5, 4);
					strcpy(Battery_1, Battery);
		 
					//UART_PutStr(USART1,Battery_1);
					memset(Battery, 0, sizeof(Battery));
					memset(Buffer, 0, sizeof(Buffer));
					
					USART_ITConfig(USART2, USART_IT_RXNE, ENABLE);
					en  = 0;
			}
	 
			/*doc PH*/
			getvalue = avergearray(pHArray, 20);
			voltage  = (getvalue/1024.0)*3.3;// read the voltage - VREF+ : 3.3V
			pHValue  =	(int)3.5*((int)voltage) + Offset;
			
			/*gui du lieu qua Lora*/
			sprintf(TX_buf,"%s_%d_%s\n", UID_TX, (int)pHValue, Battery_1);				
			lora_enterTestMode();
			printf("AT+TEST=TXLRSTR,%s\r\n", TX_buf);

			memset(Battery_1, 0, sizeof(Battery_1));
			delay_ms(1000);
			GPIO_ToggleBits(GPIOB, LED);
//	    printf("AT\r\n");
	}    
}

void USART2_IRQHandler(){
	volatile uint8_t RxBuffer = (uint8_t)USART_GetChar(USART2);
	UART_SendChar(USART1, RxBuffer);
    if(old_buf == 0x2B && RxBuffer == 0x56){
        start = 1;
	}
	if(start == 1){
			Buffer[j] = RxBuffer;
			j++;
			if(Buffer[j-1] == '\n'){
					j = 0;
					start = 0;
					en = 1;
					USART_ITConfig(USART2, USART_IT_RXNE, DISABLE);
			}
	}
	old_buf = RxBuffer;
}

void USART3_IRQHandler(){
	RxBuffer = (uint8_t)USART_ReceiveData(USART3);
	array[i] = RxBuffer;
	i++;
	if(i==7) i=0;
}

void ADC_Configuration(){
	ADC_InitTypeDef			 			ADC_InitStructure;
	ADC_CommonInitTypeDef 		ADC_CommonInitStructure;
	GPIO_InitTypeDef 					GPIO_InitStructure;

	/*enable clock*/
	RCC_APB2PeriphClockCmd(RCC_APB2Periph_ADC1, ENABLE);
	RCC_AHBPeriphClockCmd(RCC_AHBPeriph_GPIOB,ENABLE);

	// PB0: ADC1-CH8
	GPIO_InitStructure.GPIO_Pin = GPIO_Pin_0;
	GPIO_InitStructure.GPIO_Mode = GPIO_Mode_AN;
	GPIO_InitStructure.GPIO_PuPd = GPIO_PuPd_NOPULL ;
	GPIO_Init(GPIOB, &GPIO_InitStructure);

	/* ADC Common Init **********************************************************/
	ADC_CommonInitStructure.ADC_Prescaler = ADC_Prescaler_Div4; /*Bo chia clock*/

	ADC_CommonInit(&ADC_CommonInitStructure);
	/* ADC1 Init ****************************************************************/
	ADC_InitStructure.ADC_Resolution = ADC_Resolution_10b; // xem lai
	ADC_InitStructure.ADC_ScanConvMode = DISABLE;
	ADC_InitStructure.ADC_ContinuousConvMode = ENABLE;
	ADC_InitStructure.ADC_ExternalTrigConvEdge = ADC_ExternalTrigConvEdge_None;
	ADC_InitStructure.ADC_ExternalTrigConv = ADC_ExternalTrigConv_T2_CC2;
	ADC_InitStructure.ADC_DataAlign = ADC_DataAlign_Right;
	ADC_InitStructure.ADC_NbrOfConversion = 1;
	ADC_Init(ADC1, &ADC_InitStructure);

	/* ADC1 regular channel configuration **************************************/
	ADC_RegularChannelConfig(ADC1, ADC_Channel_8, 1, ADC_SampleTime_4Cycles);
	/* Enable ADC */
	ADC_Cmd(ADC1, ENABLE);
	/* Start ADC Software Conversion */ 
	ADC_SoftwareStartConv(ADC1);
}

double avergearray(int* arr, int number){
  int i=0, j=0;
  int max, min;
  double avg;
  long amount = 0;
	// sampling 
	while(j < number){
        arr[j] = ADC_GetConversionValue(ADC1);
		j++;
	}
  if(number <= 0) return 0;
  if(number < 5){   //less than 5, calculated directly statistics
    for(i = 0;i < number;i++){
      amount += arr[i];
    }
    avg = amount/number;
    return avg;
  }
  else{
    if(arr[0]<arr[1]){
      min = arr[0];
			max=arr[1];
    }
    else{
      min=arr[1];
	  max=arr[0];
    }
    for(i = 2;i < number;i++){
      if(arr[i] < min){
        amount += min;        //arr < min
        min = arr[i];
      }
      else{
        if(arr[i] > max){
          amount += max;    //arr > max
          max = arr[i];
        }
        else{
          amount += arr[i]; // min <= arr <= max
        }
      }//if
    }//for
    avg = (double)amount/(number-2);
  }//if
  return avg;
}
