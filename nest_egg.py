import sys

RETIREMENT_AGE = 65
DEATH_AGE = 95
MY_AGE = 27
YEARS_IN_RETIREMENT = DEATH_AGE - RETIREMENT_AGE
MARKET_GROWTH = 1.07
INFLATION_RATE = 1.022

LOW_NEST_EGG = 100000


def calc_nest_egg(annual_withdrawal):
    """Use a binary search to find the needed nest_egg to retire at RETIREMENT_AGE, assuming you will live till DEATH_AGE

      High and Low are rough guesses to start the binary search. They are calculated as:
        - beginning low estimate: $100,000
        - beginning high estimate: The annual withdrawal amount multiplied by the number of years in retirement.
            With the assumption that the market will grow every year by MARKET_GROWTH, this estimate is safely a high estimate
    """
    high_nest_egg = annual_withdrawal * YEARS_IN_RETIREMENT

    def get_remainder_from_guess(nest_egg_guess):
        return get_remainder_after_death(nest_egg_guess, annual_withdrawal)

    return binary_search(LOW_NEST_EGG, high_nest_egg, get_remainder_from_guess)


def binary_search(low, high, get_remainder):
    """This is a unique binary search that tries to find a number that falls within the range 0 and 1.
    """
    mid = (high + low) / 2
    remainder = get_remainder(mid)

    if remainder >= 0 and remainder < 1:
        return mid
    elif remainder < 0:
        return binary_search(mid, high, get_remainder)
    else:
        return binary_search(low, mid, get_remainder)
    

def get_remainder_after_death(nest_egg, annual_withdrawal):
    for _ in range(YEARS_IN_RETIREMENT):
        annual_withdrawal = get_inflation_adjustment(annual_withdrawal, 1)
        nest_egg = nest_egg - annual_withdrawal
        if (nest_egg > 0):
            nest_egg = get_market_growth(nest_egg)

    return nest_egg


def get_inflation_adjustment(num, years):
    # 2.2% inflation rate is the median of the monthly inflation rates from 2000 - 2019
    # based on this data set: https://www.usinflationcalculator.com/inflation/historical-inflation-rates/
    for _ in range(years):
        num = num * INFLATION_RATE

    return num

def get_market_growth(amount):
    return amount * MARKET_GROWTH


def format_currency(num):
    return "${:,}".format(round(num, 2))


annual_withdrawal_num = float(sys.argv[1])
years_to_retirement = RETIREMENT_AGE - MY_AGE
inflation_adjusted_annual_withdrawal = get_inflation_adjustment(
    annual_withdrawal_num, years_to_retirement)

estimated_nest_egg = calc_nest_egg(inflation_adjusted_annual_withdrawal)
print(format_currency(estimated_nest_egg))
