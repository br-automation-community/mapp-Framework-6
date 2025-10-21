ACTION ChangeConfiguration:
	MpBackupCoreConfigSys.MpLink := ADR(gMpLinkBackupCore);
	MpBackupCoreConfigSys.Data := ADR(MpBackupConfiguration);
	MpBackupCoreConfigSys.DataType := mpBACKUP_CFG_CORE;
	MpBackupCoreConfigSys.ReadFrom := mpCOM_CONFIGBASIC_SOURCE_CFG;

	IF (MpBackupCoreConfigSys.Error) THEN
		// Loading currently always throws an error about failed to write Auditing.Type
		IF (MpBackupCoreConfigSys.StatusID = mpBACKUP_ERR_CONFIG_LOAD) THEN
			LoadBackupConfiguration;
		END_IF

		MpBackupCoreConfigSys.CmdRead := FALSE;
		MpBackupCoreConfigSys.CmdWrite := FALSE;
		MpBackupCoreConfigSys.ErrorReset := TRUE;
	END_IF
	MpBackupCoreConfigSys();
	MpBackupCoreConfigSys.ErrorReset := FALSE;
	IF (MpBackupCoreConfigSys.CommandDone) THEN
		IF (MpBackupCoreConfigSys.CmdRead) THEN
			LoadBackupConfiguration;
		END_IF
		MpBackupCoreConfigSys.CmdRead := FALSE;
		MpBackupCoreConfigSys.CmdWrite := FALSE;
	END_IF

END_ACTION
