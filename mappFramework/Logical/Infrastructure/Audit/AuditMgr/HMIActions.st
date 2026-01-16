ACTION ArchiveExport:

	// Assign variables to exchange with the HMI
	MpAuditTrailSys.ExportArchive := HmiAudit.Commands.ExportArchives;
	HmiAudit.Status.ArchiveAvailable := MpAuditTrailSys.ArchiveAvailable;
	HmiAudit.Status.NumberOfArchives := MpAuditTrailSys.Info.NumberArchives;

	IF (HmiAudit.Commands.ExportArchives AND MpAuditTrailSys.CommandDone) THEN
		HmiAudit.Commands.ExportArchives := FALSE;
	END_IF

END_ACTION

ACTION ArchiveSettings:

	// Audit Trail Config implementation
	MpAuditTrailConfigSys.CmdWrite := HmiAudit.Commands.SaveConfig;
	IF (HmiAudit.Commands.SaveConfig) THEN
		SaveAuditConfiguration;
	END_IF
	IF (HmiAudit.Commands.SaveConfig AND MpAuditTrailConfigSys.CommandDone) THEN
		HmiAudit.Commands.SaveConfig := FALSE;
	END_IF

END_ACTION

ACTION SaveAuditConfiguration:
	// Assign current parameters from the HMI structure to AuditTrail configuration before saving it
	MpAuditTrailConfiguration.Audit.Archive.On.Time := (((USINT_TO_UDINT(HmiAudit.Parameters.ArchiveSettings.Hour) * 60) +
	USINT_TO_UDINT(HmiAudit.Parameters.ArchiveSettings.Minute)) * 60) * 1;
	IF HmiAudit.Parameters.ArchiveSettings.Enable THEN
		MpAuditTrailConfiguration.Audit.Archive.Type := mpAUDIT_CFG_TRAIL_ARCHIVE_ON;
	ELSE
		MpAuditTrailConfiguration.Audit.Archive.Type := mpAUDIT_CFG_TRAIL_ARCHIVE_OFF;
	END_IF;
	MpAuditTrailConfiguration.Audit.Archive.On.MaximumSize := HmiAudit.Parameters.ArchiveSettings.MaxSize;
	MpAuditTrailConfiguration.Audit.Archive.On.Mode := HmiAudit.Parameters.ArchiveSettings.Mode;
	MpAuditTrailConfiguration.Audit.Export.FileType := HmiAudit.Parameters.ArchiveSettings.FileType;

	// Save current archive setings to retain variable
	ArchiveSettingsRetain := HmiAudit.Parameters.ArchiveSettings;

 END_ACTION

ACTION LoadAuditConfiguration:
	// Assign current parameters from the configuration to the HMI structure
	HmiAudit.Parameters.ArchiveSettings.Hour := UDINT_TO_USINT(MpAuditTrailConfiguration.Audit.Archive.On.Time / 1 / 60 / 60);
	HmiAudit.Parameters.ArchiveSettings.Minute := UDINT_TO_USINT(MpAuditTrailConfiguration.Audit.Archive.On.Time / 1 / 60) -
	(HmiAudit.Parameters.ArchiveSettings.Hour * 60);
	CASE MpAuditTrailConfiguration.Audit.Archive.Type OF
		mpAUDIT_CFG_TRAIL_ARCHIVE_ON : HmiAudit.Parameters.ArchiveSettings.Enable := TRUE;
		mpAUDIT_CFG_TRAIL_ARCHIVE_OFF : HmiAudit.Parameters.ArchiveSettings.Enable := FALSE;
	END_CASE;
	HmiAudit.Parameters.ArchiveSettings.MaxSize := MpAuditTrailConfiguration.Audit.Archive.On.MaximumSize;
	HmiAudit.Parameters.ArchiveSettings.Mode := MpAuditTrailConfiguration.Audit.Archive.On.Mode;
	HmiAudit.Parameters.ArchiveSettings.FileType := MpAuditTrailConfiguration.Audit.Export.FileType;

END_ACTION

ACTION QueryTableConfig:

	// Configure visible list
	TmpTableConfig := '{ "specRows": [{"from":';
	HmiAudit.Status.Query.QueryCount := 0;
	FOR i := 0 TO 9 DO
		IF HmiAudit.Status.Query.Text[i] <> "" THEN
			HmiAudit.Status.Query.QueryCount := i + 1;
		END_IF
	END_FOR
	brsitoa((HmiAudit.Status.Query.QueryCount), ADR(TmpTableConfig) + brsstrlen(ADR(TmpTableConfig)));
	brsstrcat(ADR(TmpTableConfig), ADR(',"to":19, "visible":false}]'));

	// Hide operator column for the recipe query
	IF (HmiAudit.Status.Query.Option = 0) THEN
		brsstrcat(ADR(TmpTableConfig), ADR(', "specColumns": [ {"from":2, "to":2, "visible":true}]'));
	ELSIF (HmiAudit.Status.Query.Option = 1) THEN
		brsstrcat(ADR(TmpTableConfig), ADR(', "specColumns": [ {"from":2, "to":2, "visible":false}]'));
	END_IF

	brsstrcat(ADR(TmpTableConfig), ADR('}'));
	brsstrcpy(ADR(HmiAudit.Status.TableConfig[0]), ADR(TmpTableConfig));

END_ACTION
