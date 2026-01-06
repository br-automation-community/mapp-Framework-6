## 🛡️ AuditMgr Task Overview

The **AuditMgr** task contains all of the provided Framework code for **mapp Audit**.  
This task is located in the **Logical View** within the **Infrastructure package**.

The chart below provides a description of the main task and each action file.

The **AuditMgr** task is deployed to **Task Class 8** by the **Import Tool**.

### 📄 Task Files

| Filename | Type | Description |
|---------|------|-------------|
| **AuditMgr.st** | Main task code | General **mapp function block** handling.<br>Calls all actions.<br>Contains **custom event examples**. |
| **HMIActions.st** | Action | Supporting code for **HMI functionality**.<br>Handles **archive settings** and **export commands**.<br>Handles commands to **load and save** an audit configuration.<br>Sets up the **table configuration** for the query table. |
| **ExecuteQuery.st** | Action | Executes a **query**.<br>Includes the supporting **state machine** to query large amounts of data. |
| **ChangeConfiguration.st** | Action | Contains the programming to modify the **audit configuration at runtime**.<br>Modifications to this action are typically **not necessary**. |

---

### 🧾 Text Files in the Audit Package

Several **text files** are provided within the **Audit package**.

| Package name | Description |
|-------------|-------------|
| **ExportedText** | Contains the audit texts that are **exported** to the audit list.<br>These texts are typically **more detailed and longer** than the texts used for the HMI. |
| **DisplayText** | Contains the audit texts that are **displayed on the HMI**.<br>These texts typically exclude timestamp, username, and similar data, since those values can be shown in dedicated HMI columns. |
| **CommonText** | Contains texts used in **both exported and displayed** audit texts.<br>These include texts relevant for each **mapp Services audit event**. |

For details on which **text ID** corresponds to which **event type**, see AS Help.

---

### ⚙️ Localizable Alarm Texts

A **localizable text file** for the **mapp Audit alarms** is included within the **Audit package**  
(**AuditAlarms.tmx**).

These alarm texts are referenced in the **mapp Audit configuration** instead of the default alarm texts provided by **mapp Services**, which makes it easier to expand the texts to include the **language of your choice**.