## AlarmMgr Task Overview

The **AlarmMgr** task contains all of the provided Framework code for mapp AlarmX.

This task is located in the Logical View within the Infrastructure package.  
The chart below provides a description of the main task and each action file.

The **AlarmMgr** task is deployed to Task Class 1 by the Import Tool.

---

## AlarmMgr Task Files

| Filename | Type | Description |
|---------|------|-------------|
| AlarmMgr.st | Main task code | General mapp function block handling.<br>Handles alarm acknowledgment.<br>Handles alarm history export.<br>Checks if any reactions are active.<br>Calls all actions. |
| AlarmHandling.st | Action | Defines the conditions which trigger each alarm.<br>The AlarmMgr task contains a Boolean array called Alarms. Each index of the array corresponds to the Monitored PV for each of the 100 predefined alarms in the AlarmX configuration.<br>This is also the designated place to define the conditions under which alarms should be inhibited, if inhibiting is required in the application. |
| HMIActions.st | Action | Shows the alarm backtrace information on the HMI.<br>Typically, the backtrace action (GetBacktraceInformation) does not need to be modified.<br>Also sets up the table configuration for the query table. |
| ExecuteQuery.st | Action | Executes a query.<br>Includes the supporting state machine used to query large amounts of data. |
| AlarmSamples.st | Action | Calls the variables for the examples built into the Framework.<br>Contains comments explaining each example. |