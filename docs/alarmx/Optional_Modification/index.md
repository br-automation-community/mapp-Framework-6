**Optional Framework Modifications**

The Framework can be adjusted as needed for the application in any way necessary.

This section summarizes some optional modifications that are commonly done to the Framework.

* Adjust the provided query (ActiveAlarms) source conditions (SELECT and WHERE) in AlarmXCfg.mpalarmxcore.
* Decide how to handle the situation where the query result contains more than 20 alarms. Refer to the comments in ExecuteQuery.st starting on line 38.
* If alarms are triggered via MpAlarmXControl or MpAlarmXSet, consider setting and resetting alarms throughout the  application and not solely within the AlarmMgr task. 
    1. For example, if an error occurs in the recipe system, the alarm can be triggered directly in the recipe task.
    2. Decentralization in this way is a key benefit of mapp AlarmX. 
* By default, the provided query runs only when the Run query button is clicked on the HMI. If you want the query to run whenever new data is available, refer to the comments in the ACTIVE_ALARM_WAIT state of the ExecuteQuery action.
* In the CPU configuration, modify the mappAlarmXFiles file device to the desired storage medium. By default, this corresponds to the User partition (F:\AlarmX). 
    1. If this is changed, update or delete lines 10–16 of the AlarmMgr.st INIT program, which create the F:\AlarmX directory if it does not already exist.
* Add additional alarms or delete unused alarms (see [here](add_alarm.md) for more details).
* Adjust the alarm mapping (see [here](alarm_mapping.md) for more details).
* Inhibit specific alarms under defined conditions (see [here](inhibit.md) for more details).
* Add additional queries (see [here](add_queries.md) for more details).

**Topics in this section:**

* [Add or Delete Alarms](add_alarm.md)
* [Alarm Mapping](alarm_mapping.md)
* [Inhibit Alarms](inhibit.md)
* [Add Queries](add_queries.md)


