## 🔧 Required Modifications

The Framework by default provides a **solid foundation**, but in order to integrate it fully into your application, a few modifications must be made.

The following list of modifications is required to get the Framework into a **functional state** within the application.

>
> 🚨 **IMPORTANT:**  
> The steps on this page must be executed in order to get the Framework into a functional state.

---

### 1. Change default user passwords

Change the passwords for the **Admin**, **Operator**, and **Service_Tech** users.

This is done in the **User.user** file in the **Configuration View**  
(**AccessAndSecurity → UserRoleSystem → User.user**).

If users with the same names already existed in the project prior to importing the Framework, those users will remain unchanged and the passwords do not need to be updated.

---

### 2. Integrate the HMI content

If you imported the **mapp View front end** with the Framework, assign the **mapp View content**  
(content ID = **PackML_content**) to an area on a page within your visualization.

If you did not import the mapp View front end, connect the **HmiPackML** structure elements to your visualization accordingly (see here for more details).

---

### 3. Implement the PackML state machine

The action file **StateMachine_Main.st** under **PackMLMgr** contains an **empty state machine** that the user may fill out.

This state machine contains:
* Actions for each **PackML state** of the **PackMLMain** module
* A line of code indicating which states require a **StateComplete** command to move on to the next state

The user should add actions for each state **before** a **StateComplete** command is sent.

In the **mpPACKML_STATE_COMPLETING** state, a **temporary line of code** has been added to allow the empty state machine to function.

This temporary line of code should be **removed** and the **StateComplete** command **uncommented** once the user has added the required code for this state.