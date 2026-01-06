# 🧭 AppAxis_1 Task Overview

The **AppAxis_1** task contains all of the provided Framework code for **mapp Axis**.  
This task is located in the **Logical View** within the **MachineControl** package.

The **AppAxis_1** task is deployed to **Task Class 1** by the **Import Tool**.

---

### 📄 Task Files

| Filename | Type | Reference vs Unique | Description |
|--------|------|--------------------|-------------|
| **AxisMgr.st** | Main task code | **Unique / dedicated file per axis** | General **mapp function block** handling.<br>Calls all actions. |
| **AxisStateMachine.st** | Action | **Referenced file within the AxisTemplate package** | Generic **state machine** used for all axes.<br>Includes states such as power-on, homing, manual/automatic operation, stopping, etc. |
| **SimulationControl.st** | Action | **Unique / dedicated file per axis** | Supporting code for **simulation**.<br>Modify as needed for simulation requirements. |
| **AxisControlModes.st** | Action | **Unique / dedicated file per axis** | Axis-specific programming.<br>Contains **manual and automatic mode state machines**.<br>Manual mode is set up for basic jogging.<br>Automatic mode is empty by default and intended to be filled per application. |
| **Recipe.st** | Action | **Referenced file within the AxisTemplate package** | Registers axis variables to the **recipe system**.<br>Optionally add additional variables as needed. |
| **ManualCommand.st** | Function | **Unique / dedicated file per axis** | Returns **TRUE/FALSE** depending on whether a **manual mode command** has been issued.<br>Used in **AxisStateMachine.st** to handle transitions between manual and automatic mode.<br>Change the ManualCommand assignment as needed.<br>This function allows the AxisStateMachine to remain **generic**. |
| **AutomaticCommand.st** | Function | **Unique / dedicated file per axis** | Returns **TRUE/FALSE** depending on whether an **automatic mode command** has been issued.<br>Used in **AxisStateMachine.st** to handle transitions between manual and automatic mode.<br>Change the AutomaticCommand assignment as needed.<br>This function allows the AxisStateMachine to remain **generic**. |
| **ChangeConfiguration.st** | Action | **Referenced file within the AxisTemplate package** | Sets up the ability to change **configuration settings at runtime**.<br>Modifications to this action are typically **not necessary**. |

---

### 🔁 Flow Chart

(Flow chart description / diagram follows)

![Flowchart](images/pic1.png)