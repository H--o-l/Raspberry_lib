/* 
 *
 *  Filename : nRF24.c
 *
 */
#define nRF24_C

/*============================ Include ============================*/

#include "RF24.h"
#include <math.h>
#include "nRF24.h"
#include <unistd.h>

/*============================ Macro ============================*/

#define MonitoringFrequency 100 /* ms => 0.8% CPU */
#define msleep(X)           usleep(X*1000)

/*============================ Global variable ============================*/

// CE and CSN pins On header using GPIO numbering (not pin numbers)
RF24 radio(25,0);  // Setup for GPIO 25 CSN

/*============================ Local Function interface ============================*/

static long millis_justForMe();

/*============================ Function implementation ============================*/

/*------------------------------- nRF24 -------------------------------*/
void nRF24_setup(void){

  memset(nRF24_gaError, 0, sizeof(nRF24_gaError));

  radio.begin();
  radio.enableDynamicPayloads();
  radio.setAutoAck(1);
  radio.setRetries(20,10); /* 4 try each 20ms */

  radio.openWritingPipe(0x7365727632LL); // pipe 0
  radio.openReadingPipe(1,0xF0F0F0F0E2LL); // pipe 1

  printf("From nRF24.c : \n");
  radio.printDetails();

  radio.startListening();
  // radio.printDetails();

  msleep(200);
}

int nRF24_send(char* iData){

  if(strlen(iData) <= 32){
    radio.stopListening();
    radio.write(iData, strlen(iData));
    radio.startListening();
    return 1;
  }else{
    printf("bouh\n");
    sprintf(nRF24_gaError,"Data to long '%s'\n", iData);
    return 0;
  }
}

int nRF24_received(char* oData, long const iMsTimeOut){
  long lTimeReference = 0;
  long lTime = 0;

  if(iMsTimeOut != -1){
    lTimeReference = millis_justForMe();
    lTime = lTimeReference;
  }

  //msleep(iMsTimeOut); /* TODO */
  while(  (iMsTimeOut == -1)
        ||((lTime - lTimeReference) <= iMsTimeOut)){
    if(radio.available()){
      uint8_t len = radio.getDynamicPayloadSize();
      if(len <= 32){
        radio.read(oData, len);
        oData[len] = 0;
        return 1;
      }else{
        sprintf(nRF24_gaError,"Error in received function\n");
        oData[0] = 0;
        return 0;
      }
    }
    if(iMsTimeOut != -1){
      lTime = millis_justForMe(); 
    }
    msleep(MonitoringFrequency);
  }
  //sprintf(nRF24_gaError, "Received time out %10ld %10ld %10ld\n", lTimeReference, lTime, lTime - lTimeReference);
  oData[0] = 0;
  return 1; /* time out is not an error */
}

static long millis_justForMe(){
  struct timespec spec;
  clock_gettime(CLOCK_MONOTONIC, &spec);
  return round((spec.tv_sec*1000) + (spec.tv_nsec / 1.0e6));
}