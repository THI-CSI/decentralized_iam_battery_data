#include "common_utils.h"
#include "rtc_init.h"

static rtc_time_t g_set_time =  {
    .tm_hour    =  RESET_VALUE,
    .tm_isdst   =  RESET_VALUE,
    .tm_mday    =  RESET_VALUE,
    .tm_min     =  RESET_VALUE,
    .tm_mon     =  RESET_VALUE,
    .tm_sec     =  RESET_VALUE,
    .tm_wday    =  RESET_VALUE,
    .tm_yday    =  RESET_VALUE,
    .tm_year    =  RESET_VALUE,
};

static void rtc_date_time_conversion(rtc_time_t * time, unsigned char read_buffer[]);

fsp_err_t rtc_init(void)
{
    fsp_err_t err = FSP_SUCCESS;
    err = R_RTC_Open(&g_rtc0_ctrl, &g_rtc0_cfg);
    if (FSP_SUCCESS != err)
    {
        APP_ERR_PRINT ("\r\nRTC module open failed.\r\nRestart the Application\r\n");
    }
    return err;
}

fsp_err_t set_rtc_calendar_time(void)
{
    fsp_err_t err = FSP_SUCCESS;
    unsigned char read_time[25] = "23:05:2025 17:00:00";
    rtc_date_time_conversion(&g_set_time, &read_time[0]);

    // Set the time
    err = R_RTC_CalendarTimeSet(&g_rtc0_ctrl, &g_set_time);
    if (FSP_SUCCESS != err)
    {
        APP_ERR_PRINT("\r\nCalendarTime Set failed.\r\n");
        return err;
    }
    return err;
}

static void rtc_date_time_conversion(rtc_time_t * time, unsigned char read_buffer[])
{
    time->tm_mday = (((read_buffer[0] - ASCII_ZERO) * PLACE_VALUE_TEN) + (read_buffer[1] - ASCII_ZERO));
    time->tm_mon = ((((read_buffer[3] - ASCII_ZERO) * PLACE_VALUE_TEN) + (read_buffer[4] - ASCII_ZERO))) - MON_ADJUST_VALUE;
    time->tm_year = (((read_buffer[6] - ASCII_ZERO) * PLACE_VALUE_THOUSAND) +
            ((read_buffer[7] - ASCII_ZERO )* PLACE_VALUE_HUNDRED) +
            ((read_buffer[8] - ASCII_ZERO) * PLACE_VALUE_TEN) + (read_buffer[9] - ASCII_ZERO)) - YEAR_ADJUST_VALUE;
    time->tm_hour = (((read_buffer[11] - ASCII_ZERO) * PLACE_VALUE_TEN) + (read_buffer[12] - ASCII_ZERO));
    time->tm_min = (((read_buffer[14] - ASCII_ZERO) * PLACE_VALUE_TEN) + (read_buffer[15] - ASCII_ZERO));
    time->tm_sec = (((read_buffer[17] - ASCII_ZERO) * PLACE_VALUE_TEN )+ (read_buffer[18] - ASCII_ZERO));
}

fsp_err_t set_rtc_calendar_alarm(void)
{
    fsp_err_t err = FSP_SUCCESS;
    rtc_alarm_time_t alarm_time_set =
    {
         .sec_match        =  RESET_VALUE,
         .min_match        =  RESET_VALUE,
         .hour_match       =  RESET_VALUE,
         .mday_match       =  RESET_VALUE,
         .mon_match        =  RESET_VALUE,
         .year_match       =  RESET_VALUE,
         .dayofweek_match  =  RESET_VALUE,
    };
    unsigned char read_alarm[BUFFER_SIZE_DOWN] = "35";
    alarm_time_set.hour_match  = false;
    alarm_time_set.min_match   = false;
    alarm_time_set.sec_match   = true;
    alarm_time_set.mday_match  = false;
    alarm_time_set.mon_match   = false;
    alarm_time_set.year_match  = false;
    alarm_time_set.time.tm_sec = (((read_alarm[0] - ASCII_ZERO) * PLACE_VALUE_TEN )+ (read_alarm[1] - ASCII_ZERO));

    // Set the alarm time
    err = R_RTC_CalendarAlarmSet(&g_rtc0_ctrl, &alarm_time_set);
    if (FSP_SUCCESS != err)
    {
        APP_ERR_PRINT("\r\nCalendar alarm Set failed.\r\n");
        return err;
    }
    return err;
}

rtc_time_t get_rtc_calendar_time(void)
{
    rtc_time_t g_present_time =  {
     .tm_hour    =  RESET_VALUE,
     .tm_isdst   =  RESET_VALUE,
     .tm_mday    =  RESET_VALUE,
     .tm_min     =  RESET_VALUE,
     .tm_mon     =  RESET_VALUE,
     .tm_sec     =  RESET_VALUE,
     .tm_wday    =  RESET_VALUE,
     .tm_yday    =  RESET_VALUE,
     .tm_year    =  RESET_VALUE,
    };
    if (FSP_SUCCESS != R_RTC_CalendarTimeGet(&g_rtc0_ctrl, &g_present_time))
    {
        APP_ERR_PRINT("\r\nGetting RTC Calendar time failed.\r\n");
    }

    return g_present_time;
}

void rtc_deinit(void)
{
    fsp_err_t err = FSP_SUCCESS;
    err = R_RTC_Close(&g_rtc0_ctrl);
    if (FSP_SUCCESS != err)
    {
        APP_ERR_PRINT("** RTC module Close failed **  \r\n");
    }
}
