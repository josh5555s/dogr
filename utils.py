def makeAgeInt(value):
    yearIndex = value.find('year')
    if (yearIndex == -1):
        years = 0
    else:
        years = value[:yearIndex]
    return int(years)

def makeWeightFloat(value):
    lbsIndex = value.find('lbs')
    if (lbsIndex == -1):
        pass
    else:
        lbs = float(value[:lbsIndex].strip())
    return lbs