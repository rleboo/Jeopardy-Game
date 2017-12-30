import json
import random


class Questions:
    """This class takes the Json dataset(found on reddit) and entrants the necessary information into a new dictionary
    within dictionary data structure"""
    def __init__(self):
        self.__cat = {}
        file = open("Jeopardy_questions.json", "r")
        decode = json.load(file)
        acc = 0 #Accumulator is used to restrict the number of iterations. Json file has over 200000 questions.
        for item in decode:
            word = item.get("value") #All values with None are skipped
            if word == None:
                pass
            else:
                num = (word[1:])
                num = (int(num.replace(',', ''))) # Removes extra parenthesis

            if "(<a" in item.get("question") or "<a" in item.get("question"): #Removed HTML Tags
                continue

            if "<" in item.get("question"): #Skips questions with "<" in them
                continue

            if "/" in item.get("answer") or "\"" in item.get("answer"): #Skips questions with backslashes, therefore
                #questions with apostrophes
                continue

            if len(item.get("category")) > 12: #Short Categories. Restrict the length of the category name
                continue

            if item.get("category").strip() in self.__cat:
                #If the category is already in the new dictionary, update the category with new questions and answers
                tempDic = {item.get("question").replace("\"", "")[1:-1]:item.get("answer").replace("\"", "")}
                self.__cat[item.get("category").replace("\"", "")].update(tempDic)
            else:
                self.__cat[item.get("category").replace("\"", "")]= {item.get("question").replace("\"", "")[1:-1]:(item.get("answer").replace("\"", ""))} #Removed parenthesis

            acc += 1

            if acc == 70000: #Only iterate 70,000 questions
                break
            else:
                continue
        for i in list(self.__cat):
            if len(self.__cat[i]) >= 45:
                pass
            else:
                #Removes categories with less than 45 items
                self.__cat.pop(i, None)

    def category(self):
        """This method randomly chooses five categories from the new data structure"""
        self.fun = []
        for i in range(5):
            if self.fun in list(self.__cat.keys()):
                pass
            else:
                random_Index = random.randrange(0, len(self.__cat))
                self.what = list(self.__cat.keys())[random_Index]
                self.fun.append(self.what)
        return self.fun

    def dataBank(self):
        """This method randomly chooses 5 questions from the data structure"""
        kiss = []
        self.databank = []
        for x in self.fun:
            value = random.choice(list(self.__cat[x]))
            kiss.append({value:self.__cat[x][value]})
            self.databank.append(kiss)
        return self.databank

    def questions(self, cate, quest):
        """This when given the cate== category index, and quest== row index, returns the corresponding question"""
        saywhat = list(self.databank[cate][quest].keys())
        return ",".join(str(x) for x in saywhat)


    def answer(self, cate, quest):
        """When given the category index and row index returns the corresponding question"""
        what = list(self.databank[cate][quest].values())
        return ",".join(str(x) for x in what)