import xml.etree.ElementTree as ET

def parse_rule(rule):
    condition = rule.find('if')
    recommendation = rule.find('then')
    
    condition_list = [attribute.text for attribute in condition]
    recommendation_list = [attribute.text for attribute in recommendation]

    return {'if': condition_list, 'then': recommendation_list}

def parse_fact(facts):
    return [attribute.text for attribute in facts]

def parse_knowledge_base(xml_string, selected_choices):
    root = ET.fromstring(xml_string)
    
    knowledge_base = {'rules': [], 'facts': selected_choices, 'recRules': [], 'recommendations': []}
    
    for element in root:
        if element.tag == 'rule':
            knowledge_base['rules'].append(parse_rule(element))
        elif element.tag == 'recRule':
            knowledge_base['recRules'].append(parse_rule(element))
    
    return knowledge_base

def read_xml_from_file(file_path):
    with open(file_path, 'r') as file:
        xml_data = file.read()
    return xml_data