class CaseMatrice():
	"""
	value = valeur de la case de la matrice (valeur d'élévation)\n
	x = indice i de la position de cette case dans la matrice\n
	y = indice j de la position de cette case dans la matrice\n
	"""
	def __init__(self, value, x, y):
		self._value = value
		self._x = x
		self._y = y

		#prévention pour A*
		#self.gCost = 0
		#self.hCost = 0

	def __repr__(self):
		#return "(" + str(self.X) + "," + str(self.Y) + " : " + str(self.Value) + ")"
		return str(self.Value)

	def __lt__(self, other):
		if isinstance(other, int):
			return (self.Value < other)
		return (self.Value < other.Value)

	def __gt__(self, other):
		if isinstance(other, int):
			return (self.Value > other)
		return (self.Value > other.Value)

	@property
	def Value(self):
		return self._value
	@Value.setter
	def Value(self, value):
		self._value = value

	@property
	def X(self):
		return self._x
	@X.setter
	def X(self, value):
		self._x = value

	@property
	def Y(self):
		return self._y
	@Y.setter
	def Y(self, value):
		self._y = value

	"""
	En prévention pour algo A*

	@property
	def Gcost(self):
		return self._gCost
	@Gcost.setter
	def Gcost(self, value):
		self._gCost = value
	@property
	def Hcost(self):
		return self._hCost
	@Hcost.setter
	def Hcost(self, value):
		self._hCost = value
	@property
	def Fcost(self):
		return self._gCost + self._hCost
	"""
