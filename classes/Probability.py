
class Probability:

	def __init__(self, **kwargs):

		self.nominator = kwargs.get('nominator', -1)
		self.denominator = kwargs.get('denominator', -1)
	
	def commonDenominator(self, secondProbability):
		firstDenominator = self.denominator # denominators
		secondDenominator = secondProbability.denominator
		
		firstNominator = self.nominator # nominators
		secondNominator = secondProbability.nominator

		commmonDenominator = firstDenominator * secondDenominator 

		self.nominator = firstNominator * secondDenominator # updating probabilities
		secondProbability.nominator = secondNominator * firstDenominator

		self.denominator = commmonDenominator
		secondProbability.denominator = commmonDenominator




