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

	def setup_vs_ai(self):
		'''
			Choose Team to play as, and how smart the robot should be.
		'''
		team = input("Enter 0 to play as White, anything else for Black.\nTeam: ") == "0"
		IQ = -1
		MaxIQ = 3
		print(f"How smart should the robot be on a semi-logarithmic scale of 0 to {MaxIQ}?")
		while IQ not in range(MaxIQ+1):
			
			try:
				IQ = int(input("Smarts: "))
			except:
				print(f"No, you don't understand, please try again. Pick a whole number from 0 to {MaxIQ}. Please.")
			else:
				if IQ > MaxIQ:
					print("Sorry, but technology just isn't there yet. Please pick a lower number.")

				elif IQ < 0:
					print("ha-ha. very funny. no.")

		return team, IQ

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