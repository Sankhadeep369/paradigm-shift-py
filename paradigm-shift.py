def battery_is_ok(temperature, soc, charge_rate, reporter=print, warnings_enabled=None):
    if warnings_enabled is None:
        warnings_enabled = {'temperature': True, 'soc': True, 'charge_rate': True}
    
    limits = [
        (temperature < 0, 'Temperature is too low!'),
        (temperature > 45, 'Temperature is too high!'),
        (soc < 20, 'State of Charge is too low!'),
        (soc > 80, 'State of Charge is too high!'),
        (charge_rate > 0.8, 'Charge rate is too high!')
    ]
    
    warnings = [
        (20 <= soc < 20 + 4, 'Warning: Approaching discharge', 'soc'),
        (80 - 4 <= soc <= 80, 'Warning: Approaching charge-peak', 'soc'),
        (0 <= temperature < 0 + 2.25, 'Warning: Approaching low temperature', 'temperature'),
        (45 - 2.25 <= temperature <= 45, 'Warning: Approaching high temperature', 'temperature'),
        (charge_rate > 0.76, 'Warning: Approaching charge-rate limit', 'charge_rate')
    ]

    # Check limits for alarms
    for condition, message in limits:
        if condition:
            reporter(message)
            return False

    # Check for warnings if enabled
    for condition, message, param in warnings:
        if condition and warnings_enabled.get(param, False):
            reporter(message)

    return True

def custom_reporter(message):
    print(f'[ALERT] {message}')

if __name__ == '__main__':
    assert(battery_is_ok(25, 70, 0.7) is True)
    assert(battery_is_ok(50, 85, 0) is False)
    assert(battery_is_ok(-5, 70, 0.7) is False)
    assert(battery_is_ok(25, 15, 0.7) is False)
    assert(battery_is_ok(25, 70, 0.9) is False) 
    assert(battery_is_ok(50, 70, 0.7, custom_reporter) is False)

    # Custom test with warnings disabled for temperature
    warnings_config = {'temperature': False, 'soc': True, 'charge_rate': True}
    battery_is_ok(44, 78, 0.78, reporter=custom_reporter, warnings_enabled=warnings_config)
