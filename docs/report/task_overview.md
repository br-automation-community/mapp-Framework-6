## 📊 ReportMgr Task Overview

The **ReportMgr** task contains all of the provided Framework code for **mapp Report**.  
This task is located in the **Logical View** within the **Infrastructure package**.

The chart below provides a description of the main task and each action file.

The **ReportMgr** task is deployed to **Task Class 8** by the **Import Tool**.

### 📄 Task Files

| Filename | Type | Description |
|---------|------|-------------|
| **ReportMgr.st** | Main task code | General **mapp function block** handling.<br>Calls all actions.<br>Populates sample data. |
| **HMIActions.st** | Action | Supporting code for **HMI functionality**.<br>Handles the selection between **simple** and **advanced** reports.<br>Manages the **report file explorer**. |

---

### ⚙️ Localizable Alarm Texts

A **localizable text file** for the **mapp Report alarms** is included within the **Report package**  
(**ReportAlarms.tmx**).

These alarm texts are referenced in the **mapp Report configuration** instead of the default alarm texts provided by **mapp Services**, which makes it easier to expand the texts to include the **language of your choice**.