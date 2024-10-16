BATTERY_LIMITS = {
    "temperature": {
        "critical_lower": 0,
        "critical_upper": 45,
        "warning_lower": None,
        "warning_upper": None,
    },
    "soc": {
        "critical_lower": 20,
        "critical_upper": 80,
        "warning_lower": 19,
        "warning_upper": 76,
    },
    "charge_rate": {
        "critical_upper": 0.8,
        "warning_upper": None,  # No early warning for charge rate
    },
}


def calculate_warning_thresholds(critical_limit):
    """Calculates the warning threshold based on the critical limit."""
    return critical_limit * 0.95 if critical_limit else None


def is_below_critical(value, lower_limit):
    return lower_limit is not None and value < lower_limit


def is_above_critical(value, upper_limit):
    return upper_limit is not None and value > upper_limit


def report_critical_breach(parameter, value, lower_limit, upper_limit, reporter):
    """Handles critical breach reporting."""
    if is_below_critical(value, lower_limit):
        reporter(f"{parameter} is too low! ({value})")
        return False
    if is_above_critical(value, upper_limit):
        reporter(f"{parameter} is too high! ({value})")
        return False
    return True


def report_lower_warning(parameter, value, warning_lower, reporter, message):
    """Handles lower warning reporting."""
    if warning_lower is not None and value < warning_lower:
        reporter(message)


def report_upper_warning(parameter, value, warning_upper, reporter, message):
    """Handles upper warning reporting."""
    if warning_upper is not None and value > warning_upper:
        reporter(message)


def report_warning_breach(parameter, value, warning_lower, warning_upper, reporter, lower_message, upper_message):
    """Handles warning breach reporting."""
    report_lower_warning(parameter, value, warning_lower, reporter, lower_message)
    report_upper_warning(parameter, value, warning_upper, reporter, upper_message)


def check_temperature(temperature, reporter):
    limits = BATTERY_LIMITS["temperature"]
    return report_critical_breach("Temperature", temperature, limits["critical_lower"], limits["critical_upper"], reporter)


def check_soc(soc, reporter):
    limits = BATTERY_LIMITS["soc"]
    report_warning_breach("SoC", soc, limits["warning_lower"], limits["warning_upper"], reporter,
                          f"Warning: Approaching discharge ({soc}%)",
                          f"Warning: Approaching charge-peak ({soc}%)")
    return report_critical_breach("State of Charge", soc, limits["critical_lower"], limits["critical_upper"], reporter)


def check_charge_rate(charge_rate, reporter):
    critical_upper = BATTERY_LIMITS["charge_rate"]["critical_upper"]
    return report_critical_breach("Charge rate", charge_rate, None, critical_upper, reporter)


def battery_is_ok(temperature, soc, charge_rate, reporter=print):
    """Orchestrates the checks for all parameters and returns the final status."""
    checks = [
        check_temperature(temperature, reporter),
        check_soc(soc, reporter),
        check_charge_rate(charge_rate, reporter),
    ]
    return all(checks)


def custom_reporter(message):
    """Prints messages with an alert prefix."""
    print(f"[ALERT] {message}")


# Tests to validate
if __name__ == "__main__":
    assert battery_is_ok(25, 70, 0.7) is True
    assert battery_is_ok(50, 85, 0) is False
    assert battery_is_ok(-5, 70, 0.7) is False
    assert battery_is_ok(25, 15, 0.7) is False
    assert battery_is_ok(25, 70, 0.9) is False
    assert battery_is_ok(50, 70, 0.7, custom_reporter) is False
