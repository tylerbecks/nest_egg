import sys

RETIREMENT_AGE = 65
DEATH_AGE = 95
MY_AGE = 27
YEARS_IN_RETIREMENT = DEATH_AGE - RETIREMENT_AGE
MARKET_GROWTH = 1.07
INFLATION_RATE = 1.022

LOW_NEST_EGG = 100000


def get_inflation_adjustment(num):
    # 2.2% inflation rate is the median of the monthly inflation rates from 2000 - 2019
    # based on this data set: https://www.usinflationcalculator.com/inflation/historical-inflation-rates/
    years_to_retirement = RETIREMENT_AGE - MY_AGE
    for _ in range(years_to_retirement):
        num = num * INFLATION_RATE

    return num


def calc_nest_egg(annual_withdrawal, low_nest_egg=LOW_NEST_EGG, high_nest_egg=None):
    """Use a binary search to find the needed nest_egg to retire at RETIREMENT_AGE, assuming you will live till DEATH_AGE
      High and Low are roughly measured by:
        - beginning low estimate: $100,000
        - beginning high estimate: The annual withdrawal amount multiplied by the number of years in retirement.
            With the assumption that the market will grow every year by MARKET_GROWTH, this estimate is safely a high estimate
    """
    if high_nest_egg is None:
        high_nest_egg = annual_withdrawal * YEARS_IN_RETIREMENT

    mid_nest_egg = (high_nest_egg + low_nest_egg) / 2
    remainder = get_remainder_after_retirement(mid_nest_egg, annual_withdrawal)

    if remainder >= 0 and remainder < 1:
        return round(mid_nest_egg, 2)
    elif remainder < 0:
        return calc_nest_egg(annual_withdrawal, mid_nest_egg, high_nest_egg)
    else:
        return calc_nest_egg(annual_withdrawal, low_nest_egg, mid_nest_egg)


def get_remainder_after_retirement(nest_egg, annual_withdrawal):
    for _ in range(YEARS_IN_RETIREMENT):
        annual_withdrawal = annual_withdrawal * INFLATION_RATE
        nest_egg = nest_egg - annual_withdrawal
        if (nest_egg > 0):
            nest_egg = get_market_growth(nest_egg)

    return nest_egg


def get_market_growth(amount):
    return amount * MARKET_GROWTH

def format_currency(num):
    return "${:,}".format(num)


annual_withdrawal_num = float(sys.argv[1])
inflation_adjusted_annual_withdrawal = get_inflation_adjustment(
    annual_withdrawal_num)

estimated_nest_egg = calc_nest_egg(inflation_adjusted_annual_withdrawal)
print(format_currency(estimated_nest_egg))
