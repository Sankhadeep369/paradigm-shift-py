def battery_is_ok(temperature, soc, charge_rate, reporter=print):
    if temperature < 0:
        reporter('Temperature is too low!')
        return False
    if temperature > 45:
        reporter('Temperature is too high!')
        return False
    if soc < 20:
        reporter('State of Charge is too low!')
        return False
    if soc > 80:
        reporter('State of Charge is too high!')
        return False
    if charge_rate > 0.8:
        reporter('Charge rate is too high!')
        return False
    return True

# Example of a custom reporter
def custom_reporter(message):
    print(f'[ALERT] {message}')

if __name__ == '__main__':
    # Complete the tests to cover all conditions
    assert(battery_is_ok(25, 70, 0.7) is True)
    assert(battery_is_ok(50, 85, 0) is False)  # High temperature and SOC, low charge rate
    assert(battery_is_ok(-5, 70, 0.7) is False)  # Low temperature
    assert(battery_is_ok(25, 15, 0.7) is False)  # Low SOC
    assert(battery_is_ok(25, 70, 0.9) is False)  # High charge rate
    assert(battery_is_ok(50, 70, 0.7, custom_reporter) is False)  # Using a custom reporter
