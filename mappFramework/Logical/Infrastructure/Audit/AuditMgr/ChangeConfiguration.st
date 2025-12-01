ACTION ChangeConfiguration:	
	MpAuditTrailConfigSys.MpLink := ADR(gMpLinkAuditTrail);
	MpAuditTrailConfigSys.Data := ADR(MpAuditTrailConfiguration);
	MpAuditTrailConfigSys.DataType := mpAUDIT_CFG_TRAIL;
	MpAuditTrailConfigSys.ReadFrom := mpCOM_CONFIGBASIC_SOURCE_CFG;
	MpAuditTrailConfigSys.ApplyTo := mpCOM_CONFIG_TARGET_CFG;

	IF (MpAuditTrailConfigSys.Error) THEN
		
		IF (MpAuditTrailConfigSys.StatusID = mpAUDIT_ERR_CONFIG_LOAD) THEN
			LoadAuditConfiguration;
		END_IF
		
		MpAuditTrailConfigSys.CmdRead := FALSE;
		MpAuditTrailConfigSys.CmdWrite := FALSE;
		MpAuditTrailConfigSys.ErrorReset := TRUE;
	END_IF
	MpAuditTrailConfigSys();
	MpAuditTrailConfigSys.ErrorReset := FALSE;
	IF (MpAuditTrailConfigSys.CommandDone) THEN
		IF (MpAuditTrailConfigSys.CmdRead) THEN
			LoadAuditConfiguration;
			MpAuditTrailConfigSys.CmdRead := FALSE;
		END_IF
	END_IF

END_ACTION
