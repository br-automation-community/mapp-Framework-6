## Required Modifications

The Framework provides a solid foundation by default.  
However, to fully integrate it into an application, several modifications are required.

The following steps must be completed to bring the Framework into a functional state within the application.

> IMPORTANT:  
> The steps on this page must be executed in order to get the Framework into a functional state.
>

---

### 1. Define the condition to trigger each alarm

* The AlarmMgr task contains a Boolean array called Alarms. Each index of the array corresponds to the monitored PV for one of the 100 predefined alarms in the AlarmX configuration.
* For each of these alarms, set the corresponding Alarms[] bit equal to the alarm condition relevant to the application.This is done in the **AlarmHandling.st action** file.

Example:  
If Alarms[0] should trigger when the light curtain is interrupted and the system is not in maintenance mode, then the alarm condition must reflect this logic.

**Alarms[0] := LightCurtainInterrupted AND NOT MaintentanceMode**

---

### 2. Define the alarm text for each alarm

* Define a unique alarm text for each alarm in the Alarms.tmx file.
* Alarms.tmx is located in the Logical View under the Infrastructure package and the AlarmX package.
* Text ID Alarm.0 corresponds to Alarm0 (Alarms[0]).Text ID Alarm.1 corresponds to Alarm1 (Alarms[1]), and so on.
* Define the alarm text for all languages relevant to the application.

---

### 3. Assign a severity to each alarm

* Assign an appropriate severity to each alarm in the Alarm List according to the alarm mapping.
* This is done in the AlarmXCfg.mpalarmxcore configuration file. The configuration file is located in the Configuration View under the CPU package, the mapp Services package, and the AlarmX package.
* By default, all alarms have a severity of 1, which corresponds to the Info reaction.
* The selected severity determines which alarm reaction is triggered.

![alarm][def]

---

### 4. Define the application response to alarm reactions

* Define how the application should respond to each alarm reaction.
* This is done using the MpAlarmXCheckReaction function calls in AlarmMgr.st, starting at line 66.
* Within each IF condition, add application-specific logic to define the machine response.
* For example:
  - Error reaction: stop all axes
  - Warning reaction: stop the machine after the next cycle
  - Info reaction: show an information popup on the HMI
* For more details on optional changes related to alarm reactions and alarm mapping, see the corresponding documentation [here](Optional_Modification/alarm_mapping.md). 

---

### 5. Change default user passwords

* Change the passwords for the Admin, Operator, and Service_Tech users. This is done in the User.user file located in the Configuration View under AccessAndSecurity, UserRoleSystem, and User.user. If users with the same names already existed in the project before importing the Framework, those users remain unchanged and the passwords do not need to be updated.

---

### 6. Integrate the HMI content

* If the mapp View front end was imported with the Framework:
  - Assign the provided mapp View content with content ID AlarmX_content to an area on a visualization page.
* If the mapp View front end was not imported:
  - Connect the elements of the HmiAlarmX structure to the visualization accordingly.
  - Refer to the relevant documentation for further details. [here](general/visualization_consideration.md)

  [def]: images/alarm3.png
