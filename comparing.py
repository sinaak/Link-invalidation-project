import measures


class Comparing:

    def __init__(self, scores, onto1, onto2):
        self.threshold = 1.0
        self.scores = scores
        self.functional_prop = []
        self.source = onto1
        self.target = onto2

    def create_functional_prop(self, threshold):
        self.threshold = threshold
        for property in self.scores.keys():
            if self.scores[property] >= threshold:
                self.functional_prop.append(property)

    def fetch(self, element1, property, threshold, possible_twins):
        # TODO
        # According to the property call the appropriate comparing function
        new_possible_twins = []
        for twin in possible_twins:
            if property.find('/date_of_birth') != -1:
                comparing_result = measures.compare_Birthdate(self.source[element1][property], self.target[twin][property])
            elif property.find('/gender') != -1:
                comparing_result = measures.compare_Gender(self.source[element1][property], self.target[twin][property])
            elif property.find('/acted_by') != -1 or property.find('/starring_in') != -1:
                comparing_result = measures.compare_ByLength(self.source[element1][property], self.target[twin][property])
            elif property.find('/name') != -1:
                comparing_result = measures.compare_Names(self.source[element1][property], self.target[twin][property])
            elif property.find('/article') != -1:
                comparing_result = measures.compareStrings(self.source[element1][property], self.target[twin][property])
            elif property.find('/amount') != -1 or property.find('calling_code') != -1 or property.find('/size') != -1\
                    or property.find('/estimated_budget_used') != -1:
                comparing_result = measures.compare_Equality(self.source[element1][property], self.target[twin][property])
            else:
                comparing_result = 0
            if comparing_result >= threshold:
                new_possible_twins.append(twin)
        return new_possible_twins

    def find_twins(self, threshold):
        res = []
        for element1 in self.source.keys():
            possible_twins = self.target.keys()
            for property in self.source[element1].keys():
                if property not in self.functional_prop:
                    continue
                possible_twins = self.fetch(element1, property, threshold, possible_twins)
            if len(possible_twins) == len(self.target.keys()):
                continue
            for twin in possible_twins:
                res.append((element1, twin))

        return res