"""
convert from a gregorian date to a jewish date
and vice versa

Jewish calendar is a lunisolar calendar that periodically incorporates leap months
in addition to conditionally extending certain months in order to prevent certain holidays
from ocurring on (or too near) Saturday

"""


start_jdate = {7, 1, 5513}
j_year_start_month = 7
molad_start = 2 + 16/24 + 595/(24 *1080)#2d 16h 595p Molad tishrei for year 0, occurs every 19 yrs in cycle

start_gdate = {9, 7, 1752}
g_year_start_month = 1

julian_day_offset = 32045

julian_date_of_hg_epocstart = 2361215 #julian day number of the jewish start date and gregorian start date

long_kislev = 30
long_heshvan = 30

#mean lunation time is 29d 12h 793hq  nb - 24h/dy, 1080hq/h
mean_lunation_time = 29.5 + 793/(24*1080)

#19 year cycle length
nineteen_years = 235 * mean_lunation_time

#19 year leap month cycle
leap_years_cycle = {0, 3, 6, 8, 11, 14, 17}

#normal year
jewish_months ={('Nisan', 30), ('Iyar', 29), ('Sivan', 30), ('Tammuz',29),
                ('Av',30), ('Elul', 29), ('Tishrei', 30), ('Heshvan', 29),
                ('Kislev',29), ('Tevet', 29),('Shevat', 30), ('Adar', 29)}

jewish_leap_months ={('Nisan', 30),('Iyar', 29), ('Sivan', 30), ('Tammuz', 29),
                     ('Av', 30), ('Elul', 29),('Tishrei', 30), ('Heshvan', 29),
                     ('Kislev', 29), ('Tevet', 29),('Shevat', 30), ('Adar I', 30), ('Adar II', 29)}

gregorian_months ={('January', 31), ('February', 28), ('March', 31), ('April',30),
                ('May',31), ('June', 30), ('July', 31), ('August', 31),
                ('September',30), ('October', 31),('November', 30), ('December', 31)}

gregorian_leap_months ={('January', 31), ('February', 29), ('March', 31), ('April',30),
                ('May',31), ('June', 30), ('July', 31), ('August', 31),
                ('September',30), ('October', 31),('November', 30), ('December', 31)}

#determine if current year is a leap year
def is_jleap_year(yearNumber):
    if (yearNumber % 19 in leap_years_cycle):
        return True
    else:
        return False



def is_year_following_leap(year):
    return isJLeapYear(year-1)



def is_gleap_year(yearNumber):
    if (yearNumber % 4 == 0):
        if (yearNumber % 100 == 0):
                if (yearNumber % 400 == 0):
                    return True
                else:
                    return False
        else:
            return True
    else:
        return False


    
def gdate_to_absdate(month, day, year): 
    #conversion formula adapted from Fliegel and Van Flandern
    julian_day_number = math.floor(( 1461 * (year + 4800 + (month - 14)/ 12 ))/ 4 +( 367 * ( month - 2 - 12 * ( ( month - 14 ) / 12 ) ) ) / 12 -( 3 * ( ( year + 4900 + ( month - 14 ) / 12 ) / 100 ) ) / 4 + day - 32075) -1
         
    return julian_day_number - julian_date_of_hg_epocstart


def absdate_to_gdate(absdate):
    #conversion formula adapted from Fliegel and Van Flandern
    julian_day_number = absdate + julian_date_of_hg_epocstart

    l = julian_day_number + 68569
    n = ( 4 * l ) / 146097
    l = l - ( 146097 * n + 3 ) / 4
    i = ( 4000 * ( l + 1 ) ) / 1461001 
    l = l - ( 1461 * i ) / 4 + 31
    j = ( 80 * l ) / 2447
    day = math.floor(l - ( 2447 * j ) / 80)
    l = j / 11
    month = math.floor(j + 2 - ( 12 * l ))
    year = math.floor(100 * ( n - 49 ) + i + l)   

    return month, day, year



def decimal_days_to_dhp(day_count):
    weeks = math.floor(day_count/7)
    days = math.floor((day_count%7) * 7)
    hours = (day_count%7) * 24
    


#molad is the "birth" of the new moon
# hq = 1/1080 of an hour   ~3.33 seconds
def molad_tishri(year):    
    #return day of week and hq time of molad

    #divide year number by 19 - mod will tell us where we are in the cycle
    num_cycle = year / 19
    index_in_cycle = year % 19

    months_since_1h = 13 * (year - 1) - ((12 * year + 5) / 19)
    molad_hq = months_since_1h * mean_lunation_time + molad_start
    
    return ((day % 7), molad_hq)




#adjustments are made to the current year calendar
#if it will cause RH of the following year to land at the
#wrong time or if the length of the year is not in an acceptable range
def get_rh_delay_rule(year):
    year += 1
    #0 = no delay, 1= long kislev, 2= long kislev and heshvan
    day, hq = molad_tishri(year)
    shift = 0
    
    if hour > 18:   #shift if molad is after noon (18 hrs since we start at 6pm)
        shift = 1
        if day == 7:
            day = 0
        else:
            day +=1

    if day in (1,3,5):  #RH cannot be sunday, wed or friday
        shift +=1
        if day == 7:
            day = 0
        else:
            day +=1

    if is_year_following_leap(year): #adjustments to account for year lengths being off
        
        if day == 2 and hq > 9924:  #tuesday adjustment rule  9 hrs, 204hq
            shift +=2
            day +=2

        if day == 1 and hq > 16789: #monday adjustment rule 15 hrs, 589hq
            shift += 1
            day +=1

    return shift






year = 5755
        
if (is_jleap_year(year)):
    num_months = len (jewish_leap_months)
    num_days = sum (month[1] for month in jewish_leap_months)
else:
    num_months = len (jewish_months)
    num_days = sum (month[1] for month in jewish_months)
    
    




    

