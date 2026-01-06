## 🧾 mapp Recipe Framework – Task Overview

The **RecipeMgr** task contains all of the provided Framework code for **mapp Recipe**. This task is located in the **Logical View** within the **Infrastructure package**.

The **RecipeMgr** task is deployed to **Task Class 8** by the **Import Tool**.

---

### 📄 Task Files

| Filename | Type | Description |
|--------|------|-------------|
| **RecipeMgr.st** | Main task code | General **mapp function block** handling.<br>Registers **structure variables** to the two recipes.<br>Loads the **two default recipes**.<br>Calls all actions. |
| **HMIActions.st** | Action | Supporting code for **HMI functionality**, such as the **recipe preview** feature.<br>Handles all recipe commands coming from the HMI (**load**, **save**, etc.). |
| **FileOperations.st** | Action | **File handling** for copying recipes between the **User partition** and the **USB stick**. |

---

### ⚙️ Localizable Alarm Texts

A **localizable text file** for the **mapp Recipe alarms** is included within the **Recipe package** (**RecipeAlarms.tmx**).

These alarm texts are referenced in the **mapp Recipe configuration** instead of the default alarm texts provided by **mapp Services**, which makes it easier for you to expand the texts to include the **language of your choice**.