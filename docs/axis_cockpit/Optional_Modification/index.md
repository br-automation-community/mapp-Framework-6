## ⚙️ Optional Modifications

The Framework can be adjusted as needed for the application in any way necessary.  
This section summarizes some optional modifications that are commonly done to the Framework. 

• The Framework comes with the **axis template files** and **one axis already set up** (**AppAxis_1**).  
  To add an additional axis, see [here](page1.md). 

• To rename **AppAxis_1** to something that more specifically reflects its purpose, see [here](page2.md). 

• The default **homing mode** defined in the axis configuration is **Restore Position**.  
  If the restore position is not valid, then a **direct home** will be executed instead.  
  If you prefer to execute a different homing mode in this case, then change line **77** of  
  **AxisStateMachine.st** from **mcHOMING_DIRECT** to the desired mode.

**Topics in this section:**

* [Add aditional axis](page1.md)
* [Rename AppAxis_1](page2.md)
* [SLO Trace Configuration](page3.md)


