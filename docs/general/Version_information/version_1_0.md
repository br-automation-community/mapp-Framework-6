### v1.0.2

| Framework / Component | Description |
|----------------------|-------------|
| **mapp AlarmX** | No changes |
| **mapp Axis / Cockpit** | - Removed the unnecessary `MC_BR_CheckRestorePositionData` function block and now use the `IsHomed` output<br>- Updated stop deceleration |
| **mapp Backup** | - Added page up/down to the file list on the mapp View HMI<br>- Improved file list to display more than 10 backup files |
| **mapp File** | - Fixed FIFO behavior when more than 50 files are present or when max file count is set above 50<br>- Added page up/down to the file list on the mapp View HMI |
| **mapp Recipe** | - Show the name of the selected recipe in addition to the active recipe<br>- Reset recipe values before loading a new recipe |
| **mapp UserX** | No changes |
| **Import Tool** | - Aesthetic improvements<br>- Block interaction with Automation Studio while the Import Tool is open<br>- Clear indication that selecting Axis Framework also requires AlarmX and Recipe Frameworks |
| **Documentation** | - Clearer indication of actions restricted to administrative access<br>- Fixed broken links in the German Help<br>- Added description of the community-based approach<br>- Added description of the support strategy<br>- Added GitHub link |
| **Miscellaneous** | - Added MIT open source license to the project, GitHub repository, and Help file<br>- Changed development project to AS 4.8<br>- Improved USB handling code |

### v1.0.1

| Framework / Component | Description |
|----------------------|-------------|
| **mapp AlarmX** | No changes |
| **mapp Axis / Cockpit** | **Bugfixes:**<br>- Fixed manual mode set speed and stop deceleration connections<br>- Fixed bug in manual mode stopping behavior<br>- Fixed state variable capitalization<br>- Added units to datapoints |
| **mapp Backup** | No changes |
| **mapp File** | No changes |
| **mapp Recipe** | No changes |
| **mapp UserX** | No changes |
| **Import Tool** | **New behavior:**<br>- Framework no longer sets the version number automatically in *Change Runtime Versions*; this must now be set manually<br><br>**Bugfix:**<br>- Fixed issue where the importer would not launch if Automation Studio was not installed in `C:\BrAutomation\` |

### v1.0.0

| Framework / Component | Description |
|----------------------|-------------|
| **mapp AlarmX** | First release |
| **mapp Axis / Cockpit** | First release |
| **mapp Backup** | First release |
| **mapp File** | First release |
| **mapp Recipe** | First release |
| **mapp UserX** | First release |
| **Import Tool** | First release |

