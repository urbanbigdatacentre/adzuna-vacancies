############################# 
# Extraction code for hourly, daily, weekly, monthly and annual salaries from the Adzuna DESCRIPTION variable.
# It also identifies jobs that offer zero hour contracts (likely hourly wage jobs), jobs that offer "competitive salaries and "negotiable" salaries
############################# 



#Clean raw salary
#df['salary_raw_clean'] = df['salary_raw'].apply(lambda x: clean_description(x) if isinstance(x,str) else None)


'''
 Zero hour contract jobs
'''
zero_hours = r'(?i)(?:\b(?:zero|0)[\s-]hour|casual contract|piece work|hours not guaranteed|no hours guarantee|can\'t guarantee hours|no guarantee of hours)'


'''
Hourly wage regex code. 
Key idea is that the word "hour" must appear 4 words before or after salary digits.
'''
hourly_wage = r'''
(?i)                                                    # Case insensitive regex code
    £(                                              ### Start of CAPTURE GROUP 1 - designed to capture a single salary figure stated e.g. "£10" or "£10.50"
        [1-9]\d?                                        # Allow digit between 1 and 9, followed by an optional second digit
        (?:\.\d{2})?                                    # Optional trailing pence e.g.".00" 
     )                                              ### End of CAPTURE GROUP 1

    (?!,?\d)                                            # Negative lookahead - disregard Capture Group 1 if a digit follows or ",digit" follows e.g. "£100" or "£10,0"
    (?![kmb]\b)                                         # Negative lookahead - disregard Capture Group 1 if the letters "k", "m" or "b" follow e.g.  "£10k"      
    (?!\s?[mb]ill)                                      # Negative lookahead - disregard Capture Group 1 if "mill" or "bill" follow e.g. "£10 mil"   
    (?!\.\d\s?[mbk]\b)                                  # Negative lookahead - disregard Capture Group 1 if a bullet point, digit, optional space and either "m", "b" or "k" follow e.g. "£10.5k"
    (?!\.\d\s?[mb]ill)                                  # Negative lookahead - disregard Capture Group 1 if a bullet point, digit, optional space and either "mill" or "bill" follow e.g. "£10.5 mill"
    (?!(?:\s(?:[A-Za-z]+\s){1,2}|\s*[-/\\]\s*)£?(?:\d{1,2}[Kk]|\d{2},\d|\d{3})) # Negative lookahead - disregard Capture Group 1 if there is a salary range and the second part has a figure that has 3 digits, "k" notation or 2 digits a comma and a digit e.g. "10,0" (this implies 10,000)

    (?:                                             ### Start of optional salary range - e.g. "£10 to £11"
        (?:\s(?:[A-Za-z]+\s){1,2}|\s*[-/\\]\s*)         # Require a space, followed by 1 or 2 words (e..g "up to") OR allow a "-", "/", "\" between the salaries 
        £?([1-9]\d?                                     # Start of CAPTURE GROUP 2 - capture the "11" in cases like "£10 to £11"
        (?:\.\d{2})?)                                   # Optional trailing ".00" - End of CAPTURE GROUP 2 
    )?                                              ### End of optional salary range
    
    (?!,?\d)                                            # Negative lookahead - see previous
    (?![kmb]\b)                                         # Negative lookahead - see previous                                    
    (?!\s?[mb]ill)                                      # Negative lookahead - see previous
    (?!\.\d\s?[mbk]\b)                                  # Negative lookahead - see previous
    (?!\.\d\s?[mb]ill)                                  # Negative lookahead - see previous

    [\\/\s]?(?:p[./\\]?hr?\b|hr\b|(?:[a-z]+\s){0,4}hour[a-z]*) # Hour words after salary. The code allows for variants of "ph" (e.g. "p/h", "p.h"), "phr" or "hr" to identify hourly wages. It also accomodates words starting with "hour" appearing at least 4 words after the salary digits (so this would capture "per hour") or immediately after e.g. £10/hour.

|                                                       # Code after this OR operator is very close to mirroring the code before it. The only difference is that is searches for hour words appearing BEFORE salary.                                               

    (?:hour[a-z]*\s(?:[a-z]+\s){0,4})                   # Search words beginning with "hour" appearing up to 4 words before salary.

    £(                                              ### Start of CAPTURE GROUP 3 - designed to capture a single salary figure stated e.g. "£10" or "£10.50"
        [1-9]\d?                                        # Digit between 1 and 9, followed by an optional second digit
        (?:\.\d{2})?                                    # Optional trailing ".00" 
     )                                              ### End of CAPTURE GROUP 3

    (?!,?\d)                                            # Negative lookahead - disregard Capture Group 1 if a digit follows or ",digit" follows e.g. "£100" or "£10,0"
    (?![kmb]\b)                                         # Negative lookahead - disregard Capture Group 1 if the letters "k", "m" or "b" follow e.g.  "£10k"    
    (?!\s?[mb]ill)                                      # Negative lookahead - disregard Capture Group 1 if "mill" or "bill" follow e.g. "£10 mil"   
    (?!\.\d\s?[mbk]\b)                                  # Negative lookahead - disregard Capture Group 1 if a bullet point, digit, optional space and either "m", "b" or "k" follow e.g. "£10.5k"
    (?!\.\d\s?[mb]ill)                                  # Negative lookahead - disregard Capture Group 1 if a bullet point, digit, optional space and either "mill" or "bill" follow e.g. "£10.5 mill"

    (?:                                             ### Start of optional salary range - e.g. "£10 to £11"
        (?:\s(?:[A-Za-z]+\s){1,2}|\s*[-/\\]\s*)         # Require a space, followed by 1 or 2 words (e..g "up to") OR allow a "-", "/", "\" between the salaries 
        £?([1-9]\d?                                     # Start of CAPTURE GROUP 4 - capture the "11" in "£10 to £11"
        (?:\.\d{2})?)                                   # End of CAPTURE GROUP 4 - optional trailing ".00"
    )?                                              ### End of optional salary range

    (?!,?\d)                                            # Negative lookahead - see previous
    (?![kmb]\b)                                         # Negative lookahead - see previous 
    (?!\s?[mb]ill)                                      # Negative lookahead - see previous  
    (?!\.\d\s?[mbk]\b)                                  # Negative lookahead - see previous  
    (?!\.\d\s?[mb]ill)                                  # Negative lookahead - see previous
'''




'''
National Living Wage and minimum wage regex code
'''
nat_liv_wage = r'(?i)(national\sliving\swage)'
min_wage = r'(?i)(minimum\swage)'





'''
Daily wage regex code
'''
daily_wage = r'''
(?i)
    £(                                               ### Start of CAPTURE GROUP 1
        (?:[1-9]\d{2}|[5-9]\d)                          # Require a 3 digit wage ("e.g. £500") or a 2 digit wage higher than £50.
        (?:\.[0-9]{2})?                                 # Optional trailing .00
     )                                               ### End of CAPTURE GROUP 1
    
    (?!,?\d)                                            # Negative lookahead - disregard Capture Group 1 if a digit follows or ",digit" follows e.g. "£100" or "£10,0"
    (?![kmb]\b)                                         # Negative lookahead - disregard Capture Group 1 if the letters "k", "m" or "b" follow e.g.  "£10k"    
    (?!\s?[mb]ill)                                      # Negative lookahead - disregard Capture Group 1 if "mill" or "bill" follow e.g. "£10 mil"   
    (?!\.\d\s?[mbk]\b)                                  # Negative lookahead - disregard Capture Group 1 if a bullet point, digit, optional space and either "m", "b" or "k" follow e.g. "£10.5k"
    (?!\.\d\s?[mb]ill)                                  # Negative lookahead - disregard Capture Group 1 if a bullet point, digit, optional space and either "mill" or "bill" follow e.g. "£10.5 mill"                                                                                    
                                                     
    (?:                                              ### Start of optional salary range - e.g. "£80 to £110"
        (?:\s(?:[A-Za-z]+\s){1,2}|\s*[-/\\]\s*)         # Require a space, followed by 1 or 2 words (e..g "up to") OR allow a "-", "/", "\" between the salaries 
        £?([1-9][0-9]{1,2}                              # Start of CAPTURE GROUP 2
        (?:\.[0-9]{2})?)                                # End of CAPTURE GROUP 2 - optional trailing ".00"
    )?                                               ### End of optional salary range - e.g. "£80 to £110"


    [\\/\s]?(?:p[./\\]?da?y?\b|(?:[a-z]+\s){0,4}(?:day\b|daily\b|night|shift\b)) # Day related words appearing 0 to 4 words after the salary   

|                                                       # Code after this OR operator is very close to mirroring the code before it. The only difference is that is searches for day words appearing BEFORE salary.                                               

    (?:\bday|\bdaily\b|\bnight|\bshift\b)\s(?:[a-z]+\s){0,4} # Daily words before salary -

    £(                                               ### Start of CAPTURE GROUP 3
        (?:[1-9]\d{2}|[5-9]\d)                          # Require a 3 digit wage ("e.g. £500") or a 2 digit wage higher than £50.
        (?:\.[0-9]{2})?                                 # Optional trailing .00
     )                                               ### End of CAPTURE GROUP 3

    (?!,?\d)                                            # Negative lookahead - see previous
    (?![kmb]\b)                                         # Negative lookahead - see previous    
    (?!\s?[mb]ill)                                      # Negative lookahead - see previous
    (?!\.\d\s?[mbk]\b)                                  # Negative lookahead - see previous
    (?!\.\d\s?[mb]ill)                                  # Negative lookahead - see previous          

    (?:                                              ### Start of optional salary range - e.g. "£80 to £110"
        (?:\s(?:[A-Za-z]+\s){1,2}|\s*[-/\\]\s*)         # Require a space, followed by 1 or 2 words (e..g "up to") OR allow a "-", "/", "\" between the salaries 
        £?([1-9][0-9]{1,2}                              # Start of CAPTURE GROUP 4
        (?:\.[0-9]{2})?)                                # End of CAPTURE GROUP 4 - optional trailing ".00"
     )?                                              ### End of optional salary range - e.g. "£80 to £110"
''' 



'''
Weekly wage
''' 
weekly_wage = r'''
(?i)
    £(                                              ### Start of Capture Group 1
        (?:[1-3],?\d{3}|[1-9]\d{2})                    # Look for a salary that is 3 digits or 4 digits that is under £1300. 
        (?:\.[0-9]{2})?                                # Optional trailing ".00"
     )                                              ### End of Capture Group 1

    (?!,?\d)                                           # Negative lookahead - disregard Capture Group 1 if a digit follows or ",digit" follows e.g. "£100" or "£10,0"
    (?![mb]\b)                                         # Negative lookahead - disregard Capture Group 1 if the letters "k", "m" or "b" follow e.g.  "£10k"    
    (?!\s?[mb]ill)                                     # Negative lookahead - disregard Capture Group 1 if "mill" or "bill" follow e.g. "£10 mil"   
    (?!\.\d\s?[mb]\b)                                  # Negative lookahead - disregard Capture Group 1 if a bullet point, digit, optional space and either "m", "b" or "k" follow e.g. "£10.5k"
    (?!\.\d\s?[mb]ill)                                 # Negative lookahead - disregard Capture Group 1 if a bullet point, digit, optional space and either "mill" or "bill" follow e.g. "£10.5 mill"

    (?:                                             ### Start of optional salary range - e.g. "£500 to £1000"
        (?:\s(?:[A-Za-z]+\s){1,2}|\s*[-/\\]\s*)        # Require a space, followed by 1 or 2 words (e..g "up to") OR allow a "-", "/", "\" between the salaries 
        £?((?:[1-3],?\d{3}|[1-9]\d{2})                 # Start of CAPTURE GROUP 2
        (?:\.[0-9]{2})?)                               # End of CAPTURE GROUP 2  - optional trailing ".00"
    )?                                              ### End of optional salary range - e.g. "£500 to £1000"

    [\\/\s]?(?:p[./\\]?w\b|(?:[a-z]+\s){0,4}(?:\bweek\b|\bworkweek\b)) # Week words after salary - Require a word beginning with "week" or "workweek" to appear up to 4 words after the salary  

|

    (?:\bweek[a-z]*|\bworkweek\b)\s(?:[a-z]+\s){0,4}   # Week words before salary 

     £(                                                ### Start of CAPTURE GROUP 3
        (?:[1-3],?\d{3}|[1-9]\d{2})                      # Look for a salary that is 3 digits or 4 digits that is under £1300.
        (?:\.[0-9]{2})?                                  # Optional trailing ".00"
     )                                                 ### End of CAPTURE GROUP 3

    (?!,?\d)                                            # Negative lookahead - see previous
    (?![mb]\b)                                          # Negative lookahead - see previous    
    (?!\s?[mb]ill)                                      # Negative lookahead - see previous
    (?!\.\d\s?[mb]\b)                                   # Negative lookahead - see previous
    (?!\.\d\s?[mb]ill)                                  # Negative lookahead - see previous 

    (?:                                               ### Start of optional salary range - e.g. "£500 to £1000"
        (?:\s(?:[A-Za-z]+\s){1,2}|\s*[-/\\]\s*)         # Require a space, followed by 1 or 2 words (e..g "up to") OR allow a "-", "/", "\" between the salaries 
        £?((?:[1-3],?\d{3}|[1-9]\d{2})                  # Start of Capture Group 4
        (?:\.[0-9]{2})?)                                # End of Capture Group 4  - optional trailing ".00" 
    )?                                                ### End of optional salary range

'''

################# Extreme monthly salaries (these are salaries that are <£1000 or >£9999). This is old and I dont use it.
monthly_wage_extreme_values = r'''
(?:salary(?:\s?[:-\=]\s?|\s[a-z]+\s))                                   # Require "salary" followed by either one of "-", "=", ":" or 1 or 2 random words.
£[1-9](?:(?:\d,?\d{3}|\d{2})                                            # Require extreme salary values like £10,000 or £100
(?:\.\d\d)?                                                             # Optional .00
(?:(?:\s*[-/\\]?\s*|\s[a-z]+\s)£?[1-9](?:\d,?\d{3}|\d{3}|\d{2}))?        # \d,?\d{3} and \d{2} are same as previous. But \d{3} is allowed so i captures cases like £900-£1000
(?:\.\d\d)?                                                             # Optional .00
|
(?:\d(?:\.\d{1,2})?k\b)                                                 # Look for monthly wages in "k" e.g. £10k or £10.5k  
(?:(?:\s*[-/\\]?\s*|\s[a-z]+\s)£?[1-9](?:\d(?:\.\d{1,2})?k\b))?          # Allow a salary range (in digits)
)
(?=\s\w*\s?(?:month|(?:four|4)[-\s]week))                               # Require a month word immediately after the salary or one word after.
'''


###################### Monthly - normal values. This is old and I dont use it.
monthly_wage_normal_values = r'''
    (£[1-9](?:,?[0-9]{3}                                                # 1) Month words after salary - Require "£" sign followed by digit between 1 and 9, followed by 3 digits
    (?:\.\d\d)?                                                         # 1) Month words after salary - Optional trailing .00
    (?:(?:\s*[-/\\]?\s*|\s[a-z]+\s)£?[1-9],?[0-9]{3,4})?                 # 1) Month words after salary - Salary range code. Allow " - ", " / ", or " \ " with optional spaces OR " word ", followed by a salary. Allow second half of salary range to have an additional digit e.g. £10,000
    (?:\.\d\d)?                                                         # 1) Month words after salary - Optional trailing .00
    |   
    (?:k\b|\.\d{1,2}k\b)                                                # 1) Month words after salary - "k" notation for salary. Allow £1k or £1.25k
    (?:(?:\s*[-/\\]?\s*|\s[a-z]+\s)£?[1-9](?:\d?k\b|\d?\.\d{1,2}k\b))?)  # 1) Month words after salary - Salary range code. Allow " - ", " / ", or " \ " with optional spaces OR " word ", followed by a salary in "k" notation. Allow second half of salary range to have an additional digit e.g. £10k
    (?:\s?[a-z]+\s){0,4}\s?(?:month|(?:four|4)[-\s]week)                # 1) Month words after salary - Require month words to appear up to 4 words after the salary
|
    (?:\bmonth[a-z]*|(?:four|4)[-\s]week[a-z]*)\s(?:[a-z]+\s){0,4}      # 2) Month words before salary -
    £[1-9](?:,?[0-9]{3}                                                 # 2) Month words before salary -
    (?:\.\d\d)?                                                         # 2) Month words before salary -    
    (?:(?:\s*[-/\\]?\s*|\s[a-z]+\s)£?[1-9],?[0-9]{3,4})?                 # 2) Month words before salary -
    (?:\.\d\d)?                                                         # 2) Month words before salary - 
    |
    (?:k\b|\.\d{1,2}k\b)                                                # 2) Month words before salary -
    (?:(?:\s*[-/\\]\s*|\s[a-z]+\s)                                      # 2) Month words before salary -
    £?[1-9](?:\d?k\b|\d?\.\d{1,2}k\b))?))                               # 2) Month words before salary -
    '''                            







###################### Annual values - normal values. Doesn't require annual words.
annual_wage = r'''
(?i)                                                       # Case insensitive regex code.
    £(                                                   ### Start of CAPTURE GROUP 1 - single salary figure up to £199,000.
        (?:1\d\d|[1-9]\d),?\d{3}                           # Allow 6 digit salaries up to £200k, or 5 digit salary e.g. £50,000
        (?:\.\d\d)?                                        # Optional trailing ".00"
     )                                                   ### End of CAPTURE GROUP 1

    (?!,?\d)                                               # Negative lookahead - disregard Capture Group 1 if a digit follows or ",digit" follows e.g. "£100" or "£10,0"
    (?![mb]\b)                                             # Negative lookahead - disregard Capture Group 1 if the letters "k", "m" or "b" follow e.g.  "£10k"    
    (?!\s?[mb]ill)                                         # Negative lookahead - disregard Capture Group 1 if "mill" or "bill" follow e.g. "£10 mil"   
    (?!\.\d\s?[mb]\b)                                      # Negative lookahead - disregard Capture Group 1 if a bullet point, digit, optional space and either "m", "b" or "k" follow e.g. "£10.5k"
    (?!\.\d\s?[mb]ill)                                     # Negative lookahead - disregard Capture Group 1 if a bullet point, digit, optional space and either "mill" or "bill" follow e.g. "£10.5 mill"
    (?!(?:\s(?:[A-Za-z]+\s){1,2}|\s*[-/\\]\s*)£?(?:[2-9]\d\d|\d{1,3},?\d{3}),?\d{3})  # Negative lookahead, no abnormally large salaries stated in second part of salary range (rules out £10,000-£150,000)
 
    (?:                                                  ### Start of optional salary range - e.g. "£10,000 to £11,000"
        (?:\s(?:[A-Za-z]+\s){1,2}|\s*[-/\\]\s*)            # Require a space, followed by 1 or 2 words (e..g "up to") OR allow a "-", "/", "\" between the salaries 
        £?(                                                # Start of CAPTURE GROUP 2 - captures second part of salary range e.g. £11,000 in "£10,000 to £11,000"
            (?:1\d\d|[1-9]\d),?\d{3}                       # Allow 6 digit salaries up to £200k, or 5 digit salary e.g. £50,000 
            (?:\.\d\d)?                                    # Optional trailing ".00"
         )                                                 # End of CAPTURE GROUP 2 - optional trailing ".00"
    )?                                                  ### End of optional salary range - e.g. "£10,000 to £11,000"

    (?!,?\d)                                               # Negative lookahead - see previous
    (?![mb]\b)                                             # Negative lookahead - see previous    
    (?!\s?[mb]ill)                                         # Negative lookahead - see previous
    (?!\.\d\s?[mb]\b)                                      # Negative lookahead - see previous
    (?!\.\d\s?[mb]ill)                                     # Negative lookahead - see previous         

|
    
    £((?:1\d\d|[1-9]\d)                                    # Start of CAPTURE GROUP 3 - K notation for salary e.g £10k. Allow up to £200k
     (?:\.\d{1,2})?)k\b                                    # End of CAPTURE GROUP 3 - K notation for salary e.g £10k. Optional digit digt e.g £10.50k                                                   

    (?:                                                  ### Start of optional salary range for K notation
        (?:\s(?:[A-Za-z]+\s){1,2}|\s*[-/\\]\s*)            # Require a space, followed by 1 or 2 words (e.g "up to") OR allow a "-", "/", "\" between the salaries 
        £?(                                                # Start of CAPTURE GROUP 4  - second part of salary range
            (?:1\d\d|[1-9]\d)                              # Single salary figure in k notation e.g. "£10k" or "£100k"
            (?:\.\d{1,2})?)                                # Also one or two digits before "k" e.g. £10.2k or £10.52k
            k\b                                            # End of CAPTURE GROUP 4                                              
    )?                                                   ### End of optional salary range
                                       
|
    £(                                                   ### Start of CAPTURE GROUP 5 - designed to capture annual salaries where "k" is missing in k notation. e.g. £50-£55k or £50-55k. Will capture the "50".
        (?:1\d\d|[1-9]\d)                                  # Allow 3 digits or 2 digits
        (?:\.\d{1,2})?                                     # Optional digits e.g. £10.52k - end of CAPTURE GROUP 5 
        )                                                ### End of CAPTURE GROUP 5

    \s?-\s?                                                # Salary range

    £?((?:1\d\d|[1-9]\d)                                   # CAPTURE GROUP 6 - Missing "k" in k notation e.g. £50-£55k or £50-55k. Will capture "55". Will need to multiple by 1,000 
      (?:\.\d{1,2})?)                                      # Optional digits - end of CAPTURE GROUP 6
     k\b                                                   # Require "k", ".digitk" or ".digitdigitk"
|
    \bsalar[a-z]+\s(?:[a-z]+\s){1,2}?                      # Require a word starting with "salar", followed by 1 or 2 words:
    ((?:1\d\d|[1-9]\d)                                     # Capture Group 7 -  Note the missing "£" sign! - captures e.g. 50k-55k. This line captures the "50". Will need to multiple by 1,000. Must have "salar" two or one word before for robustness.
     (?:\.\d{1,2})?)                                       # Require "k", ".digitk" or ".digitdigitk"
     k\b

    (?:                                                  ### Start of optional salary range
        (?:\s(?:[A-Za-z]+\s){1}|\s*[-/\\]\s*)              # Allow only one word between salary figures here, or allow spaces, dashes, forward slashes
        ((?:1\d\d|[1-9]\d)                                 # Capture Group 8 -  Missing "£" sign - e.g. 50k-55k. Will capture second part of salary, i.e. the "55". Will need to multiple by 1,000. 
        (?:\.\d{1,2})?)                                    # Require "k", ".digitk" or ".digitdigitk"
        k\b
    )?                                                   ### End of optional salary range                           
'''




competitive_negotiable_salary = r'''
(?i)((?:competitive\ssalar[a-z]+|salar[a-z]+\s(?:[a-z]+\s){0,2}competitive)  # Require "competitive salary" or the word salary, one or two words, then competitive.
    |
(?:negoti[a-z]+\s(?:[a-z]+\s){0,2}salar[a-z]+|salar[a-z]+\s(?:[a-z]+\s){0,2}negoti[a-z]+)) # Require "salary negotiable or the word negotionable, one or two words, then salary.
'''        



#hourly_wage_pattern = re.compile(hourly_wage, re.VERBOSE)
#daily_wage_pattern = re.compile(daily_wage, re.VERBOSE)
#weekly_wage_pattern = re.compile(weekly_wage, re.VERBOSE)
#monthly_wage_normal_values_pattern = re.compile(monthly_wage_normal_values)
#monthly_wage_extreme_values_pattern = re.compile(monthly_wage_extreme_values)
#annual_wage_pattern = re.compile(annual_wage, re.VERBOSE)



# Make sure the regex code isnt case sensitive.
'''
pay_freq_tuples_re = [('vacancy_with_zero_hour_contracts', zero_hours),
                      ('vacancy_with_hourly_wage', hourly_wage), 
                      ('vacancy_with_daily_wage', daily_wage), 
                      ('vacancy_with_weekly_wage', weekly_wage),
                      ('vacancy_with_monthly_wage_normal_values', monthly_wage_normal_values),
                      ('vacancy_with_monthly_wage_extreme_values', monthly_wage_extreme_values),
                      ('vacancy_with_annual_wage', annual_wage)
                      ] 
'''




