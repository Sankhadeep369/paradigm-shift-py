## Battery Monitoring System - Test Specification

### Objective
To validate the correct functioning of the battery monitoring system and verify that the added warning and critical limit features work as intended.

### Parameters to Monitor
- **Temperature**: Critical range [0°C - 45°C].
- **State of Charge (SoC)**: Critical range [20% - 80%].
- **Charge Rate**: Critical upper limit [0.8].

---

### Test Scenarios

#### 1. Critical Condition Tests
Validate that the system correctly identifies conditions where parameters exceed critical limits and reports these as failures.

| **Test Case** | **Input Values**             | **Expected Output**               |
|---------------|------------------------------|-----------------------------------|
| T1            | `battery_is_ok(-5, 70, 0.7)` | "Temperature is too low!"         |
| T2            | `battery_is_ok(50, 70, 0.7)` | "Temperature is too high!"        |
| T3            | `battery_is_ok(25, 15, 0.7)` | "State of Charge is too low!"     |
| T4            | `battery_is_ok(25, 85, 0)`   | "State of Charge is too high!"    |
| T5            | `battery_is_ok(25, 70, 0.9)` | "Charge rate is too high!"        |

#### 2. Warning Condition Tests
Validate that the system issues warnings when parameters approach critical limits within a 5% tolerance.

| **Test Case** | **Input Values**             | **Expected Output**                              |
|---------------|------------------------------|--------------------------------------------------|
| W1            | `battery_is_ok(25, 19.5, 0.7)` | "Warning: Approaching discharge (19.5%)"         |
| W2            | `battery_is_ok(25, 77, 0.7)`   | "Warning: Approaching charge-peak (77%)"         |

#### 3. Normal Condition Tests
Validate that the system correctly reports normal conditions without raising warnings or alarms.

| **Test Case** | **Input Values**             | **Expected Output**                              |
|---------------|------------------------------|--------------------------------------------------|
| N1            | `battery_is_ok(25, 70, 0.7)` | No output                                        |
| N2            | `battery_is_ok(25, 70, 0.7)` | No output                                        |
| N3            | `battery_is_ok(25, 70, 0.7)` | No output                                        |

#### 4. Custom Reporter Tests
Validate that the system can output messages using a custom reporting mechanism.

| **Test Case** | **Input Values**                               | **Expected Output**                                  |
|---------------|------------------------------------------------|------------------------------------------------------|
| C1            | `battery_is_ok(50, 70, 0.7, custom_reporter)`  | "[ALERT] Temperature is too high!"                   |

---

### Edge Cases

| **Test Case** | **Input Values**              | **Expected Output**                                    |
|---------------|-------------------------------|--------------------------------------------------------|
| E1            | `battery_is_ok(25, 20, 0.7)`  | No warnings should be issued (SoC exactly at 20%)       |
| E2            | `battery_is_ok(25, 80, 0.7)`  | No warnings should be issued (SoC exactly at 80%)       |
| E3            | `battery_is_ok(25, 77, 0.7)`  | Warning: Approaching charge-peak (77%)                 |
| E4            | `battery_is_ok(25, 19.5, 0.7)`| Warning: Approaching discharge (19.5%)                 |
| E5            | `battery_is_ok(25, 70, 0.75)` | No warnings should be issued for charge rate of 0.75    |



