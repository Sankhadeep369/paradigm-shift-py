def battery_is_ok(temperature, soc, charge_rate, reporter=print):
    limits = [
        (temperature < 0, 'Temperature is too low!'),
        (temperature > 45, 'Temperature is too high!'),
        (soc < 20, 'State of Charge is too low!'),
        (soc > 80, 'State of Charge is too high!'),
        (charge_rate > 0.8, 'Charge rate is too high!')
    ]

    for condition, message in limits:
        if condition:
            reporter(message)
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
