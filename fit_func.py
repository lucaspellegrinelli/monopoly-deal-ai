class FitnessFunction():
  def calculateFitness(self, indv):
    raise NotImplementedError("Please implement the method 'calculateFitness' in the subclass")

  def __call__(self, indv):
    return self.calculateFitness(indv)

class TestFitnessFunction(FitnessFunction):
  def calculateFitness(self, indv):
    return sum(indv.genes)
