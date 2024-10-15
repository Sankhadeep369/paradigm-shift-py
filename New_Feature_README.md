Battery Monitoring System
This project monitors a battery's status based on three parameters:

Temperature: Must stay within a safe range to avoid battery damage.
State of Charge (SoC): Ensures the battery does not overcharge or undercharge.
Charge Rate: Keeps charge rate within safe operating limits.
Features Added
Early Warning System:
Introduced a warning system that provides early alerts when the battery parameters approach critical limits. For temperature, SoC, and charge rate, the system issues a warning when the parameters come within 5% of the upper or lower limit.

For example:

If SoC should be between 20% and 80%, a warning will be issued if the SoC drops below 20% or rises above 76%.
Temperature warnings are issued based on critical lower and upper thresholds.
Parameter-Specific Warnings:
The warning system allows for future customization where the user can enable or disable warnings for specific parameters without major code changes.

Modularity and Maintainability:
The code has been refactored to improve modularity by separating parameter checks (temperature, SoC, charge rate) into individual functions. This approach simplifies adding new checks and enhances readability. The cyclomatic complexity (CCN) of the code has been reduced to ensure easier maintainability and readability.

Customizable Reporting:
Introduced a custom_reporter that allows users to define how alerts and warnings are displayed. The default reporter prints messages to the console, but users can customize this behavior.

