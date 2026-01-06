## Adding Additional Queries

The **ExecuteQuery.st action** file contains the programming required to execute the query that comes with the Framework, the ActivateAlarms query.

It also contains the supporting state machine that is used to query large amounts of data.

---

If you would like to add an additional query, the following steps are required.

### 1. AlarmMgr.var

1. Copy and paste the variable declaration for QueryActiveAlarms and give it a unique name.  
   Each query needs a dedicated function block instance.

2. Copy and paste the variable declaration for AlarmQuery and give it a unique name.

---

### 2. AlarmXCfg.mpalarmxcore configuration file

1. Define the new query in the Data Queries section at the bottom of the configuration file.  
   Give it a unique name.

2. Use the new query variable created in step 1.2 for the process variable connections and update count.

---

### 3. ExecuteQuery.st

Copy and paste lines 3–47 of ExecuteQuery.st to duplicate the code.Then within the copied code:

1. Replace every instance of QueryActiveAlarms with the new function block name created in step 1.1.
2. Replace the query name assignment with the name of the new query created in step 2.1.
      - NewQueryFUB.Name := ADR('NewQueryNameFromStep2.1');
3. Replace every instance of AlarmQuery with the new variable name created in step 1.2.

4. If you would like the new query to run only based on a button press.Add a new boolean within HmiAlarmX.Commands for the new trigger. Update the IF statement accordingly within the ACTIVE_ALARM_WAIT state. 

---

Repeat these steps for all additional queries.


