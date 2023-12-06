import xml.etree.ElementTree as ET

def parse_rule(rule):
    condition = rule.find('if')
    recommendation = rule.find('then')
    
    condition_list = [attribute.text for attribute in condition]
    recommendation_list = [attribute.text for attribute in recommendation]

    return {'if': condition_list, 'then': recommendation_list}

def parse_fact(facts):
    return [attribute.text for attribute in facts]

def parse_knowledge_base(xml_string):
    root = ET.fromstring(xml_string)
    
    knowledge_base = {'rules': [], 'facts': [], 'recRules': [], 'recommendations': []}
    
    for element in root:
        if element.tag == 'rule':
            knowledge_base['rules'].append(parse_rule(element))
        elif element.tag == 'fact':
            knowledge_base['facts']=(parse_fact(element))
        elif element.tag == 'recRule':
            knowledge_base['recRules'].append(parse_rule(element))
    
    return knowledge_base

def read_xml_from_file(file_path):
    with open(file_path, 'r') as file:
        xml_data = file.read()
    return xml_data

def prtDict(dict):
    print('---')
    for rule in dict:
        for key, value in rule.items():
            print(f"{key}: {value}")
        print('---')

def print_KB():
    print('Rules:')
    prtDict(knowledge_base['rules'])
    print('Recommendation rules:')
    prtDict(knowledge_base['recRules'])
    print('Facts:')
    print(knowledge_base['facts'])
    print('---')
    print('Recommendations:')
    print(knowledge_base['recommendations'])

def forward_chaining():
    empty = 0
    while empty != 1:
        new = []
        for rule in knowledge_base['rules']:
            premises = rule['if']
            conclusions = rule['then']
            flag = 1
            for premise in premises:
                if premise not in knowledge_base['facts']:
                    flag = 0

            if flag == 1:
                for conclusion in conclusions:
                    if conclusion not in knowledge_base['facts']:
                        new.append(conclusion)

        if new == []:
            empty = 1
        else:
            for item in new:
                knowledge_base['facts'].append(item)

        print(f"\tNew Inferred Facts: {new}")

def find_recommendations():
    for recRule in knowledge_base['recRules']:
        conditions = recRule['if']
        recommendations = recRule['then']
        if set(conditions).issubset(set(knowledge_base['facts'])):
            knowledge_base['recommendations'].append(recommendations)



# Read XML data
xml_file_path = 'fishKB.xml'
xml_data = read_xml_from_file(xml_file_path)

# Parse XML
knowledge_base = parse_knowledge_base(xml_data)

print_KB()
forward_chaining()
find_recommendations()
print_KB()




