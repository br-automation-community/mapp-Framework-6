ACTION FormatDeviceDataProvider:

	// Select CF device if USB device is not available
	FOR i := 0 TO ((SIZEOF(gUSBAvailable) / SIZEOF(gUSBAvailable[0])) - 1) DO
		IF gUSBAvailable[i] THEN
			HmiBackup.Status.DeviceDataProvider[i + 1] := '{"value":"USB';
			brsitoa(i + 1, ADR(HmiBackup.Status.DeviceDataProvider[i + 1]) + brsstrlen(ADR(HmiBackup.Status.DeviceDataProvider[i + 1])));
			brsstrcat(ADR(HmiBackup.Status.DeviceDataProvider[i + 1]), ADR('","text":"USB'));
			brsitoa(i + 1, ADR(HmiBackup.Status.DeviceDataProvider[i + 1]) + brsstrlen(ADR(HmiBackup.Status.DeviceDataProvider[i + 1])));
			brsstrcat(ADR(HmiBackup.Status.DeviceDataProvider[i + 1]), ADR('"}'));
			MpFileManagerUIConnect.DeviceList.DeviceNames[i + 1] := 'USB';
			brsitoa(i + 1, ADR(MpFileManagerUIConnect.DeviceList.DeviceNames[i + 1]) + brsstrlen(ADR(MpFileManagerUIConnect.DeviceList.DeviceNames[i + 1])));
		ELSE
			brsmemset(ADR(HmiBackup.Status.DeviceDataProvider[i + 1]), 0, SIZEOF(HmiBackup.Status.DeviceDataProvider[i + 1]));
			brsmemset(ADR(MpFileManagerUIConnect.DeviceList.DeviceNames[i + 1]), 0, SIZEOF(MpFileManagerUIConnect.DeviceList.DeviceNames[i + 1]));
		END_IF
	END_FOR

	// Configure visible device list
	HmiBackup.Status.TableConfig[0] := '{ "specRows": [{"from":';
	FOR i := 0 TO ((SIZEOF(MpFileManagerUIConnect.DeviceList.DeviceNames)/SIZEOF(MpFileManagerUIConnect.DeviceList.DeviceNames[0])) - 1) DO
		IF MpFileManagerUIConnect.DeviceList.DeviceNames[i] <> '' THEN
			DeviceCount := i + 1;
		END_IF
	END_FOR
	brsitoa((DeviceCount), ADR(HmiBackup.Status.TableConfig[0]) + brsstrlen(ADR(HmiBackup.Status.TableConfig[0])));
	brsstrcat(ADR(HmiBackup.Status.TableConfig[0]), ADR(',"to":9, "visible":false}]}'));

	// Configure visible file list
	ItemCount := MpFileManagerUIConnect.File.PathInfo.FileCount + MpFileManagerUIConnect.File.PathInfo.FolderCount;
	HmiBackup.Status.TableConfig[1] := '{ "specRows": [{"from":';
	brsitoa((ItemCount), ADR(HmiBackup.Status.TableConfig[1]) + brsstrlen(ADR(HmiBackup.Status.TableConfig[1])));
	brsstrcat(ADR(HmiBackup.Status.TableConfig[1]), ADR(',"to":50, "visible":false}]}'));

	HmiBackup.Status.FileOverMax := ItemCount > (SIZEOF(MpFileManagerUIConnect.File.List.Items)/SIZEOF(MpFileManagerUIConnect.File.List.Items[0]));

END_ACTION

ACTION SaveBackupConfiguration:
	HmiBackup.Parameters.AutomaticBackup.Type := MpBackupConfiguration.Backup.AutomaticBackup.Type;
	MpBackupConfiguration.Backup.AutomaticBackup.Data.NamePrefix := HmiBackup.Parameters.AutomaticBackup.Prefix;
	MpBackupConfiguration.Backup.AutomaticBackup.Data.DeviceName := HmiBackup.Parameters.AutomaticBackup.Device;
	MpBackupConfiguration.Backup.AutomaticBackup.Data.OverwriteOldest := HmiBackup.Parameters.AutomaticBackup.OverwriteOldest;
	MpBackupConfiguration.Backup.AutomaticBackup.Data.Mode.Schedule.Time := (((USINT_TO_UDINT(HmiBackup.Parameters.AutomaticBackup.Mode.Hour) * 60) + HmiBackup.Parameters.AutomaticBackup.Mode.Minute) * 60) * 1000;
	MpBackupConfiguration.Backup.AutomaticBackup.Data.Mode.Type := HmiBackup.Parameters.AutomaticBackup.Mode.Type;
	MpBackupConfiguration.Backup.AutomaticBackup.Data.Mode.Schedule.Day := HmiBackup.Parameters.AutomaticBackup.Mode.Day;

	// Save current backup setings to retain variable
	AutomaticBackupRetain := HmiBackup.Parameters.AutomaticBackup;

 END_ACTION

ACTION LoadBackupConfiguration:

	HmiBackup.Parameters.AutomaticBackup.Type := HmiBackup.Parameters.AutomaticBackup.Type;
	HmiBackup.Parameters.AutomaticBackup.Prefix := MpBackupConfiguration.Backup.AutomaticBackup.Data.NamePrefix;
	HmiBackup.Parameters.AutomaticBackup.Device := MpBackupConfiguration.Backup.AutomaticBackup.Data.DeviceName;
	HmiBackup.Parameters.AutomaticBackup.OverwriteOldest := MpBackupConfiguration.Backup.AutomaticBackup.Data.OverwriteOldest;
	HmiBackup.Parameters.AutomaticBackup.Mode.Hour := UDINT_TO_USINT(MpBackupConfiguration.Backup.AutomaticBackup.Data.Mode.Schedule.Time / 1000 / 60 / 60);
	HmiBackup.Parameters.AutomaticBackup.Mode.Minute := UDINT_TO_USINT(MpBackupConfiguration.Backup.AutomaticBackup.Data.Mode.Schedule.Time / 1000 / 60) - (HmiBackup.Parameters.AutomaticBackup.Mode.Hour * 60);
	HmiBackup.Parameters.AutomaticBackup.Mode.Type := MpBackupConfiguration.Backup.AutomaticBackup.Data.Mode.Type;
	HmiBackup.Parameters.AutomaticBackup.Mode.Day := MpBackupConfiguration.Backup.AutomaticBackup.Data.Mode.Schedule.Day;
END_ACTION

ACTION FileManager:

	MpFileManagerUIBackup.MpLink := ADR(gMpLinkFileManagerUIBackup);
	MpFileManagerUIBackup.UIConnect := ADR(MpFileManagerUIConnect);
	MpFileManagerUIBackup();
	FOR i := 0 TO ((SIZEOF(HmiBackup.Status.FileNames)/SIZEOF(HmiBackup.Status.FileNames[0])) - 1) DO
		HmiBackup.Status.FileNames[i] := MpFileManagerUIConnect.File.List.Items[i].Name;
		HmiBackup.Status.TimeStamps[i] := MpFileManagerUIConnect.File.List.Items[i].LastModified;
	END_FOR

	IF ((MpFileManagerUIConnect.DeviceList.SelectedIndex <> HmiBackup.Status.LastSelectedDeviceIndex) AND (MpFileManagerUIConnect.Status = mpFILE_UI_STATUS_IDLE)) THEN
		HmiBackup.Status.LastSelectedDeviceIndex := MpFileManagerUIConnect.DeviceList.SelectedIndex;
		IF HmiBackup.Status.LastSelectedIndex >= MpFileManagerUIConnect.File.PathInfo.FolderCount THEN
			HmiBackup.Status.SelectedIndex := 0;
		ELSE
			HmiBackup.Status.LastSelectedIndex := HmiBackup.Status.LastSelectedIndex + 1;
		END_IF
	END_IF

END_ACTION
