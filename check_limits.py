def check_threshold(value, lower_limit, upper_limit, parameter_name, reporter):
    if value < lower_limit:
        reporter(f'{parameter_name} is too low!')
        return False
    elif value > upper_limit:
        reporter(f'{parameter_name} is too high!')
        return False
    return True

def battery_is_ok(temperature, soc, charge_rate, reporter=print):
    checks = [
        (temperature, 0, 45, 'Temperature'),
        (soc, 20, 80, 'State of Charge'),
        (charge_rate, 0, 0.8, 'Charge rate')
    ]
    
    return all(check_threshold(value, lower, upper, name, reporter) for value, lower, upper, name in checks)

# Example of a custom reporter
def custom_reporter(message):
    print(f'[ALERT] {message}')

if __name__ == '__main__':
    # Complete the tests to cover all conditions
    assert(battery_is_ok(25, 70, 0.7) is True)
    assert(battery_is_ok(50, 85, 0) is False)  # High temperature, high soc, low charge rate
    assert(battery_is_ok(-5, 70, 0.7) is False)  # Low temperature
    assert(battery_is_ok(25, 15, 0.7) is False)  # Low State of Charge
    assert(battery_is_ok(25, 70, 0.9) is False)  # High charge rate
    assert(battery_is_ok(50, 70, 0.7, custom_reporter) is False)  # Using a custom reporter
