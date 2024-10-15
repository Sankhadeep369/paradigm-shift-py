Test Specification Document

Objective:
To validate the correct functioning of the battery monitoring system and verify that the added warning and critical limit features work as intended.

Parameters to Monitor:
•	Temperature: Critical range [0°C - 45°C].
•	State of Charge (SoC): Critical range [20% - 80%].
•	Charge Rate: Critical upper limit [0.8].

Test Scenarios:
1.	Critical Condition Tests:
Validate that the system correctly identifies conditions where parameters exceed critical limits and reports these as failures.
o	T1: Temperature too low (below 0°C).
o	T2: Temperature too high (above 45°C).
o	T3: SoC too low (below 20%).
o	T4: SoC too high (above 80%).
o	T5: Charge rate too high (above 0.8).

2.	Warning Condition Tests:
Validate that the system issues warnings when parameters approach critical limits within a 5% tolerance.
o	W1: SoC approaching low critical limit (between 19% - 20%).
o	W2: SoC approaching high critical limit (between 76% - 80%).

3.	Normal Condition Tests:
Validate that the system correctly reports normal conditions without raising warnings or alarms.
o	N1: Temperature within safe range (e.g., 25°C).
o	N2: SoC within safe range (e.g., 70%).
o	N3: Charge rate within safe range (e.g., 0.7).

4.	Custom Reporter Tests:
Validate that the system can output messages using a custom reporting mechanism.
o	C1: Use a custom reporter to print alerts with a specific message format.

Test Cases:
Test Case	Input Values	Expected Output	Result
T1	battery_is_ok(-5, 70, 0.7)	"Temperature is too low!"	Pass
T2	battery_is_ok(50, 70, 0.7)	"Temperature is too high!"	Pass
T3	battery_is_ok(25, 15, 0.7)	"State of Charge is too low!"	Pass
T4	battery_is_ok(25, 85, 0)	"State of Charge is too high!"	Pass
T5	battery_is_ok(25, 70, 0.9)	"Charge rate is too high!"	Pass
W1	battery_is_ok(25, 19.5, 0.7)	"Warning: Approaching discharge (19.5%)"	Pass
W2	battery_is_ok(25, 77, 0.7)	"Warning: Approaching charge-peak (77%)"	Pass
N1	battery_is_ok(25, 70, 0.7)	No output	Pass
N2	battery_is_ok(25, 70, 0.7)	No output	Pass
N3	battery_is_ok(25, 70, 0.7)	No output	Pass
C1	battery_is_ok(50, 70, 0.7, custom_reporter)	"[ALERT] Temperature is too high!"	Pass

Edge Cases:
1.	Exact Threshold Test:
Verify that no warning is issued when the SoC is exactly at the lower or upper limit (20% and 80%).
o	E1: battery_is_ok(25, 20, 0.7) should pass without warnings.
o	E2: battery_is_ok(25, 80, 0.7) should pass without warnings.

2.	Upper Bound Warning Test:
Verify that warnings are correctly issued when SoC approaches but does not exceed critical limits.
o	E3: battery_is_ok(25, 77, 0.7) should issue a charge-peak warning.

3.	Lower Bound Warning Test:
Verify that warnings are correctly issued when SoC approaches but does not exceed lower critical limits.
o	E4: battery_is_ok(25, 19.5, 0.7) should issue a discharge warning.
4.	No Warning for Charge Rate:
Since charge rate does not have a warning limit, ensure that no warning is issued when the charge rate approaches 0.8.
o	E5: battery_is_ok(25, 70, 0.75) should pass without warnings.

