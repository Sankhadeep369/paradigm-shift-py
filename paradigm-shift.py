MAJOR_TEMP_LIMITS = (0, 45)
SOC_LIMITS = (20, 80)
CHARGE_RATE_LIMIT = 0.8

def check_limits(value, low, high, low_message, high_message):
    """Helper function to check if a value is out of defined limits."""
    if value < low:
        return low_message
    elif value > high:
        return high_message
    return None

def check_warnings(value, low, high, warning_low_message, warning_high_message, tolerance):
    """Helper function to check if a value is nearing the defined limits."""
    if low <= value < low + tolerance:
        return warning_low_message
    elif high - tolerance <= value <= high:
        return warning_high_message
    return None

def battery_is_ok(temperature, soc, charge_rate, warnings_enabled=None):
    """Check if the battery parameters are within safe limits and warnings."""
    warnings_enabled = warnings_enabled or {'temperature': True, 'soc': True, 'charge_rate': True}
    tolerance = 0.05  # 5% tolerance
    
    # Check limits
    limit_checks = [
        check_limits(temperature, MAJOR_TEMP_LIMITS[0], MAJOR_TEMP_LIMITS[1],
                     'Temperature is too low!', 'Temperature is too high!'),
        check_limits(soc, SOC_LIMITS[0], SOC_LIMITS[1],
                     'State of Charge is too low!', 'State of Charge is too high!'),
        check_limits(charge_rate, 0, CHARGE_RATE_LIMIT,
                     '', 'Charge rate is too high!')
    ]
    
    for check in limit_checks:
        if check:
            return False, check
    
    # Check warnings
    warning_messages = []
    warning_checks = [
        (check_warnings(temperature, MAJOR_TEMP_LIMITS[0], MAJOR_TEMP_LIMITS[1],
                        'Warning: Approaching low temperature', 'Warning: Approaching high temperature', MAJOR_TEMP_LIMITS[1] * tolerance),
         warnings_enabled.get('temperature', True)),
        (check_warnings(soc, SOC_LIMITS[0], SOC_LIMITS[1],
                        'Warning: Approaching discharge', 'Warning: Approaching charge-peak', SOC_LIMITS[1] * tolerance),
         warnings_enabled.get('soc', True)),
        (check_warnings(charge_rate, 0, CHARGE_RATE_LIMIT,
                        '', 'Warning: Approaching charge-rate limit', CHARGE_RATE_LIMIT * tolerance),
         warnings_enabled.get('charge_rate', True))
    ]

    for warning, enabled in warning_checks:
        if warning and enabled:
            warning_messages.append(warning)
    
    return True, warning_messages

def handle_battery_check(temperature, soc, charge_rate, reporter=print, warnings_enabled=None):
    is_ok, messages = battery_is_ok(temperature, soc, charge_rate, warnings_enabled)
    if not is_ok:
        reporter(messages)  # Report failure message
        return False
    if messages:
        for msg in messages:
            reporter(msg)  # Report warnings
    return True

def custom_reporter(message):
    print(f'[ALERT] {message}')

if __name__ == '__main__':
    assert(handle_battery_check(25, 70, 0.7) is True)
    assert(handle_battery_check(50, 85, 0) is False)
    assert(handle_battery_check(-5, 70, 0.7) is False)
    assert(handle_battery_check(25, 15, 0.7) is False)
    assert(handle_battery_check(25, 70, 0.9) is False) 
    assert(handle_battery_check(50, 70, 0.7, custom_reporter) is False)

    # Custom test 
    warnings_config = {'temperature': False, 'soc': True, 'charge_rate': True}
    handle_battery_check(44, 78, 0.78, reporter=custom_reporter, warnings_enabled=warnings_config)
