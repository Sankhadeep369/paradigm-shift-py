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


def battery_is_ok(temperature, soc, charge_rate, reporter=print):

    for parameter, limits in BATTERY_LIMITS.items():
        critical_lower = limits.get("critical_lower")
        critical_upper = limits.get("critical_upper")
        warning_lower = calculate_warning_thresholds(critical_lower)
        warning_upper = calculate_warning_thresholds(critical_upper)

        if critical_lower and temperature < critical_lower:
            reporter(f"Temperature is too low! ({temperature}°C)")
            return False
        elif critical_upper and temperature > critical_upper:
            reporter(f"Temperature is too high! ({temperature}°C)")
            return False

        if warning_lower and soc < warning_lower:
            reporter(f"Warning: Approaching discharge ({soc}%)")
        elif warning_upper and soc > warning_upper:
            reporter(f"Warning: Approaching charge-peak ({soc}%)")

        if critical_upper and soc > critical_upper:
            reporter(f"State of Charge is too high! ({soc}%)")
            return False

        if critical_lower and soc < critical_lower:
            reporter(f"State of Charge is too low! ({soc}%)")
            return False

        if critical_upper and charge_rate > critical_upper:
            reporter(f"Charge rate is too high! ({charge_rate})")
            return False

    return True


def custom_reporter(message):
    """Prints messages with an alert prefix."""
    print(f"[ALERT] {message}")


if __name__ == "__main__":
    assert battery_is_ok(25, 70, 0.7) is True
    assert battery_is_ok(50, 85, 0) is False
    assert battery_is_ok(-5, 70, 0.7) is False
    assert battery_is_ok(25, 15, 0.7) is False
    assert battery_is_ok(25, 70, 0.9) is False
    assert battery_is_ok(50, 70, 0.7, custom_reporter) is False
