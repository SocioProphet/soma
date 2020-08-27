#!/usr/bin/env python

import sys
import xml.etree.ElementTree as ET

import os

def find_entity(name):
	for fname in os.listdir('owl'):
		fpath='owl/'+fname
		if not os.path.isfile(fpath):
			continue
		with open(fpath) as f:
			count=0
			for line in f:
				count+=1
				if '#'+name+"\">" in line:
					return (fpath,count)

def get_affected_soma_iris(xml_elem):
	affects = xml_elem.findall('{http://www.oeg-upm.net/oops}Affects')[0]
	iris = list(map(lambda x: x.text,
		affects.findall('{http://www.oeg-upm.net/oops}AffectedElement')))
	return list(filter(lambda x: "SOMA.owl" in x, iris))

def get_resource_names(iris):
	return list(map(lambda x: x.split('#')[1],iris))

def format_pitfall(name,descr,names):
	return descr+" Affected resources: "+str(names)

def report_pitfall(name,descr,level,iris):
	names = get_resource_names(iris)
	msg = format_pitfall(name,descr,names)
	if level=="Important":
		msg_level="warning"
	elif level=="Minor":
		msg_level="warning"
	else:
		msg_level="debug"
	needle = find_entity(names[0])
	if needle!=None:
		(path,line) = needle
		print("::"+msg_level+" file="+path+",line="+str(line)+"::["+level+"]"+msg)
	else:
		print("::"+msg_level+" file=SOMA.owl::["+level+"]"+msg)

def report_suggestion(name,descr,iris):
	names = get_resource_names(iris)
	msg = format_pitfall(name,descr,names)
	print("::info ::"+msg)

if __name__ == "__main__":
	# read arguments
	xml_file = sys.argv[1]
	root = ET.parse(xml_file).getroot()
	
	for pitfall_xml in root.findall('{http://www.oeg-upm.net/oops}Pitfall'):
		name  = pitfall_xml.findall('{http://www.oeg-upm.net/oops}Name')[0].text
		descr = pitfall_xml.findall('{http://www.oeg-upm.net/oops}Description')[0].text
		level = pitfall_xml.findall('{http://www.oeg-upm.net/oops}Importance')[0].text
		iris = get_affected_soma_iris(pitfall_xml)
		if len(iris)>0:
			report_pitfall(name,descr,level,iris)
	
	for suggestion_xml in root.findall('{http://www.oeg-upm.net/oops}Suggestion'):
		name  = suggestion_xml.findall('{http://www.oeg-upm.net/oops}Name')[0].text
		descr = suggestion_xml.findall('{http://www.oeg-upm.net/oops}Description')[0].text
		iris = get_affected_soma_iris(suggestion_xml)
		if len(iris)>0:
			report_suggestion(name,descr,iris)

