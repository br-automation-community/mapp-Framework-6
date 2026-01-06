## 📁 FileMgr Task Overview

The **FileMgr** task contains all of the provided Framework code for **mapp File**.  
This task is located in the **Logical View** within the **Infrastructure package**.

The **FileMgr** task is deployed to **Task Class 8** by the **Import Tool**.

---

### 📄 Task Files

| Filename | Type | Description |
|--------|------|-------------|
| **FileMgr.st** | Main task code | General **mapp function block** handling.<br>Calls all actions. |
| **HMIActions.st** | Action | Handles the **file explorer operations** for the **HMI**.<br>Note that full use of this file explorer is **exclusive to administrative users**. |
| **FIFOOperations.st** | Action | Handles the implementation of the **FIFO (first-in-first-out)** for the selected file device. |

---

### ⚙️ Localizable Alarm Texts

A **localizable text file** for the **mapp File alarms** is included within the **File package**  
(**FileAlarms.tmx**).

These alarm texts are referenced in the **mapp File manager UI configuration** instead of the default alarm texts provided by **mapp Services**, which makes it easier for you to expand the texts to include the **language of your choice**.