## 💾 BackupMgr Task Overview

The **BackupMgr** task contains all of the provided Framework code for **mapp Backup**.  
This task is located in the **Logical View** within the **Infrastructure package**.

The **BackupMgr** task is deployed to **Task Class 8** by the **Import Tool**.

---

### 📄 Task Files

| Filename | Type | Description |
|--------|------|-------------|
| **BackupMgr.st** | Main task code | General **mapp function block** handling.<br>This task contains all of the necessary code to **create**, **restore**, and **delete** a backup of the program. |
| **HMIActions.st** | Action | Supporting code for **HMI functionality**.<br>Loads and saves the **backup configuration**.<br>Handles the **file manager**. |
| **ChangeConfiguration.st** | Action | Contains the programming to modify the **backup configuration at runtime**.<br>Modifications to this action are typically **not necessary**. |

---

### ⚙️ Localizable Alarm Texts

A **localizable text file** for the **mapp Backup alarms** is included within the **Backup package**  
(**BackupAlarms.tmx**).

These alarm texts are referenced in the **mapp Backup configuration** instead of the default alarm texts provided by **mapp Services**, which makes it easier for you to expand the texts to include the **language of your choice**.