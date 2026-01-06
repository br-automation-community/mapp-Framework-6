## Adding Alarms

The Framework comes with **100 discrete value** monitoring alarms. If you need more discrete value monitoring alarms or any other type of alarm, add them accordingly.

The steps are as follows:

1. Increase the size of the Alarms[] array in AlarmMgr.var according to how many alarms you need to add.
2. Add the new alarms to the Alarm List in the AlarmXCfg.mpalarmxcore configuration file.
   Set the monitored PVs to the newly added elements of the Alarms[] array from step 1.
3. Define the condition to trigger each new alarm in the AlarmHandling.st action file.

> Note that it is permissible to mix and match different types of alarms.
> For example, monitoring alarms can be combined with edge or persistent alarms that are triggered via 
> MpAlarmXAlarmControl or MpAlarmXSet.

---

## Deleting Alarms

The Framework comes with 100 discrete value monitoring alarms. If you do not need all 100 alarms, delete them as required.

The steps are as follows:

1. Optionally decrease the size of the Alarms[] array in AlarmMgr.var according to how many alarms you want to remove.
2. Delete the unused alarms from the Alarm List in the AlarmXCfg.mpalarmxcore configuration file.
3. Delete the alarm assignments for the unused alarms in the AlarmHandling.st action file.

Note that these assignments may already be commented out from the initial Framework import.

---

## Deleting the Example Alarms

The Framework also includes a number of example alarms. If you do not need some or all of these examples, perform the following steps:

1. Remove members from the AlarmExamples_typ or completely delete the AlarmExamples variable in AlarmMgr.var.
2. Delete the example alarms from the top of the Alarm List in the AlarmXCfg.mpalarmxcore configuration file.
3. Edit or completely delete the AlarmSamples.st file, depending on which alarms are no longer required. If you delete the AlarmSamples.st file, also delete lines 19 and 62 of AlarmMgr.st where the AlarmSampleInit and AlarmSampleFub actions are called.


