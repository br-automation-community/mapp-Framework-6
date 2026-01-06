## ⚙️ Optional Modifications

The Framework can be adjusted as needed for the application in any way necessary.  
This section summarizes some optional modifications that are commonly done to the Framework. 

• In the **CPU configuration**, modify the **mappBackupFiles** file device to the desired storage medium.  
  By default, this corresponds to the **User partition** (**F:\Backup**).

  -> If you do, modify or delete lines **10–16** of the **BackupMgr.st INIT** program, which creates the directory **F:\Backup** if it does not already exist.