## 🛡️ mapp Audit Framework 6 Features

The following features and functionality are included in the mapp Audit Framework 6:

**Two audit systems:**

  * mapp Services events

     * This audit trail captures all built-in events related to the other mapp Services frameworks that are included in the project

  * Custom events

     * This audit trail can be used for debugging and troubleshooting the application. The intention with these custom events is that you can leave “breadcrumbs” throughout the application which can help you track down bugs in the application code. For example, if you are troubleshooting a page fault, you could trigger a custom audit event at the top of every task or in several places throughout a task to narrow down where the page fault occurs. The text for the custom audit event is provided directly to the MpAuditCustomEvent() function. For more details, see here.

**A mapp View content to view the audit list**

  * The audit systems use separate display texts, meaning the text shown on the HMI is different than the text that gets exported to the file. This allows you to show a succinct message in the message column on the HMI, and optionally add in the timestamp column / user column / etc to show additional context as needed. Then the exported audit file contains more information directly in the message.

**The ability to export an audit archive and choose your export format via the HMI**

**The ability to configure automatic archiving**

**The text system has been set up to generate applicable text for all mapp Services audit events**

**A query along with the supporting state machine to be able to query large amounts of data**

----

An example of setting up a variable monitoring audit event is provided within the framework:

* You can choose to record the value change events of specific variables by adding them to the “Variable Monitor” list in the mapp Audit Configuration

    * The provided example uses variable ::AuditMgr:VariableMonitorExample

* The localizable text definition for these events is defined in the TxtDatapoints.tmx files

    * Namespace MpAudit/DP for the exported text, and namespace MpAudit/Display/DP for the displayed text
    * The text ID must be equal to the fully resolved variable name (::AuditMgr:VariableMonitorExample in this case)

---

### 🔐 Access Rights

The ability to **configure the automatic archive export** is restricted to the **Administrators** role.

The ability to **create an immediate export** is restricted to the **Administrators** or **Service** role.

The default administrative user is **Admin** with default password **123ABc**.
The password **must be changed after import**.