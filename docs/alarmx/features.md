## mapp AlarmX Framework 6 Features

The following features and functionality are included in the mapp AlarmX Framework 6:

* 100 ready-made discrete value monitoring alarms and a Boolean array to trigger each alarm
* Localizable text for each alarm
* Alarm mapping by severity with reactions
* A query along with the supporting state machine to query large amounts of data
* mapp View content to display current alarms, alarm history, and the alarm query
* The ability to acknowledge and export alarms from the HMI

---

## Embedded Examples

The following examples are embedded into the Framework:

* Examples for each type of monitoring alarm.Details are provided in the comments in the **AlarmSamples.st** action file, starting on line 5.
  - Alarm names:
    - LevelMonitoringExample
    - DeviationMonitoringExample
    - RateOfChangeExample

* Example for incorporating a snippet into an alarm. This example is provided to allow easy copy and paste of the syntax for referencing a snippet in the mapp AlarmX configuration.
  - Alarm name: SnippetExample

* Example of using MpAlarmXAlarmControl to manually set and reset an alarm from code
  - Alarm name: MpAlarmXControlExample
  - The supporting code is shown in the **AlarmSamples.st** action file on lines 24–32