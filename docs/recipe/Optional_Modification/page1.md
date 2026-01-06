## Change recipe format

By default the Framework sets up the recipe system in the XML format. The framework includes recipe configurations for both the XML and CSV formats to simplify changeover. If you'd like to switch to CSV.

The steps are as follows:

1. In RecipeMgr.var:
    * Change the datatype of variable **MpRecipeSys** to **MpRecipeCsv**
    * Change the datatype of variable **Header** to **MpRecipeCsvHeaderType**
2. In RecipeMgr.st:
    * Go to Edit → Find and Replace → Replace
    * Replace all instances of **gMpLinkRecipeXml** with **gMpLinkRecipeCsv** in the whole file. There are 8 occurrences total. 

    ![alt text](images/pic1.png) 

3. Delete or move any existing .mcfg and .par files out of the Recipe file device (by default this is F:\Recipe), since these will be the XML format. 
4. Copy the default recipe files that are provided in the CSV format (Logical View → UserPartition → Recipe → CSVformat) to the root directory of the Recipe file device. Now the recipe system will load the CSV format versions of the files by default. 


