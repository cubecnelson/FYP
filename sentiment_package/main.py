from nntrainer import NNTrainer
from nnactivator import NNActivator
from bydate import ByDate

class Main:

	def main(self):
		bydate = ByDate('manhattan')
		bydate.group_data()

	
m = Main()
m.main()