## ⚙️ Optional Modifications

The Framework can be adjusted as needed for the application in any way necessary.This section summarizes some optional modifications that are commonly done to the Framework. 

**Modify the available roles and users** if desired.

  1. This is done in the **Role.role** and **User.user** files in the **Configuration View**.

  2. If you make changes, be sure to update the **UserXCfg.mpuserx** configuration file as well.

    ▪ Note that users only need to be added to the **UserXCfg.mpuserx** configuration file  
      if you want to utilize the **Language**, **Measurement system**, or **Additional Data** properties for that user.  
      **mapp UserX** automatically has access to all users listed in **User.user**.  

    ▪ Similarly, note that roles only need to be added to the **UserXCfg.mpuserx** configuration file  
      if you want to specify **administrative or access rights**. **mapp UserX** automatically has access to all roles listed in **Role.role**. 

In the **CPU configuration**, modify the **mappUserXFiles** file device to the desired storage medium.  By default, this corresponds to the **User partition** (**F:\UserX**).
  
  1. If you do, modify or delete lines **10–16** of the **UserXMgr.st INIT** program, which creates the directory **F:\UserX** if it does not already exist.