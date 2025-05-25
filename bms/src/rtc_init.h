#ifndef RTC_EP_H_
#define RTC_EP_H_

/* MACRO for ASCII value of zero */
#define ASCII_ZERO       (48)
/* MACRO for null character */
#define NULL_CHAR   ('\0')

/*MACROs to adjust month and year values */
#define MON_ADJUST_VALUE      (1)
#define YEAR_ADJUST_VALUE     (1900)

/* MACROs for RTT input processing */
#define PLACE_VALUE_TEN           (10)
#define PLACE_VALUE_HUNDRED       (100)
#define PLACE_VALUE_THOUSAND      (1000)

fsp_err_t rtc_init(void);
fsp_err_t set_rtc_calendar_time(void);
fsp_err_t set_rtc_calendar_alarm(void);
rtc_time_t get_rtc_calendar_time(void);
void rtc_deinit(void);

#endif /* RTC_EP_H_ */
