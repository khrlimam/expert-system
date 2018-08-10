from models.intensity import intensity


class ProbabilityCounter:
    def __init__(self, intensitas_gejala, model):
        self.gejala_weighted = {str(x): intensity.get(intensitas_gejala.get(x), 0) for x in intensitas_gejala.keys()}
        self.set_gejala = set(self.gejala_weighted.keys())
        self.model = model

    def penyakit(self):
        return list(filter(lambda x: len(set(list(x.values())[0]).intersection(self.set_gejala)) > 0, self.model))

    def penyakit_weighted(self):
        return [{list(x.keys())[0]: [self.gejala_weighted.get(y, 0) for y in list(x.values())[0]]} for x in
                self.penyakit()]

    def probability(self):
        return [{list(x.keys())[0]: sum(list(x.values())[0]) / len(list(x.values())[0])} for x in
                self.penyakit_weighted()]

    def sort_probability_desc(self):
        return sorted(self.probability(), key=lambda item: -list(item.values())[0])

    def conclusions(self):
        return [{list(y.keys())[0]: (list(y.values())[0], 'Mean')
                 } for y in self.sort_probability_desc()]
