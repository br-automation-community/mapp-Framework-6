## AlarmX Configuration Import and Export via Python

A Python script is provided within the AlarmX package in the Logical View.

This script allows you to export the AlarmX configuration to Excel and then re-import the AlarmX configuration back into the project after you've made any necessary changes.

---

## Prerequisites for Using the Script

### 1.Download and Install Python

-> [Download](https://www.python.org/downloads/) and Install Python

---

### 2.Edit Your System Path

1.From the Control Panel, navigate to the advanced system settings. Alternatively, type "environment variables" in the start menu search bar and select "Edit the system environment variables".

   ![script1][def]

2.Click on "Environment Variables".

   ![script2][def1]

3.Click on "Path" and then "Edit".

   ![script3][def2]

4.Add the following two paths to the list:

```
   C:\Users\{username}\AppData\Local\Programs\Python\Python310
   C:\Users\{username}\AppData\Local\Programs\Python\Python310\Scripts
```
   ![script4][def3]
---

### 3.Install lxml

1.Open the command prompt (Start menu, cmd.exe).
2.Run the following command:  
   **pip install lxml**

---

## Steps to Export the Alarm Configuration to Excel

1.Open the command prompt (Start menu, cmd.exe).

2.Change directory to:

```
  <directory of project>\Logical\Infrastructure\AlarmX
```

3.Edit the following command according to your configuration name and PLC name, and then run it in the command line:
```
   - python AlarmImportExport.py --export True --csv-file .\Alarmx.csv --mpalarmxcore "..\..\..\Physical\{ConfigName}\{PLCname}\mappServices\AlarmX\AlarmXCfg.mpalarmxcore"
```
   > Note:  
   > During Python installation, if you associated .py files with the Python executable, then remove the word "python" 
   > from the beginning of the command.

4.Open the resulting AlarmX.csv file in Excel.

   The .csv file is added to the AlarmX package in the Logical View.  
   You will not see it in Automation Studio and must open it using Windows Explorer.

5.Edit the alarm list as needed using Excel.

---

## Steps to Import the Alarm Configuration from Excel

1.Close the Alarm configuration file within Automation Studio, if it is currently open.

2.Open the command prompt (Start menu, cmd.exe).

3.Change directory to:
```
   - <directory of project>\Logical\Infrastructure\AlarmX
```
4.Edit the following command according to your configuration name and PLC name, and then run it in the command line.

   Note that any changes made to the alarm configuration file in Automation Studio after exporting to Excel will be overwritten by this import.

```
   - python AlarmImportExport.py --csv-file .\Alarmx.csv --mpalarmxcore "..\..\..\Physical\{ConfigName}\{PLCname}\mappServices\AlarmX\AlarmXCfg.mpalarmxcore"

```

   > Note:  
   > During Python installation, if you associated .py files with the Python executable, then remove the word "python" 
   > from the beginning of the command.

   [def]: images/script1.png
   [def1]: images/script2.png
   [def2]: images/script3.png
   [def3]: images/script4.png
