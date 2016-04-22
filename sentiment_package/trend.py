class Trend:

	_retweet_sum = 0
	_related = {}
	_sum = 0;

	def setName(self,name):
		self.name = name

	def getName(self):
		return self.name

	def addToRelated(self,trend,sum):
		if trend in self._related:
			self._related.update({ trend : (self._related[trend]+sum) })
		else:
			self._related.update({ trend : sum })

	def getRelated(self):
		return self._related

	def addToSum(self,sum):
		_sum += sum

	def clear(self):
		self._related.clear()