from sys import exit
class Probability:

	def __init__(self, **kwargs):

		self.nominator = kwargs.get('nominator', -1)
		self.denominator = kwargs.get('denominator', -1)
	
	###---bring probabilities to a common denominator---###
	def commonDenominator(self, secondProbability):
    		
		if (self.denominator == 0 or secondProbability.denominator == 0):
			print('One of denominators is 0')
			exit()

		# denominators
		firstDenominator = self.denominator 
		secondDenominator = secondProbability.denominator
		
		# nominators
		firstNominator = self.nominator 
		secondNominator = secondProbability.nominator

		commmonDenominator = firstDenominator * secondDenominator 

		# updating probabilities
		self.nominator = firstNominator * secondDenominator 
		secondProbability.nominator = secondNominator * firstDenominator

		self.denominator = commmonDenominator
		secondProbability.denominator = commmonDenominator
