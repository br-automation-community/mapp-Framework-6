## 🧭 mapp Axis Framework

The following features and functionality are included in the **mapp Axis Framework**:  

• **Single-axis implementation** which can be repeated for multiple axes.  
  Includes basic commands, **manual/automatic modes**, and an overarching **state machine** for axis control  

• **Cyclic data exchange** for current, lag error, and motor temperature  

• **Detailed alarm integration** with **mapp AlarmX**  

• **Automatic setup** of **mapp Cockpit**  

• **mapp View content** to show the **axis faceplate**  

---

The **mapp Axis Framework** is designed so that the main axis control code within the **AxisTemplate** package is reused for all axes that you add. This makes it easy to update the overall process for **all axes simultaneously**.

Any modifications made to the following files within this package will apply to **all axes**:

• **AxisMgr.var**  
• **AxisStateMachine.st**  
• **ChangeConfiguration.st**  
• **Recipe.st**  

The Framework comes with the **AxisTemplate** package as well as **one application axis** set up for you in the **AppAxis_1** package. To add additional axes, see [here](Optional_Modification/page1.md).

---

**Axis-specific code** is written within a **dedicated package** for that axis.For more details, see [here](required_modification.md).

---

### 🔐 Access Rights

The ability to interact with the **axis faceplate** on the **mapp View HMI** is restricted to the  
**Administrators**, **Service**, and **Operators** roles.

The default administrative user is **Admin** with default password **123ABc**.  
The password **must be changed after import**.

---

### 🏠 Homing Behavior

The homing mode is **mcHOMING_RESTORE_POSITION**.

• If you power on and a **homing position exists and is valid**, it is **automatically restored**.  

• If you power on and a **homing position does not exist**, an **alarm will trigger** to notify you.  
  At that point, you must execute a **homing command**, which corresponds to **mcHOMING_DIRECT**.

---

### ⚠️ Automatic Mode Behavior

Please note that in **Automatic mode**, **active alarms** will prevent the axis from running.

To start running the axis in **Automatic mode**, **all alarms must be acknowledged**.