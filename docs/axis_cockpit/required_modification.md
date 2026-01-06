## 🔧 Required Modifications

The Framework by default provides a solid foundation, but in order to integrate it fully into your application there are a few modifications that must be made.  
The following list of modifications are required to get the Framework in a functional state within the application.

> 🚨 **IMPORTANT:**  
>  The steps on this page must be executed in order to get the Framework into a functional state!
>

---

1. If you plan to run the axis on **physical hardware** (not via a pure virtual), do the following:

     1. Add the **drive** which will control the axis to the **Physical View**.

     2. In the drive configuration, set the **axis reference** to the **MpLink** from the single axis configuration file.

     3. Delete the **VAppAxis1.purevaxcfg** file.

     4. Change the value of **MC_BR_ProcessConfig_ACP.DataType** from **mcCFG_PURE_V_AX** to **mcCFG_ACP_AX**  
      in the **ConfigurationInit** action (line 16 of **ChangeConfiguration.st** in the **AxisTemplate** package).

     If at any point you need to simulate this axis after configuring it to run on real hardware,  
     be sure to set a **version number for McAcpSim** within **Change Runtime Versions**  
     (check the **Advanced** box and then expand **mapp Motion**).

2. Implement **Automatic Mode** for the axis.This is done within the **AxisAutomatic** action of the 
   **AxisControlModes.st** file. After importing the Framework, automatic mode is **empty** and must be programmed according to the needs of the application.

3. Edit the **SimulationControl.st**, **AxisMgr.st**, **ManualCommand.st**, and **AutomaticCommand.st** files according to
   the unique application requirements of your axis.  For details about what these files are intended for, see Task Overview.

4. The **axis task(s)** should run in **cyclic 1**, and the maximum allowed cycle time is **20 ms**. Adjust the **TC1** 
   **cycle time** accordingly.

5. Change the passwords for the **Admin**, **Operator**, and **Service_Tech** users.This is done in the **User.user** file 
   in the Configuration View (**AccessAndSecurity → UserRoleSystem → User.user**). Note that if you already had users in your project with these same names prior to import, your existing users will remain unchanged and you do not need to update the passwords.

6. If you imported the **mapp View front end** with the Framework:

     1. Assign the **mapp View content** (content ID = **Axis_content**) to an area on a page within your visualization.

     2. The ability to interact with the **axis faceplate** on the **mapp View HMI** is restricted to the  
      **Administrators**, **Service**, and **Operators** roles. Therefore, add a way to **log in on the HMI**  
      (for example, by importing the **mapp UserX** framework).

     Note that on the **mapp View HMI**, a button to **activate synchronization** is provided on the **Auto** mode tab.  
     Since only **one axis** is included by default in the Framework, this button has **no effect**. This button is provided in case you add additional axes, since **synchronization is often required**.

7. If you did **not** import the mapp View front end with the Framework,connect the **HmiAxis** structure elements to your 
   visualization accordingly.