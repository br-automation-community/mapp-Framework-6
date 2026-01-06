## 🔁 PackMLMgr Task Overview

The **PackMLMgr** task contains all of the provided Framework code for **mapp PackML**.  
This task is located in the **Logical View** within the **PackML package**.

The chart below provides a description of the main task and each action file.

### 📄 Task Files

| Filename | Type | Description |
|---------|------|-------------|
| **PackMLMgr.st** | Main task code | General **mapp function block** handling.<br>Calls all actions. |
| **HMIActions.st** | Action | Supporting code for **HMI functionality**. |
| **StateMachine_Main.st** | Action | Empty **state machine** for the main module of the machine.<br>Contains basic functionality to allow the user to move through **PackML states**.<br>Machine-specific code may be added here. |

---

### ⚙️ Localizable Alarm Texts

A **localizable text file** for the **mapp PackML alarms** is included within the **PackML package**  
(**PackMLAlarms.tmx**).

These alarm texts are referenced in the **mapp PackML configuration** instead of the default alarm texts provided by **mapp Services**.  
This makes it easier to expand the alarm texts to include the **language of your choice**.