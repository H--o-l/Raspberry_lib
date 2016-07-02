/* 
 *
 *  Filename : nRF24.h
 *
 */

#ifndef nRF24_H
#define nRF24_H

/*============================ Include ============================*/

/*============================ Macro ============================*/

/*============================ Extern variable ============================*/
#ifdef nRF24_C
#define _extern 
#else
#define _extern extern
#endif

_extern char nRF24_gaError[250];

/*============================ Function interface ============================*/

void nRF24_setup(void);
int  nRF24_send(char* iData);
int  nRF24_received(char* oData, long const iMsTimeOut);

#endif