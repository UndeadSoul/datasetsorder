substring_date="08/12/1982"

day=substring_date[:2]
month=substring_date[-5:-3:]
year=substring_date[:-6]

print(day+"-"+month+"-"+year)