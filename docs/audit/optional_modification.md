## ⚙️ Optional Modifications

The Framework can be adjusted as needed for the application in any way necessary. This section summarizes some optional modifications that are commonly done to the Framework.

*  Implement custom audit events throughout the application as needed for debugging during development. These audit events correspond to the custom event audit trail. The full process is as follows:

    1.  Increase the value of MAX_CUSTOM_EVENTS within AuditMgr.var according to how many custom events you will use. 
    2. Define the text for the type, message, and comment of each custom audit event in the CustomEvent variable structure. This is done in the initialization program of AuditMgr.st starting on line 35. Alternatively, you can do this directly in the "Value" column of AuditMgr.var. These texts will be used when calling the MpAuditCustomEvent() function block. Note that you can only provide the texts in one language (they are not localizable).
    3.  Trigger the custom events throughout the application. Examples for how to do this are shown starting on line 75 of AuditMgr.st.

* The localizable text files for mapp Services audit events are provided in the Infrastructure/Audit package of the Logical View. These files were originally taken from the MpAudit library, but they were expanded upon for the framework. Edit the text entries as needed. 
* In the CPU configuration, modify the “mappAuditFiles” file device to the desired storage medium. By default, this corresponds to the User partition (F:\\Audit). 
    1.  If you do, modify or delete lines 10-16 of the AuditMgr.st INIT program, which creates the directory F:\\Audit if it does not already exist.