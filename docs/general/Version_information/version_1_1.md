### v1.1.0

| Framework / Component | Description |
|----------------------|-------------|
| **mapp AlarmX** | Fixed MpLink error on `MpAlarmXListUI` and `MpAlarmXHistoryUI` |
| **mapp Audit** | New framework component |
| **mapp Axis / Cockpit** | - Automatically reset the axis function block when all related alarms are acknowledged<br>- Added a status bar for the axis faceplate<br>- Added a move velocity command to the axis faceplate |
| **mapp Backup** | - Show a pop-up when a new automatic backup is available<br>- Removed the backup size from the HMI |
| **mapp File** | - Made the FIFO configuration persistent<br>- Fixed FIFO deletion behavior when more than 50 files are on the monitored file device<br>- Prevent editing the FIFO configuration while FIFO is actively deleting files<br>- Added a visual indicator on the HMI showing which file device has FIFO activated |
| **mapp Recipe** | Improved the implementation of the preview window on the HMI |
| **mapp UserX** | - Fixed the EditUser SVG so `imageColor` can be changed correctly<br>- Warn the user when exporting a user list with the same filename as an existing file<br>- Updated configuration settings to better align with **21 CFR Part 11** |
| **mapp View** | - Resolved benign mapp View errors in the logbook<br>- Standardized all main content sizes |
| **Import Tool** | - Improved import functionality<br>- Improved organization of the selection page<br>- Improved overall aesthetics<br>- Updated to AS API 4.0 (requires **AS 4.10 – AS 4.12**) |
| **Documentation** | Improvements to the German translation of the Help |
| **Miscellaneous** | Removed all usage of `TON_10ms` |
