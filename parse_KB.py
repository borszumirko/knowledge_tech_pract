import xml.etree.ElementTree as ET
#mukodik a github dejomost
def parse_knowledge_base(xml_content):
    # Initialize an empty dictionary to store the knowledge base
    knowledge_base = {'facts': [], 'rules': []}
    
    # Parse the XML content and get the root element
    root = ET.fromstring(xml_content)
    # Iterate over each element in the root
    for element in root:
        # Check if the element represents a fact
        if element.tag == 'fact':
            # Initialize an empty dictionary to store the fact details
            fact = {}
            
            # Extract information about the animal (name, habitat, diet)
            for sub_element in element.find('animal'):
                fact[sub_element.tag] = sub_element.text
            
            # Add the fact to the 'facts' list in the knowledge base
            knowledge_base['facts'].append(fact)

        # Check if the element represents a rule
        elif element.tag == 'rule':
            # Initialize a dictionary to represent a rule with 'if' and 'then' parts
            rule = {'if': [], 'then': {}}
            
            # Extract conditions from the 'if' part of the rule
            for condition in element.find('if'):
                rule['if'].append({
                    'property': condition.find('property').text,
                    'value': condition.find('value').text
                })
            
            # Extract the conclusion from the 'then' part of the rule
            then_element = element.find('then')
            rule['then']['text'] = then_element.find('conclusion').find('text').text
            
            # Add the rule to the 'rules' list in the knowledge base
            knowledge_base['rules'].append(rule)

    # Return the final knowledge base dictionary
    return knowledge_base

# Load XML content from file
xml_file_path = 'kb-chatgpt.xml'
with open(xml_file_path, 'r') as file:
    xml_data = file.read()

# Parse knowledge base
result = parse_knowledge_base(xml_data)

# Print the resulting knowledge base dictionary
print(result)
