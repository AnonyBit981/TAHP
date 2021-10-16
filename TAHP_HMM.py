import json
import re
from prettytable import PrettyTable
import collections

class TAHP_HMM:
	DEFAULT_DIR = 'Username'
	outStateProbability = None
	
	def __init__(self, filename = None):
		if filename == None:
			return
		data = self.extractMessage(filename)
		commands = self.gatherCommands(data)
		self.outStateProbability = self.findProbability(commands)

	def getOutStateProbability(self) -> dict:
		return self.outStateProbability

	def printOutStateProbability(self) -> None:
		print('\n-----------------------------------------------\n')
		for superKey in outStateProbability.keys():
			t = PrettyTable(['Out State', 'Probaility'])
			print('Current State = '+superKey)
			for key in outStateProbability[superKey].keys():
				t.add_row([key, outStateProbability[superKey][key]])
			print(t)
			print('\n-----------------------------------------------\n')

	def initOutStateProbability(self) -> dict():
		outStateProbability = dict()
		outStateProbability[self.DEFAULT_DIR] = dict()
		outStateProbability[self.DEFAULT_DIR][self.DEFAULT_DIR] = 0
		return outStateProbability

	def extractMessage(self, filename: str) -> list:
		data = []
		try:
			for line in open(filename, 'r'):
				jsonLine = json.loads(line)['message']
				if len(re.findall('CMD', str(jsonLine))) != 1:
					continue
				data.append(json.loads(line)['message'])
		except FileNotFoundError:
			print('File Not Found')
		return data

	def gatherCommands(self, data: list) -> list: 
		listCommands = list()
		for line in data:
			commands = line[5:].split(';')
			if commands!=[]:
				listCommands.append(commands)
		return listCommands

	def findProbability(self, listCommands: list) -> dict:
		sourceCount = dict()
		sourceCount[self.DEFAULT_DIR] = 0
		outStateProbability = self.initOutStateProbability()#forms 2d matrix

		pattern = '(?:\/(?:\w+))+'
		for commands in listCommands:
			for command in commands:
				dir_list = re.findall(pattern, command)
				if len(dir_list) == 0:
					outStateProbability[self.DEFAULT_DIR][self.DEFAULT_DIR] += 1 
					sourceCount[self.DEFAULT_DIR] += 1
				elif len(dir_list) == 1:
					outStateProbability[self.DEFAULT_DIR][dir_list[0]] = outStateProbability[self.DEFAULT_DIR].get(dir_list[0],0) + 1
					sourceCount[self.DEFAULT_DIR] += 1
				elif len(dir_list) == 2:
					if dir_list[0] not in outStateProbability:
						outStateProbability[dir_list[0]] = dict()
						sourceCount[dir_list[0]] = 0
					outStateProbability[dir_list[0]][dir_list[1]] = outStateProbability[dir_list[0]].get(dir_list[1],0) + 1
					sourceCount[dir_list[0]] += 1
		for superKey in outStateProbability.keys():
			for key in outStateProbability[superKey].keys():
				outStateProbability[superKey][key] = outStateProbability[superKey][key] / sourceCount[superKey]
		return outStateProbability

if __name__ == '__main__':
	filename = 'cowrie_temp.json'
	obj = TAHP_HMM(filename)
	outStateProbability = obj.getOutStateProbability()
	obj.printOutStateProbability()