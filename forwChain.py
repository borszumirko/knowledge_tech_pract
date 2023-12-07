
def forward_chaining(knowledge_base):
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

def find_recommendations(knowledge_base):
    for recRule in knowledge_base['recRules']:
        conditions = recRule['if']
        recommendations = recRule['then']
        if set(conditions).issubset(set(knowledge_base['facts'])):
            knowledge_base['recommendations'].append(recommendations)