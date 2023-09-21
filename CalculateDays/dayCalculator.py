def get_days(date1, date2):
    fee_rate = 5 

    # splitting day1 into 3 variables: '2024-01-02' to '2024', '01', '02'
    year1, month1, day1 = date1.split("-")[0], date1.split("-")[1], date1.split("-")[2]

    # splitting day2 into 3 variables: '2023-06-02' to '2023', '06', '02'
    year2, month2, day2 = date2.split("-")[0], date2.split("-")[1], date2.split("-")[2]
    
    # get total days in date1
    # days in years1
    total_days_date1 = get_year_days(year1)

    # days in month1
    total_days_date1 += get_month_days(month1, year1)

    # total_days added to day1
    total_days_date1 += day1

    #get total days in date2
    # days in years2
    total_days_date2 = get_year_days(year2)

    # days in month2
    total_days_date2 += get_month_days(month2, year2)

    # total_days added to day2
    total_days_date2 += day2

    # get difference in days
    no_of_days = total_days_date1 - total_days_date2
    return no_of_days, (no_of_days * fee_rate)

# method used to get days from years
def get_year_days(year):
    passed_years = year - 1
    leap_years = passed_years - (passed_years%4)
    days_in_leap_years = leap_years * 365.25
    days_in_normal_years = (passed_years%4) * 365
    total_days_date1 = days_in_leap_years + days_in_normal_years
    return total_days_date1

# method used to get days from months
def get_month_days(month, year):
    months = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    total_days = 0
    for i in range(months[month]+1):
        total_days += days[i]
    if(year%4 == 0 and month >= 2):
        total_days += 1
    return total_days