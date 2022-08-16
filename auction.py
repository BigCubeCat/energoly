from random import shuffle
from time import time

class Auction():
	def __init__(self, teamCount, buildings):
		
		
		self.teamCount = teamCount
		self.builds = []
		self.log = {}
		self.results = {}
		
		self.activeSlotCount = 1

		for i in list(buildings):
			self.builds += [objects[i]['char'] + str(j) for j in range(buildings[i])]
		
		shuffle(self.builds)
		
		
	def start(self):
		print('Аукцион запущен')
		print('Лоты: ', end='')
		print(self.builds)
		print()
		self.itemSelled = 0
		slot = activeSlot(1)
		slot.newItem(self)
		
		self.auctionIsActive = True
		while self.auctionIsActive:
			slot.update(self)			
		
		print('Аукцион завершён')
		print(self.results)
	
class activeSlot():
	def __init__(self, slotId):
		
		self.slotTime = 10
		self.id = slotId
		
		self.busy = False
		self.item = None
		self.price = 0
		self.round = 1
		self.itemSellStarted = 0
		self.winner = -1
		self.itemType = 'up'
		self.minimum_difference = 0.5

		
	
	def update(self, auction):
		if time() - self.itemSellStarted >= self.slotTime: #когда время вышло
			
			bids = self.getBids()
			bidsDict = dict(sorted(bids.items(), key=lambda x: x[1], reverse = not (self.itemType == 'down')))#сортировка словаря ставок по значению 
			bids = list(bidsDict.items()) #Перевод в список для упрощения анализа
			self.round += 1
			if (self.itemType == 'up' and float(bids[0][1])-float(bids[1][1]) > self.minimum_difference) or (self.itemType == 'down' and float(bids[1][1])-float(bids[0][1]) > self.minimum_difference):
				self.winner = bids[0][0] #одним словом - продано
				self.round = 1
				
				print(f'объект {self.item} продан команде {self.winner}')
				auction.results[self.item] = self.winner
				#print(auction.builds)
				self.newItem(auction)
				

				
				
			
			else:
				#print(self.itemType, float(bids[0][1]), float(bids[1][1]), float(bids[0][1])-float(bids[1][1]), self.minimum_difference, float(bids[0][1])-float(bids[1][1]) > self.minimum_difference)
				print('победитель в этом раунде не выявлен')
				
				print(f'раунд {self.round} начинается')
				self.itemSellStarted = time()
				
			

	def newItem(self, auction):
		#print(auction.builds)
		if len(auction.builds) == 0:
			auction.auctionIsActive = False
			return
		self.item = auction.builds[0]
		self.itemType = objects[convert[self.item[0]]]['auctionType']
		auction.builds = auction.builds[1:]
		print('\n-------------------------\n')
		print(f'Hовый предмет для торгов: {self.item}, тип аукциона {self.itemType}')
		print(f'раунд {self.round} начинается')
		self.itemSellStarted = time()
		
		
	def getBids(self): #типа запрос на фронт за ставками. одновременно является сигналом что лот пора закрывать
		print('Принимаются ставки')
		data = input() #формат для теста: 1-10 2-15 3-25   номерКоманды-ставка.   
		bidList = data.split()
		bidDict = {}
		for i in bidList:
			bid = i.split('-')
			bidDict[bid[0]] = float(bid[1]) 
		print('ставки приняты: ', end='')
		print(bidDict)
		return bidDict #{1:10, 2:15, 3:0} в таком формате приходит с фронта
		

if __name__ == '__main__':
	
	objects = {
		'house' : {
			'char' : 'h',
			'auctionType' : 'down',
			'minPrice' : 1,
			'maxPrice': 10},
			
		'solarPanel' : {
			'char' : 's',
			'auctionType' : 'up',
			'minPrice' : 1,
			'maxPrice': 10}
	}
	
	convert = {'h':'house', 's':'solarPanel'}
	auction = Auction(teamCount = 2, buildings = {'house' : 2, 'solarPanel' : 1}) 
	
	auction.start()
