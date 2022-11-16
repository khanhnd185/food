import csv

def GetKnowledgeDictCsv(filename):
    knowledge = {}
    
    with open(filename) as f:
        csvreader = csv.reader(f)
        header = next(csvreader)

        for row in csvreader:
            knowledge[row[0].lower()] = int(row[2])    

    return knowledge


anticancer_knowledge = GetKnowledgeDictCsv("data/food_compound_simplified.csv")

def GetHealthyScore(ingredients):
    score = 0

    for elements in anticancer_knowledge.keys():
        for ingredient in ingredients:
            if ingredient.find(elements) != -1:
                score += anticancer_knowledge[elements]
                break

    return score

if __name__=="__main__":
    ret = GetHealthyScore(["apple", "grape"])
    print(ret)
