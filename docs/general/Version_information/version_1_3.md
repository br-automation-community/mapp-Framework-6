### v1.3.1

| Framework / Component | Description |
|----------------------|-------------|
| **mapp Axis** | - Improved documentation describing the requirements for converting from a pure virtual axis to a physical axis<br>- Fixed missing type member for v1.3 (`ModeManual`) in the `AxisMgr.typ` file within the AxisTemplate |
| **Miscellaneous** | Improved transfer robustness when using transfer settings **“Keep PV Values”** together with **“Installation during task operation”** |

### v1.3.0

| Framework / Component | Description |
|----------------------|-------------|
| **mapp AlarmX** | Added a Python script to export/import the alarm configuration to/from Excel |
| **mapp Axis / Cockpit** | - Enhanced the Automatic Mode mapp View content<br>- Added configuration support for SLO traces |
| **mapp Backup** | - Added visual feedback indicating that a backup is in progress (preventing parallel triggers)<br>- Fixed automatic refresh of the backup list when an automatic backup is generated |
| **mapp File** | Added more HMI feedback to indicate invalid operations |
| **mapp Recipe** | - Fixed the popup warning about a missing default recipe so it no longer appears twice<br>- Improved behavior of the recipe page up/down buttons<br>- Prevented deletion of the default recipe |
| **mapp Report** | Added the ability to sort the file list on the HMI |
| **mapp UserX** | - Added confirmation popup when deleting a user<br>- Added visual indication that the *Anonymous* user cannot be deleted<br>- Added popup informing users when they are automatically logged out |
| **mapp View** | - Standardized widget naming conventions across all frameworks<br>- Standardized AlarmX and Audit list columns<br>- Standardized button icons and button sizes across the HMI<br>- Organized and minimized required SVG images<br>- Added popup explaining why disabled buttons cannot be clicked (insufficient rights or current state) |
| **Import Tool** | - Added option to back up the project as a `.zip` file prior to import<br>- Added direct integration to the framework section in the Help (manual open button and automatic open option after import)<br>- Import the `UsbMgr` task if the Backup framework is imported on its own |
| **Miscellaneous** | - Updated file device implementation to use `USER_PATH` instead of `F:\`<br>- Minimum supported AR version is now **A4.91** due to use of `USER_PATH` |

