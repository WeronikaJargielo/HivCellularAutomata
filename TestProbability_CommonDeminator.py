import unittest
from classes.Probability import *

class TestProbability_CommonDeminator(unittest.TestCase):
	
	def mySetUp(self, nominatorTestA, denominatorTestA, nominatorTestB, denominatorTestB):	
		probabilityA = Probability(nominator = nominatorTestA, denominator = denominatorTestA) 
		probabilityB = Probability(nominator = nominatorTestB, denominator = denominatorTestB) 

		return [probabilityA, probabilityB]
	
	def testPart1_checkCommonDenominator(self):
		probabilities = self.mySetUp(7, 23, 0, 5)
		probabilityA = probabilities[0]
		probabilityB = probabilities[1]
		probabilityA.commonDenominator(probabilityB)

		self.assertEqual(probabilityA.denominator, 115)		# checking denominators
		self.assertEqual(probabilityB.denominator, 115)

		self.assertEqual(probabilityA.nominator, 35)		# checking nominators
		self.assertEqual(probabilityB.nominator, 0)


	def testPart2_checkCommonDenominator(self):
		probabilities = self.mySetUp(1, 976320, 23679, 51)
		probabilityA = probabilities[0]
		probabilityB = probabilities[1]
		probabilityA.commonDenominator(probabilityB)

		self.assertEqual(probabilityA.denominator, 49792320)	# checking denominators
		self.assertEqual(probabilityB.denominator, 49792320)

		self.assertEqual(probabilityA.nominator, 51)			# checking nominators
		self.assertEqual(probabilityB.nominator, 23118281280)
	
	def testPart2_checkCommonDenominator_ZeroSituation(self):
		probabilities = self.mySetUp(1, 976320, 23679, 0)
		probabilityA = probabilities[0]
		probabilityB = probabilities[1]
		self.assertRaises(SystemExit, probabilityA.commonDenominator, probabilityB)

	
if __name__ == '__main__':
    unittest.main()