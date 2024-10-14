MAJOR_TEMP_LIMITS = (0, 45)
SOC_LIMITS = (20, 80)
CHARGE_RATE_LIMIT = 0.8
TOLERANCE_PERCENTAGE = 0.05


def check_temperature_limits(temperature):
    """Check temperature for critical limits."""
    if temperature < MAJOR_TEMP_LIMITS[0]:
        return False, 'Temperature is too low!'
    if temperature > MAJOR_TEMP_LIMITS[1]:
        return False, 'Temperature is too high!'
    return True, ''


def check_soc_limits(soc):
    """Check State of Charge (SoC) for critical limits."""
    if soc < SOC_LIMITS[0]:
        return False, 'State of Charge is too low!'
    if soc > SOC_LIMITS[1]:
        return False, 'State of Charge is too high!'
    return True, ''


def check_charge_rate_limits(charge_rate):
    """Check charge rate for critical limits."""
    if charge_rate > CHARGE_RATE_LIMIT:
        return False, 'Charge rate is too high!'
    return True, ''


def check_temperature_warnings(temperature):
    """Check temperature for warning levels."""
    tolerance = MAJOR_TEMP_LIMITS[1] * TOLERANCE_PERCENTAGE
    if MAJOR_TEMP_LIMITS[0] <= temperature < MAJOR_TEMP_LIMITS[0] + tolerance:
        return 'Warning: Approaching low temperature'
    if MAJOR_TEMP_LIMITS[1] - tolerance <= temperature <= MAJOR_TEMP_LIMITS[1]:
        return 'Warning: Approaching high temperature'
    return None


def check_soc_warnings(soc):
    """Check State of Charge (SoC) for warning levels."""
    tolerance = SOC_LIMITS[1] * TOLERANCE_PERCENTAGE
    if SOC_LIMITS[0] <= soc < SOC_LIMITS[0] + tolerance:
        return 'Warning: Approaching discharge'
    if SOC_LIMITS[1] - tolerance <= soc <= SOC_LIMITS[1]:
        return 'Warning: Approaching charge-peak'
    return None


def check_charge_rate_warnings(charge_rate):
    """Check charge rate for warning levels."""
    tolerance = CHARGE_RATE_LIMIT * TOLERANCE_PERCENTAGE
    if CHARGE_RATE_LIMIT - tolerance <= charge_rate <= CHARGE_RATE_LIMIT:
        return 'Warning: Approaching charge-rate limit'
    return None


def battery_is_ok(temperature, soc, charge_rate, warnings_enabled=None):
    """Check battery limits and warnings."""
    warnings_enabled = warnings_enabled or {'temperature': True, 'soc': True, 'charge_rate': True}
    # Critical checks
    temp_ok, temp_message = check_temperature_limits(temperature)
    if not temp_ok:
        return False, temp_message
    
    soc_ok, soc_message = check_soc_limits(soc)
    if not soc_ok:
        return False, soc_message

    charge_rate_ok, charge_rate_message = check_charge_rate_limits(charge_rate)
    if not charge_rate_ok:
        return False, charge_rate_message
    
    # Warning checks
    warning_messages = []
    if warnings_enabled.get('temperature', True):
        temp_warning = check_temperature_warnings(temperature)
        if temp_warning:
            warning_messages.append(temp_warning)
    
    if warnings_enabled.get('soc', True):
        soc_warning = check_soc_warnings(soc)
        if soc_warning:
            warning_messages.append(soc_warning)
    
    if warnings_enabled.get('charge_rate', True):
        charge_rate_warning = check_charge_rate_warnings(charge_rate)
        if charge_rate_warning:
            warning_messages.append(charge_rate_warning)
    
    return True, warning_messages


# To keep the purity of the function, the printing and reporting happens outside the core logic.
def handle_battery_check(temperature, soc, charge_rate, reporter=print, warnings_enabled=None):
    is_ok, messages = battery_is_ok(temperature, soc, charge_rate, warnings_enabled)
    if not is_ok:
        reporter(messages)  # Directly report failure message
        return False
    if messages:
        for msg in messages:
            reporter(msg)  # Report warnings
    return True

def custom_reporter(message):
    print(f'[ALERT] {message}')


# Tests to validate
if __name__ == '__main__':
    assert(handle_battery_check(25, 70, 0.7) is True)
    assert(handle_battery_check(50, 85, 0) is False)
    assert(handle_battery_check(-5, 70, 0.7) is False)
    assert(handle_battery_check(25, 15, 0.7) is False)
    assert(handle_battery_check(25, 70, 0.9) is False) 
    assert(handle_battery_check(50, 70, 0.7, custom_reporter) is False)

    # Custom test with warnings disabled for temperature
    warnings_config = {'temperature': False, 'soc': True, 'charge_rate': True}
    handle_battery_check(44, 78, 0.78, reporter=custom_reporter, warnings_enabled=warnings_config)
