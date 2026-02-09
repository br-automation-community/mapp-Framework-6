import csv
import argparse
import os
import sys
from lxml import etree as et
from dataclasses import dataclass

"""
AlarmImportExport.py

Exports/imports mapp AlarmX lists to a single tab-delimited CSV for bulk editing.
It discovers list files via the mpalarmxcore mapping and keeps extra alarm
properties via explicit columns plus dynamic "Extra:" columns.
"""

@dataclass
class EdgeAlarm:
	retain: bool
	asynchronous: bool

@dataclass
class PersistentAlarm:
	retain: bool
	asynchronous: bool

@dataclass
class DiscreteValueMonitoring:
	monitoredPV: str
	triggerValues: list
	delay: str

@dataclass
class Level:
	limit: any
	text: str

@dataclass
class LevelMonitoring:
	monitoredPV: str
	delay: str
	lowLimit: Level
	highLimit: Level
	lowLowLimit: Level = None
	highHighLimit: Level = None

@dataclass
class DeviationMonitoring:
	monitoredPV: str
	delay: str
	setpointPV: str
	lowLimit: Level
	highLimit: Level
	lowLowLimit: Level = None
	highHighLimit: Level = None

@dataclass
class RateOfChangeMonitoring:
	monitoredPV: str
	delay: str
	lowLimit: Level
	highLimit: Level
	lowLowLimit: Level = None
	highHighLimit: Level = None

# Dynamic columns for unknown/extended properties are prefixed with this.
EXTRA_PREFIX = 'Extra:'

# Explicit, well-known properties mapped to friendly CSV columns.
EXPLICIT_PATH_TO_COLUMN = {
	'Behavior/Confirm': 'Confirm',
	'Behavior/ReactionWhilePending': 'Reaction While Pending',
	'Behavior/Retain': 'Retain',
	'Behavior/Async': 'Async',
	'Behavior/Monitoring/MonitoredPV': 'Monitored PV',
	'Behavior/Monitoring/SetpointPV': 'Set Point PV',
	'Behavior/Monitoring/Settings/Delay': 'Delay',
	'Behavior/Monitoring/Settings/DelayPV': 'Delay',
	'Behavior/Recording/InactiveToActive': 'Recording Inactive To Active',
	'Behavior/Recording/UnacknowledgedToAcknowledged': 'Recording Unacknowledged To Acknowledged',
	'Behavior/Recording/AcknowledgedToUnacknowledged': 'Recording Acknowledged To Unacknowledged',
	'Behavior/Recording/UnconfirmedToConfirmed': 'Recording Unconfirmed To Confirmed',
	'Behavior/Recording/ConfirmedToUnconfirmed': 'Recording Confirmed To Unconfirmed',
	'Behavior/Recording/Update': 'Recording Update',
	'Behavior/DataUpdate/Activation/TimeStamp': 'Data Update Activation TimeStamp',
	'Behavior/DataUpdate/Activation/Snippets': 'Data Update Activation Snippets',
	'Behavior/Monitoring/Exclusive': 'Monitoring Exclusive',
	'Disable': 'Disable',
	'InhibitPV': 'Inhibit PV',
	'AdditionalInformation1': 'Additional Information 1',
	'AdditionalInformation2': 'Additional Information 2',
}

STANDARD_EXCLUDE_PATHS = {
	'Name',
	'Message',
	'Code',
	'Severity',
	'Behavior@Value',
	'Behavior/Retain',
	'Behavior/Async',
	'Behavior/Monitoring/MonitoredPV',
	'Behavior/Monitoring/SetpointPV',
	'Behavior/Monitoring/Settings/Delay',
	'Behavior/Monitoring/Settings/DelayPV',
}

STANDARD_EXCLUDE_PREFIXES = (
	'Behavior/Monitoring/TriggerValues/',
)

LIMIT_EXCLUDE_PATHS = {
	'Behavior/Monitoring/LowLimitEnable/Limit',
	'Behavior/Monitoring/LowLimitEnable/LimitPV',
	'Behavior/Monitoring/LowLimitEnable/LimitText',
	'Behavior/Monitoring/LowLowLimitEnable/Limit',
	'Behavior/Monitoring/LowLowLimitEnable/LimitPV',
	'Behavior/Monitoring/LowLowLimitEnable/LimitText',
	'Behavior/Monitoring/HighLimitEnable/Limit',
	'Behavior/Monitoring/HighLimitEnable/LimitPV',
	'Behavior/Monitoring/HighLimitEnable/LimitText',
	'Behavior/Monitoring/HighHighLimitEnable/Limit',
	'Behavior/Monitoring/HighHighLimitEnable/LimitPV',
	'Behavior/Monitoring/HighHighLimitEnable/LimitText',
}

EXPLICIT_COLUMNS = list(EXPLICIT_PATH_TO_COLUMN.values())
	
class Alarm:
	def __init__(self, name: str, message, severity, behavior, code, behaviorType: str, listFile: str = '', listId: str = '', explicitProps: dict = None, extraProps: dict = None):
		self._name = name
		self._message = message
		self._severity = severity
		self._behavior = behavior
		self._code = code
		self._behaviorType = behaviorType
		self._listFile = listFile
		self._listId = listId
		self._explicitProps = explicitProps or {}
		self._extraProps = extraProps or {}

	def __eq__(self, obj):
		return isinstance(obj, Alarm) and (self._name == obj._name) and (self._message == obj._message) and (self._severity == obj._severity) and (self._behavior == obj._behavior) and (self._code == obj._code) and (self._behaviorType == obj._behaviorType) and (self._listFile == obj._listFile) and (self._listId == obj._listId) and (self._explicitProps == obj._explicitProps) and (self._extraProps == obj._extraProps)
	
def parseDict(alarmDict: dict):
	# Convert a CSV row into an Alarm + property maps (explicit + extra).
	listFile = alarmDict['List File'] if ('List File' in alarmDict) else ''
	listId = alarmDict['List ID'] if ('List ID' in alarmDict) else ''
	name = alarmDict['Name'] if ('Name' in alarmDict) else None
	message = alarmDict['Message'] if ('Message' in alarmDict) else None
	severity = alarmDict['Severity'] if ('Severity' in alarmDict) else None
	code = alarmDict['Code'] if ('Code' in alarmDict) else None
	behaviorType = alarmDict['Behavior'] if ('Behavior' in alarmDict) else 'EdgeAlarm'
	behavior = None
	if (behaviorType == 'EdgeAlarm'):
		behavior = EdgeAlarm(alarmDict['Retain'], alarmDict['Async'])
	elif (behaviorType == 'PersistentAlarm'):
		behavior = PersistentAlarm(alarmDict['Retain'], alarmDict['Async'])
	elif (behaviorType == 'DiscreteValueMonitoring'):
		behavior = DiscreteValueMonitoring(alarmDict['Monitored PV'], alarmDict['Trigger Values'].strip('][').replace("'", '').split(', '), alarmDict['Delay'])
	elif (behaviorType == 'LevelMonitoring'):
		behavior = LevelMonitoring(alarmDict['Monitored PV'], alarmDict['Delay'], Level(alarmDict['Low Limit'], alarmDict['Low Limit Text']), Level(alarmDict['High Limit'], alarmDict['High Limit Text']), Level(alarmDict['Low Low Limit'], alarmDict['Low Low Limit Text']), Level(alarmDict['High High Limit'], alarmDict['High High Limit Text']))
	elif (behaviorType == 'DeviationMonitoring'):
		behavior = DeviationMonitoring(alarmDict['Monitored PV'], alarmDict['Delay'], alarmDict['Set Point PV'], Level(alarmDict['Low Limit'], alarmDict['Low Limit Text']), Level(alarmDict['High Limit'], alarmDict['High Limit Text']), Level(alarmDict['Low Low Limit'], alarmDict['Low Low Limit Text']), Level(alarmDict['High High Limit'], alarmDict['High High Limit Text']))
	elif (behaviorType == 'RateOfChangeMonitoring'):
		behavior = RateOfChangeMonitoring(alarmDict['Monitored PV'], alarmDict['Delay'], Level(alarmDict['Low Limit'], alarmDict['Low Limit Text']), Level(alarmDict['High Limit'], alarmDict['High Limit Text']), Level(alarmDict['Low Low Limit'], alarmDict['Low Low Limit Text']), Level(alarmDict['High High Limit'], alarmDict['High High Limit Text']))
	extraProps = {}
	explicitProps = {}
	for key, value in alarmDict.items():
		if key.startswith(EXTRA_PREFIX) and value is not None and value != '':
			extraProps[key[len(EXTRA_PREFIX):]] = value
	for path, column in EXPLICIT_PATH_TO_COLUMN.items():
		if column == 'Delay':
			continue
		if column in alarmDict and alarmDict[column] is not None and alarmDict[column] != '':
			explicitProps[path] = alarmDict[column]
	if 'Delay' in alarmDict and alarmDict['Delay'] is not None and alarmDict['Delay'] != '':
		if alarmDict['Delay'].startswith(':'):
			explicitProps['Behavior/Monitoring/Settings/DelayPV'] = alarmDict['Delay']
		else:
			explicitProps['Behavior/Monitoring/Settings/Delay'] = alarmDict['Delay']
	return Alarm(name, message, severity, behavior, code, behaviorType, listFile, listId, explicitProps, extraProps)

def parseLevel( element: et.Element) -> Level:
	if (element is None): return None
	if (element.find('Property[@ID="LimitText"]') is None):
		return None
	if (element.find('Property[@ID="Limit"]') is not None):
		value = get_prop_value(element, 'Limit')
	elif (element.find('Property[@ID="LimitPV"]') is not None):
		value = get_prop_value(element, 'LimitPV')
	text = get_prop_value(element, 'LimitText')
	if text is None:
		return None
	level = Level(value, text)
	return level

def parseLevels(selector: et.Element):
	low = None
	lowLow = None
	high = None
	highHigh = None
	levelElement = selector.find('Selector[@ID="LowLimitEnable"]')
	if (levelElement is None):
		levelElement = selector.find('Group/Selector[@ID="LowLimitEnable"]')
	if (levelElement is not None):
		low = parseLevel(levelElement)
		lowLow = parseLevel(levelElement.find('Selector[@ID="LowLowLimitEnable"]'))
	if (lowLow is None):
		levelElement = selector.find('Selector[@ID="LowLowLimitEnable"]')
		if (levelElement is None):
			levelElement = selector.find('Group/Selector[@ID="LowLowLimitEnable"]')
		lowLow = parseLevel(levelElement)
	
	levelElement = selector.find('Selector[@ID="HighLimitEnable"]')
	if (levelElement is None):
		levelElement = selector.find('Group/Selector[@ID="HighLimitEnable"]')
	if (levelElement is not None):
		high = parseLevel(levelElement)
		highHigh = parseLevel(levelElement.find('Selector[@ID="HighHighLimitEnable"]'))
	if (highHigh is None):
		levelElement = selector.find('Selector[@ID="HighHighLimitEnable"]')
		if (levelElement is None):
			levelElement = selector.find('Group/Selector[@ID="HighHighLimitEnable"]')
		highHigh = parseLevel(levelElement)
	return low, lowLow, high, highHigh

def parseDelay(settings):
	delay = None
	if settings is not None:
		delay = get_prop_value(settings, 'Delay')
		if delay is None:
			delay = get_prop_value(settings, 'DelayPV')
	return delay

def get_prop_value(element: et.Element, prop_id: str):
	prop = element.find(f'Property[@ID="{prop_id}"]')
	if prop is None:
		return None
	return prop.attrib.get('Value')

def parseAlarmElement(element: et.Element, listFile: str = '', listId: str = ''):
	# Parse an alarm entry from a list XML group.
		name = get_prop_value(element, 'Name')
		message = get_prop_value(element, 'Message')
		code = get_prop_value(element, 'Code')
		severity = get_prop_value(element, 'Severity')
		selector = element.find('Selector[@ID="Behavior"]') if (element.find('Selector[@ID="Behavior"]') is not None) else element.find('Selector')
		if (selector is None):
			behaviorType = 'EdgeAlarm'
			behavior = EdgeAlarm(False, False)
		elif ('Value' in selector.attrib):
			behaviorType = selector.attrib['Value']
			if (behaviorType == 'PersistentAlarm'):
				retain = (get_prop_value(selector, 'Retain') or 'false').lower() == 'true'
				asynchronous = (get_prop_value(selector, 'Async') or 'false').lower() == 'true'
				behavior = PersistentAlarm(retain, asynchronous)
			elif (behaviorType == 'DiscreteValueMonitoring'):
				monitoring = selector.find('Group[@ID="Monitoring"]') if (selector.find('Group[@ID="Monitoring"]') is not None) else selector.find('Group')
				variable = get_prop_value(monitoring, 'MonitoredPV') if monitoring is not None else None
				triggers = []
				if monitoring is not None:
					for trigger in monitoring.findall('Group[@ID="TriggerValues"]/Property'):
						value = trigger.attrib.get('Value')
						if value is not None:
							triggers.append(value)
					delay = parseDelay(monitoring.find('Selector[@ID="Settings"]'))
				else:
					delay = None
				behavior = DiscreteValueMonitoring(variable, triggers, delay)
			elif (behaviorType == 'LevelMonitoring'):
				monitoring = selector.find('Group[@ID="Monitoring"]') if (selector.find('Group[@ID="Monitoring"]') is not None) else selector.find('Group')
				variable = get_prop_value(monitoring, 'MonitoredPV') if monitoring is not None else None
				low, lowLow, high, highHigh = parseLevels(monitoring)
				delay = parseDelay(monitoring.find('Selector[@ID="Settings"]')) if monitoring is not None else None
				behavior = LevelMonitoring(variable, delay, low, high, lowLow, highHigh)
			elif (behaviorType == 'DeviationMonitoring'):
				monitoring = selector.find('Group[@ID="Monitoring"]') if (selector.find('Group[@ID="Monitoring"]') is not None) else selector.find('Group')
				variable = get_prop_value(monitoring, 'MonitoredPV') if monitoring is not None else None
				setPointPV = get_prop_value(monitoring, 'SetpointPV') if monitoring is not None else None
				low, lowLow, high, highHigh = parseLevels(monitoring)
				delay = parseDelay(monitoring.find('Selector[@ID="Settings"]')) if monitoring is not None else None
				behavior = DeviationMonitoring(variable, delay, setPointPV, low, high, lowLow, highHigh)
			elif (behaviorType == 'RateOfChangeMonitoring'):
				monitoring = selector.find('Group[@ID="Monitoring"]') if (selector.find('Group[@ID="Monitoring"]') is not None) else selector.find('Group')
				variable = get_prop_value(monitoring, 'MonitoredPV') if monitoring is not None else None
				low, lowLow, high, highHigh = parseLevels(monitoring)
				delay = parseDelay(monitoring.find('Selector[@ID="Settings"]')) if monitoring is not None else None
				behavior = RateOfChangeMonitoring(variable, delay, low, high, lowLow, highHigh)
			else:
				behavior = None
		else:
			behaviorType = 'EdgeAlarm'
			retain = (get_prop_value(selector, 'Retain') or 'false').lower() == 'true'
			asynchronous = (get_prop_value(selector, 'Async') or 'false').lower() == 'true'
			behavior = EdgeAlarm(retain, asynchronous)
		return Alarm(name, message, severity, behavior, code, behaviorType, listFile, listId, {}, {})

def should_include_extra(path: str) -> bool:
	if path in STANDARD_EXCLUDE_PATHS:
		return False
	if path in LIMIT_EXCLUDE_PATHS:
		return False
	if path in EXPLICIT_PATH_TO_COLUMN:
		return False
	for prefix in STANDARD_EXCLUDE_PREFIXES:
		if path.startswith(prefix):
			return False
	return True

def extract_extra_properties(element: et.Element) -> dict:
	# Walk the XML and capture properties not handled by explicit columns.
	extras = {}

	def walk(node: et.Element, path_parts: list):
		if node.tag == 'Property':
			prop_id = node.attrib.get('ID')
			if prop_id is None:
				return
			path = '/'.join(path_parts + [prop_id]) if path_parts else prop_id
			if should_include_extra(path):
				extras[path] = node.attrib.get('Value', '')
			return
		if node.tag in ('Group', 'Selector'):
			node_id = node.attrib.get('ID')
			new_parts = list(path_parts)
			if node_id is not None and not (node_id.startswith('[') and node_id.endswith(']')):
				new_parts.append(node_id)
			if node.tag == 'Selector' and 'Value' in node.attrib and node_id is not None:
				path = '/'.join(new_parts) + '@Value'
				if should_include_extra(path):
					extras[path] = node.attrib.get('Value', '')
			for child in list(node):
				walk(child, new_parts)
			return
		for child in list(node):
			walk(child, path_parts)

	for child in list(element):
		walk(child, [])
	return extras

def find_child_with_id(parent: et.Element, tag_names: list, node_id: str):
	for tag in tag_names:
		for child in parent.findall(tag):
			if child.attrib.get('ID') == node_id:
				return child
	return None

def get_property_value_by_path(element: et.Element, path: str):
	parts = path.split('/')
	if not parts:
		return None
	parent = element
	for part in parts[:-1]:
		node = find_child_with_id(parent, ['Group', 'Selector'], part)
		if node is None:
			return None
		parent = node
	prop = find_child_with_id(parent, ['Property'], parts[-1])
	if prop is None:
		return None
	return prop.attrib.get('Value', '')

def get_selector_value_by_path(element: et.Element, path: str):
	parts = path.split('/')
	parent = element
	for part in parts:
		node = find_child_with_id(parent, ['Group', 'Selector'], part)
		if node is None:
			return None
		parent = node
	return parent.attrib.get('Value')

def extract_explicit_properties(element: et.Element) -> dict:
	# Capture explicit properties for fixed CSV columns.
	values = {}
	for path in EXPLICIT_PATH_TO_COLUMN.keys():
		val = get_property_value_by_path(element, path)
		if val is not None:
			values[path] = val
	return values

def readListIdsFromCore(alarmXCore) -> list:
	if (not os.path.isfile(alarmXCore)):
		return []
	alarmXTree = et.parse(alarmXCore)
	alarmXRoot = alarmXTree.getroot()
	listConfig = alarmXRoot.find('.//Element[@Type="mpalarmxcore"]').find('.//Group[@ID="mapp.AlarmX.List"]')
	if (listConfig is None):
		return []
	listIds = []
	for group in listConfig.findall('Group'):
		listProp = group.find('Property[@ID="List"]')
		if (listProp is not None) and ('Value' in listProp.attrib):
			if 'Value' in listProp.attrib:
				listIds.append(listProp.attrib['Value'])
	return listIds

def readListIdFromFile(alarmXListFile: str):
	if (not os.path.isfile(alarmXListFile)):
		return None
	tree = et.parse(alarmXListFile)
	root = tree.getroot()
	element = root.find('.//Element[@Type="mpalarmxlist"]')
	if (element is None):
		return None
	return element.attrib.get('ID')

def resolveListFiles(alarmXCore: str) -> dict:
	baseDir = os.path.dirname(os.path.abspath(alarmXCore))
	listIds = readListIdsFromCore(alarmXCore)
	listIdToFile = {}
	for path in [x for x in os.listdir(baseDir) if x.lower().endswith('.mpalarmxlist')]:
		fullPath = os.path.join(baseDir, path)
		listId = readListIdFromFile(fullPath)
		if (listId is not None):
			listIdToFile[listId] = fullPath
	resolved = {}
	for listId in listIds:
		if (listId in listIdToFile):
			resolved[listId] = listIdToFile[listId]
		else:
			print(f'Warning: could not resolve list "{listId}" to any .mpalarmxlist file in {baseDir}')
	return resolved

def readAlarmXList(alarmXListPath: str, listId: str) -> list:
	if (not os.path.isfile(alarmXListPath)):
		return []
	alarmXTree = et.parse(alarmXListPath)
	alarmXRoot = alarmXTree.getroot()
	configuration = alarmXRoot.find('.//Element[@Type="mpalarmxlist"]').find('.//Group[@ID="mapp.AlarmX.Core.Configuration"]')
	alarmList = []
	for element in configuration.findall('Group'):
		alarm = parseAlarmElement(element, os.path.basename(alarmXListPath), listId)
		alarm._explicitProps = extract_explicit_properties(element)
		alarm._extraProps = extract_extra_properties(element)
		alarmList.append(alarm)
	return alarmList

def prettyPrintLevel(level: Level) -> list:
	if (level is None): return ['', '']
	return [level.limit, level.text]

def levelToElement(parent: et.Element, name: str, level: Level) -> et.Element:
	if (level.limit == ''):
		return None
	if (level.limit.startswith(':')):
		limitEnable = et.SubElement(parent, 'Selector', {'ID': f'{name}LimitEnable', 'Value': 'Dynamic'})
		et.SubElement(limitEnable, 'Property', {'ID': 'LimitPV', 'Value': level.limit})
	else:
		limitEnable = et.SubElement(parent, 'Selector', {'ID': f'{name}LimitEnable', 'Value': 'Static'})
		et.SubElement(limitEnable, 'Property', {'ID': 'Limit', 'Value': level.limit})
	et.SubElement(limitEnable, 'Property', {'ID': 'LimitText', 'Value': level.text})
	return limitEnable

def levelsToElement(parent: et.Element, behavior):
	if (behavior.lowLimit is not None):
		low = levelToElement(parent, 'Low', behavior.lowLimit)
		if (behavior.lowLowLimit is not None):
			levelToElement(low, 'LowLow', behavior.lowLowLimit)
	if (behavior.highLimit is not None):
		high = levelToElement(parent, 'High', behavior.highLimit)
		if (behavior.highHighLimit is not None):
			levelToElement(high, 'HighHigh', behavior.highHighLimit)

def ensure_property(parent: et.Element, prop_id: str, value):
	prop = parent.find(f'Property[@ID="{prop_id}"]')
	if prop is None:
		prop = et.SubElement(parent, 'Property', {'ID': prop_id})
	prop.attrib['Value'] = str(value)
	return prop

SELECTOR_IDS = {
	'Behavior', 'Settings',
	'LowLimitEnable', 'LowLowLimitEnable',
	'HighLimitEnable', 'HighHighLimitEnable',
}

def ensure_node(parent: et.Element, node_id: str):
	node = find_child_with_id(parent, ['Group', 'Selector'], node_id)
	if node is not None:
		return node
	if node_id in SELECTOR_IDS or node_id.endswith('Enable'):
		return et.SubElement(parent, 'Selector', {'ID': node_id})
	return et.SubElement(parent, 'Group', {'ID': node_id})

def set_property_by_path(element: et.Element, path: str, value):
	if value is None or value == '':
		return
	parts = path.split('/')
	parent = element
	for part in parts[:-1]:
		parent = ensure_node(parent, part)
	ensure_property(parent, parts[-1], value)

def set_selector_value_by_path(element: et.Element, path: str, value):
	if value is None or value == '':
		return
	parts = path.split('/')
	parent = element
	for part in parts:
		parent = ensure_node(parent, part)
	parent.attrib['Value'] = str(value)

def set_limit(monitoring: et.Element, selector_id: str, level: Level):
	if monitoring is None or level is None or level.limit is None or level.limit == '':
		return
	selector = find_child_with_id(monitoring, ['Selector'], selector_id)
	if selector is None:
		selector = et.SubElement(monitoring, 'Selector', {'ID': selector_id})
	if str(level.limit).startswith(':'):
		selector.attrib['Value'] = 'Dynamic'
		ensure_property(selector, 'LimitPV', level.limit)
	else:
		selector.attrib['Value'] = 'Static'
		ensure_property(selector, 'Limit', level.limit)
	ensure_property(selector, 'LimitText', level.text)

def update_alarm_element_from_csv(element: et.Element, alarm: Alarm, index: int) -> et.Element:
	element.attrib['ID'] = f'[{index}]'
	if alarm._name is not None and alarm._name != '':
		ensure_property(element, 'Name', alarm._name)
	if (alarm._message is not None) and (alarm._message != ''):
		ensure_property(element, 'Message', alarm._message)
	if (alarm._code is not None) and (alarm._code != '') and (alarm._code != 0):
		ensure_property(element, 'Code', str(alarm._code))
	if (alarm._severity is not None) and (alarm._severity != ''):
		ensure_property(element, 'Severity', str(alarm._severity))

	behavior = find_child_with_id(element, ['Selector'], 'Behavior')
	if behavior is None:
		behavior = et.SubElement(element, 'Selector', {'ID': 'Behavior'})
	if alarm._behaviorType is not None and alarm._behaviorType != '':
		behavior.attrib['Value'] = alarm._behaviorType

	if type(alarm._behavior) is EdgeAlarm:
		ensure_property(behavior, 'Retain', str(alarm._behavior.retain).upper())
		ensure_property(behavior, 'Async', str(alarm._behavior.asynchronous).upper())
	elif type(alarm._behavior) is PersistentAlarm:
		ensure_property(behavior, 'Retain', str(alarm._behavior.retain).upper())
		ensure_property(behavior, 'Async', str(alarm._behavior.asynchronous).upper())
	elif type(alarm._behavior) is DiscreteValueMonitoring:
		monitoring = find_child_with_id(behavior, ['Group'], 'Monitoring')
		if monitoring is None:
			monitoring = et.SubElement(behavior, 'Group', {'ID': 'Monitoring'})
		ensure_property(monitoring, 'MonitoredPV', alarm._behavior.monitoredPV)
		trigger_values = find_child_with_id(monitoring, ['Group'], 'TriggerValues')
		if trigger_values is None:
			trigger_values = et.SubElement(monitoring, 'Group', {'ID': 'TriggerValues'})
		for child in list(trigger_values.findall('Property')):
			trigger_values.remove(child)
		for idx, trigger in enumerate(alarm._behavior.triggerValues):
			et.SubElement(trigger_values, 'Property', {'ID': f'[{idx}]', 'Value': trigger})
		if alarm._behavior.delay is not None and alarm._behavior.delay != '':
			settings = find_child_with_id(monitoring, ['Selector'], 'Settings')
			if settings is None:
				settings = et.SubElement(monitoring, 'Selector', {'ID': 'Settings'})
			if alarm._behavior.delay.startswith(':'):
				settings.attrib['Value'] = '0'
				ensure_property(settings, 'DelayPV', alarm._behavior.delay)
			else:
				settings.attrib['Value'] = '0'
				ensure_property(settings, 'Delay', alarm._behavior.delay)
	elif type(alarm._behavior) is LevelMonitoring:
		monitoring = find_child_with_id(behavior, ['Group'], 'Monitoring')
		if monitoring is None:
			monitoring = et.SubElement(behavior, 'Group', {'ID': 'Monitoring'})
		ensure_property(monitoring, 'MonitoredPV', alarm._behavior.monitoredPV)
		set_limit(monitoring, 'LowLimitEnable', alarm._behavior.lowLimit)
		set_limit(monitoring, 'LowLowLimitEnable', alarm._behavior.lowLowLimit)
		set_limit(monitoring, 'HighLimitEnable', alarm._behavior.highLimit)
		set_limit(monitoring, 'HighHighLimitEnable', alarm._behavior.highHighLimit)
		if alarm._behavior.delay is not None and alarm._behavior.delay != '':
			settings = find_child_with_id(monitoring, ['Selector'], 'Settings')
			if settings is None:
				settings = et.SubElement(monitoring, 'Selector', {'ID': 'Settings'})
			if alarm._behavior.delay.startswith(':'):
				settings.attrib['Value'] = '0'
				ensure_property(settings, 'DelayPV', alarm._behavior.delay)
			else:
				settings.attrib['Value'] = '0'
				ensure_property(settings, 'Delay', alarm._behavior.delay)
	elif type(alarm._behavior) is DeviationMonitoring:
		monitoring = find_child_with_id(behavior, ['Group'], 'Monitoring')
		if monitoring is None:
			monitoring = et.SubElement(behavior, 'Group', {'ID': 'Monitoring'})
		ensure_property(monitoring, 'MonitoredPV', alarm._behavior.monitoredPV)
		ensure_property(monitoring, 'SetpointPV', alarm._behavior.setpointPV)
		set_limit(monitoring, 'LowLimitEnable', alarm._behavior.lowLimit)
		set_limit(monitoring, 'LowLowLimitEnable', alarm._behavior.lowLowLimit)
		set_limit(monitoring, 'HighLimitEnable', alarm._behavior.highLimit)
		set_limit(monitoring, 'HighHighLimitEnable', alarm._behavior.highHighLimit)
		if alarm._behavior.delay is not None and alarm._behavior.delay != '':
			settings = find_child_with_id(monitoring, ['Selector'], 'Settings')
			if settings is None:
				settings = et.SubElement(monitoring, 'Selector', {'ID': 'Settings'})
			if alarm._behavior.delay.startswith(':'):
				settings.attrib['Value'] = '0'
				ensure_property(settings, 'DelayPV', alarm._behavior.delay)
			else:
				settings.attrib['Value'] = '0'
				ensure_property(settings, 'Delay', alarm._behavior.delay)
	elif type(alarm._behavior) is RateOfChangeMonitoring:
		monitoring = find_child_with_id(behavior, ['Group'], 'Monitoring')
		if monitoring is None:
			monitoring = et.SubElement(behavior, 'Group', {'ID': 'Monitoring'})
		ensure_property(monitoring, 'MonitoredPV', alarm._behavior.monitoredPV)
		set_limit(monitoring, 'LowLimitEnable', alarm._behavior.lowLimit)
		set_limit(monitoring, 'LowLowLimitEnable', alarm._behavior.lowLowLimit)
		set_limit(monitoring, 'HighLimitEnable', alarm._behavior.highLimit)
		set_limit(monitoring, 'HighHighLimitEnable', alarm._behavior.highHighLimit)
		if alarm._behavior.delay is not None and alarm._behavior.delay != '':
			settings = find_child_with_id(monitoring, ['Selector'], 'Settings')
			if settings is None:
				settings = et.SubElement(monitoring, 'Selector', {'ID': 'Settings'})
			if alarm._behavior.delay.startswith(':'):
				settings.attrib['Value'] = '0'
				ensure_property(settings, 'DelayPV', alarm._behavior.delay)
			else:
				settings.attrib['Value'] = '0'
				ensure_property(settings, 'Delay', alarm._behavior.delay)

	for path, value in alarm._explicitProps.items():
		set_property_by_path(element, path, value)

	for path, value in alarm._extraProps.items():
		if path.endswith('@Value'):
			if path.endswith('LowLimitEnable@Value') and type(alarm._behavior) in (LevelMonitoring, DeviationMonitoring, RateOfChangeMonitoring) and alarm._behavior.lowLimit is not None and alarm._behavior.lowLimit.limit not in (None, ''):
				continue
			if path.endswith('LowLowLimitEnable@Value') and type(alarm._behavior) in (LevelMonitoring, DeviationMonitoring, RateOfChangeMonitoring) and alarm._behavior.lowLowLimit is not None and alarm._behavior.lowLowLimit.limit not in (None, ''):
				continue
			if path.endswith('HighLimitEnable@Value') and type(alarm._behavior) in (LevelMonitoring, DeviationMonitoring, RateOfChangeMonitoring) and alarm._behavior.highLimit is not None and alarm._behavior.highLimit.limit not in (None, ''):
				continue
			if path.endswith('HighHighLimitEnable@Value') and type(alarm._behavior) in (LevelMonitoring, DeviationMonitoring, RateOfChangeMonitoring) and alarm._behavior.highHighLimit is not None and alarm._behavior.highHighLimit.limit not in (None, ''):
				continue
			set_selector_value_by_path(element, path[:-6], value)
		else:
			set_property_by_path(element, path, value)

	return element

def exportAlarmXCore(csvFile, alarmXCore) -> None:
	# Export all referenced lists into one tab-delimited CSV.
	alarmList = []
	for listId, listPath in resolveListFiles(alarmXCore).items():
		alarmList.extend(readAlarmXList(listPath, listId))
	extra_columns = set()
	for alarm in alarmList:
		for key in alarm._extraProps.keys():
			extra_columns.add(EXTRA_PREFIX + key)
	extra_columns = sorted(list(extra_columns))

	header = [
		'List File', 'List ID',
		'Name', 'Message', 'Code', 'Severity',
		'Behavior', 'Retain', 'Async',
		'Confirm', 'Reaction While Pending',
		'Recording Inactive To Active', 'Recording Unacknowledged To Acknowledged', 'Recording Acknowledged To Unacknowledged',
		'Recording Unconfirmed To Confirmed', 'Recording Confirmed To Unconfirmed', 'Recording Update',
		'Data Update Activation TimeStamp', 'Data Update Activation Snippets',
		'Disable', 'Inhibit PV', 'Additional Information 1', 'Additional Information 2',
		'Monitoring Exclusive',
		'Monitored PV', 'Trigger Values', 'Set Point PV',
		'Low Low Limit', 'Low Low Limit Text', 'Low Limit', 'Low Limit Text', 'High Limit', 'High Limit Text', 'High High Limit', 'High High Limit Text',
		'Delay',
	]
	header.extend(extra_columns)
	csvData = csv.writer(open(csvFile, 'w', newline=''), dialect='excel-tab')
	csvData.writerow(header) 
	for alarm in alarmList:
		behaviorName = alarm._behaviorType if alarm._behaviorType is not None and alarm._behaviorType != '' else (alarm._behavior.__class__.__name__ if alarm._behavior is not None else 'EdgeAlarm')
		row_values = {col: '' for col in header}
		row_values['List File'] = alarm._listFile
		row_values['List ID'] = alarm._listId
		row_values['Name'] = alarm._name
		row_values['Message'] = alarm._message
		row_values['Code'] = alarm._code
		row_values['Severity'] = alarm._severity
		row_values['Behavior'] = behaviorName

		for path, column in EXPLICIT_PATH_TO_COLUMN.items():
			if path in alarm._explicitProps:
				row_values[column] = alarm._explicitProps[path]

		if (type(alarm._behavior) is EdgeAlarm):
			row_values['Retain'] = alarm._behavior.retain
			row_values['Async'] = alarm._behavior.asynchronous
		elif (type(alarm._behavior) is PersistentAlarm):
			row_values['Retain'] = alarm._behavior.retain
			row_values['Async'] = alarm._behavior.asynchronous
		elif (type(alarm._behavior) is DiscreteValueMonitoring):
			row_values['Monitored PV'] = alarm._behavior.monitoredPV
			row_values['Trigger Values'] = alarm._behavior.triggerValues
			row_values['Delay'] = alarm._behavior.delay
		elif (type(alarm._behavior) is LevelMonitoring):
			row_values['Monitored PV'] = alarm._behavior.monitoredPV
			row_values['Low Low Limit'], row_values['Low Low Limit Text'] = prettyPrintLevel(alarm._behavior.lowLowLimit)
			row_values['Low Limit'], row_values['Low Limit Text'] = prettyPrintLevel(alarm._behavior.lowLimit)
			row_values['High Limit'], row_values['High Limit Text'] = prettyPrintLevel(alarm._behavior.highLimit)
			row_values['High High Limit'], row_values['High High Limit Text'] = prettyPrintLevel(alarm._behavior.highHighLimit)
			row_values['Delay'] = alarm._behavior.delay
		elif (type(alarm._behavior) is DeviationMonitoring):
			row_values['Monitored PV'] = alarm._behavior.monitoredPV
			row_values['Set Point PV'] = alarm._behavior.setpointPV
			row_values['Low Low Limit'], row_values['Low Low Limit Text'] = prettyPrintLevel(alarm._behavior.lowLowLimit)
			row_values['Low Limit'], row_values['Low Limit Text'] = prettyPrintLevel(alarm._behavior.lowLimit)
			row_values['High Limit'], row_values['High Limit Text'] = prettyPrintLevel(alarm._behavior.highLimit)
			row_values['High High Limit'], row_values['High High Limit Text'] = prettyPrintLevel(alarm._behavior.highHighLimit)
			row_values['Delay'] = alarm._behavior.delay
		elif (type(alarm._behavior) is RateOfChangeMonitoring):
			row_values['Monitored PV'] = alarm._behavior.monitoredPV
			row_values['Low Low Limit'], row_values['Low Low Limit Text'] = prettyPrintLevel(alarm._behavior.lowLowLimit)
			row_values['Low Limit'], row_values['Low Limit Text'] = prettyPrintLevel(alarm._behavior.lowLimit)
			row_values['High Limit'], row_values['High Limit Text'] = prettyPrintLevel(alarm._behavior.highLimit)
			row_values['High High Limit'], row_values['High High Limit Text'] = prettyPrintLevel(alarm._behavior.highHighLimit)
			row_values['Delay'] = alarm._behavior.delay

		for key in extra_columns:
			row_values[key] = alarm._extraProps.get(key[len(EXTRA_PREFIX):], '')

		csvData.writerow([row_values.get(col, '') for col in header])

def readCsvFile(csvFile) -> list:
	if (not os.path.isfile(csvFile)):
		print('CSV file not found')
		return
	csvData = csv.DictReader(open(csvFile, 'r', newline=''), dialect='excel-tab')
	alarmList = []   
	for row in csvData:
		alarm = parseDict(row)
		alarmList.append(alarm)
	return alarmList

def createAlarm(alarm: Alarm, index: int) -> et.Element:
	element = et.Element('Group', {'ID': f'[{str(index)}]'})
	t = et.SubElement(element, 'Property', {'ID': 'Name', 'Value': alarm._name})
	if (alarm._message is not None) and (alarm._message != ''):
		et.SubElement(element, 'Property', {'ID': 'Message', 'Value': alarm._message})
	if (alarm._code is not None) and (alarm._code != '') and (alarm._code != 0):
		et.SubElement(element, 'Property', {'ID': 'Code', 'Value': str(alarm._code)})
	if (alarm._severity is not None) and (alarm._severity != ''):
		et.SubElement(element, 'Property', {'ID': 'Severity', 'Value': str(alarm._severity)})
	behavior_type = alarm._behaviorType if alarm._behaviorType is not None and alarm._behaviorType != '' else 'EdgeAlarm'
	if (alarm._behavior is None):
		behavior = et.SubElement(element, 'Selector', {'ID': 'Behavior', 'Value': behavior_type})
		return element
	if (type(alarm._behavior) is EdgeAlarm):
		behavior = et.SubElement(element, 'Selector', {'ID': 'Behavior', 'Value': behavior_type})
		if (alarm._behavior.retain == True):
			et.SubElement(behavior, 'Property', {'ID': 'Retain', 'Value': str(alarm._behavior.retain).upper()})
		if (alarm._behavior.asynchronous == True):
			et.SubElement(behavior, 'Property', {'ID': 'Async', 'Value': str(alarm._behavior.asynchronous).upper()})
	elif (type(alarm._behavior) is PersistentAlarm):
		behavior = et.SubElement(element, 'Selector', {'ID': 'Behavior', 'Value': 'PersistentAlarm'})
		if (alarm._behavior.retain == True):
			et.SubElement(behavior, 'Property', {'ID': 'Retain', 'Value': str(alarm._behavior.retain).upper()})
		if (alarm._behavior.asynchronous == True):
			et.SubElement(behavior, 'Property', {'ID': 'Async', 'Value': str(alarm._behavior.asynchronous).upper()})
	elif (type(alarm._behavior) is DiscreteValueMonitoring):
		behavior = et.SubElement(element, 'Selector', {'ID': 'Behavior', 'Value': 'DiscreteValueMonitoring'})
		monitoring = et.SubElement(behavior, 'Group', {'ID': 'Monitoring'})
		et.SubElement(monitoring, 'Property', {'ID': 'MonitoredPV', 'Value': alarm._behavior.monitoredPV})
		triggerValues = et.SubElement(monitoring, 'Group', {'ID': 'TriggerValues'})
		triggerIndex = 0
		for trigger in alarm._behavior.triggerValues:
			et.SubElement(triggerValues, 'Property', {'ID': f'[{triggerIndex}]', 'Value': trigger})
			triggerIndex += 1
		if (alarm._behavior.delay is not None) and (alarm._behavior.delay != ''):
			settings = et.SubElement(monitoring, 'Selector', {'ID': 'Settings'})
			if (alarm._behavior.delay.startswith(':')):
				et.SubElement(settings, 'Property', {'ID': 'DelayPV', 'Value': alarm._behavior.delay})
			else:
				et.SubElement(settings, 'Property', {'ID': 'Delay', 'Value': alarm._behavior.delay})
	elif (type(alarm._behavior) is LevelMonitoring):
		behavior = et.SubElement(element, 'Selector', {'ID': 'Behavior', 'Value': 'LevelMonitoring'})
		monitoring = et.SubElement(behavior, 'Group', {'ID': 'Monitoring'})
		et.SubElement(monitoring, 'Property', {'ID': 'MonitoredPV', 'Value': alarm._behavior.monitoredPV})
		levelsToElement(monitoring, alarm._behavior)
	elif (type(alarm._behavior) is DeviationMonitoring):
		behavior = et.SubElement(element, 'Selector', {'ID': 'Behavior', 'Value': 'DeviationMonitoring'})
		monitoring = et.SubElement(behavior, 'Group', {'ID': 'Monitoring'})
		et.SubElement(monitoring, 'Property', {'ID': 'MonitoredPV', 'Value': alarm._behavior.monitoredPV})
		et.SubElement(monitoring, 'Property', {'ID': 'SetpointPV', 'Value': alarm._behavior.setpointPV})
		levelsToElement(monitoring, alarm._behavior)
	elif (type(alarm._behavior) is RateOfChangeMonitoring):
		behavior = et.SubElement(element, 'Selector', {'ID': 'Behavior', 'Value': 'RateOfChangeMonitoring'})
		monitoring = et.SubElement(behavior, 'Group', {'ID': 'Monitoring'})
		et.SubElement(monitoring, 'Property', {'ID': 'MonitoredPV', 'Value': alarm._behavior.monitoredPV})
		levelsToElement(monitoring, alarm._behavior)
	return element
	
def updateAlarmXList(alarmXListPath, alarmList):
	if (not os.path.isfile(alarmXListPath)):
		print(f'mpAlarmXList file not found: {alarmXListPath}')
		return
	if (alarmList is None):
		print('no alarms in list')
		return
	alarmXTree = et.parse(alarmXListPath)
	alarmXRoot = alarmXTree.getroot()
	parent = alarmXRoot.find('.//Element[@Type="mpalarmxlist"]')
	config = parent.find('.//Group[@ID="mapp.AlarmX.Core.Configuration"]')

	# Merge against existing alarms to preserve properties not present in CSV.
	existing_by_name = {}
	for element in config.findall('Group'):
		name_prop = element.find('Property[@ID="Name"]')
		if name_prop is not None and 'Value' in name_prop.attrib:
			if 'Value' in name_prop.attrib:
				existing_by_name[name_prop.attrib['Value']] = element

	for element in list(config.findall('Group')):
		config.remove(element)
	index = 0
	for alarm in alarmList:
		base = None
		if alarm._name in existing_by_name:
			base = existing_by_name[alarm._name]
			element = et.fromstring(et.tostring(base, encoding='utf-8'))
		else:
			element = createAlarm(alarm, index)
		element = update_alarm_element_from_csv(element, alarm, index)
		index += 1
		config.append(element)
	et.indent(alarmXRoot, space="  ")
	alarmXTree.write(alarmXListPath, encoding="utf-8", xml_declaration=True, pretty_print=True)

def updateAlarmXLists(alarmXCore: str, alarmList: list):
	listMapping = resolveListFiles(alarmXCore)
	baseDir = os.path.dirname(os.path.abspath(alarmXCore))

	alarmsByFile = {}
	for alarm in alarmList:
		targetPath = None
		if (alarm._listFile is not None) and (alarm._listFile != ''):
			targetPath = alarm._listFile
			if (not os.path.isabs(targetPath)):
				targetPath = os.path.join(baseDir, targetPath)
		elif (alarm._listId is not None) and (alarm._listId != '') and (alarm._listId in listMapping):
			targetPath = listMapping[alarm._listId]
		if (targetPath is None):
			print(f'Warning: alarm "{alarm._name}" has no target list file/id, skipping')
			continue
		if (targetPath not in alarmsByFile):
			alarmsByFile[targetPath] = []
		alarmsByFile[targetPath].append(alarm)

	for targetPath, alarms in alarmsByFile.items():
		updateAlarmXList(targetPath, alarms)

def get_args_from_tkinter(default_csv: str, default_core: str):
	try:
		import tkinter as tk
		from tkinter import filedialog, messagebox
	except Exception as exc:
		print(f'Tkinter UI not available: {exc}')
		return None

	root = tk.Tk()
	root.title('Alarm Import/Export')
	root.resizable(False, False)

	mode = tk.StringVar(value='export')
	csv_path = tk.StringVar(value=default_csv)
	core_path = tk.StringVar(value=default_core)

	def choose_csv():
		if mode.get() == 'import':
			path = filedialog.askopenfilename(
				title='Select CSV file',
				filetypes=[('CSV files', '*.csv'), ('All files', '*.*')],
			)
		else:
			path = filedialog.asksaveasfilename(
				title='Select CSV file',
				defaultextension='.csv',
				filetypes=[('CSV files', '*.csv'), ('All files', '*.*')],
			)
		if path:
			csv_path.set(path)

	def choose_core():
		path = filedialog.askopenfilename(
			title='Select mpalarmxcore file',
			filetypes=[('mpalarmxcore files', '*.mpalarmxcore'), ('All files', '*.*')],
		)
		if path:
			core_path.set(path)

	def submit():
		if csv_path.get().strip() == '' or core_path.get().strip() == '':
			messagebox.showerror('Missing input', 'Please select both CSV and mpalarmxcore paths.')
			return
		root.quit()

	tk.Label(root, text='Mode').grid(row=0, column=0, sticky='w', padx=8, pady=6)
	tk.Radiobutton(root, text='Export', variable=mode, value='export').grid(row=0, column=1, sticky='w', padx=8, pady=6)
	tk.Radiobutton(root, text='Import', variable=mode, value='import').grid(row=0, column=2, sticky='w', padx=8, pady=6)

	tk.Label(root, text='CSV file').grid(row=1, column=0, sticky='w', padx=8, pady=6)
	tk.Entry(root, textvariable=csv_path, width=50).grid(row=1, column=1, columnspan=2, sticky='w', padx=8, pady=6)
	tk.Button(root, text='Browse', command=choose_csv).grid(row=1, column=3, sticky='w', padx=8, pady=6)

	tk.Label(root, text='mpalarmxcore').grid(row=2, column=0, sticky='w', padx=8, pady=6)
	tk.Entry(root, textvariable=core_path, width=50).grid(row=2, column=1, columnspan=2, sticky='w', padx=8, pady=6)
	tk.Button(root, text='Browse', command=choose_core).grid(row=2, column=3, sticky='w', padx=8, pady=6)

	tk.Button(root, text='Run', command=submit).grid(row=3, column=1, sticky='e', padx=8, pady=10)
	tk.Button(root, text='Cancel', command=root.destroy).grid(row=3, column=2, sticky='w', padx=8, pady=10)

	root.mainloop()
	if not root.winfo_exists():
		return None

	args = {
		'export': mode.get() == 'export',
		'csvFile': csv_path.get(),
		'alarmXCore': core_path.get(),
	}
	root.destroy()
	return args

def main() -> None:
	parser = argparse.ArgumentParser()
	parser.add_argument('-e', '--export', help='Exports the AlarmXCore configuration to a CSV file', dest='export', required=False, default=False)
	parser.add_argument('-c', '--csv-file', help='The CSV file that you want to import from', dest='csvFile', required=False, default='AlarmTriggers.csv')
	parser.add_argument('-m', '--mpalarmxcore', help='The mpalarmxcore file to read list mappings from', dest='alarmXCore', required=False, default='AlarmXCfg.mpalarmxcore')
	if len(sys.argv) == 1:
		ui_args = get_args_from_tkinter('AlarmTriggers.csv', 'AlarmXCfg.mpalarmxcore')
		if ui_args is None:
			return
		args = argparse.Namespace(**ui_args)
	else:
		args = parser.parse_args()
	
	if (args.export):
		if (not os.path.isfile(args.alarmXCore)):
			print('MpAlarmXCore file not found')
			return
		exportAlarmXCore(args.csvFile, args.alarmXCore)
	else:
		if (not os.path.isfile(args.csvFile)):
			print('CSV file not found')
			return
		alarmList = readCsvFile(args.csvFile)
		updateAlarmXLists(args.alarmXCore, alarmList)

if __name__ == '__main__':
	main()
