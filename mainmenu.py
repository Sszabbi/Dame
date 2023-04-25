class MainMenu:
	
	def __init__(self):

		print("\nWelcome to Dame! (aka. checkers) What would you like to do?")
		self.list_commdands()

	def list_commdands(self):
		print("Here's a list of options:\n")

		print("0: Play VS player")
		print("1: Play VS AI")
		print("2: Quit")
		print("Anything else: List options and choose again")
		print()

	def get_command(self):
		
		self.command = input("Enter command: ")

		try:
			self.command = int(self.command)
			assert self.command in range(0,3)
			print(f"\nAlright, option {self.command} it is!\n")
			return self.command

		except:
			self.list_commdands()
			return self.get_command()