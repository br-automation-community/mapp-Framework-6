**Optional Framework Modifications**

The Framework can be adjusted as needed for the application in any way necessary.

This section summarizes some optional modifications that are commonly done to the Framework.

* Change to CSV format
* In the CPU configuration, modify the “mappRecipeFiles” file device to the desired storage medium. By default, this corresponds to the User partition (F:\Recipe). 
    * If you do, modify or delete lines 10-16 of the RecipeMgr.st INIT program, which creates the directory F:\Recipe if it does not already exist. 

**Topics in this section:**

* [Change recipe format](page1.md)



