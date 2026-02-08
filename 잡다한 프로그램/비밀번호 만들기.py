import random

def get_four_number_list():
	numbers = []
	
	random_int = []
	
	# Not Duplicated
	while(len(numbers) != 5):
		random_int = random.randint(0,9)
		
		if not random_int in numbers:
			numbers.append(random_int)
		
	return numbers

def get_four_character_list():
	characters = []
	
	upper_number = random.randint(1,4)
	lower_number = 5 - upper_number
	
	# Not duplicated
	random_upper_characters = []
	while(len(random_upper_characters) != upper_number):
		random_upper_character_temp = chr(ord("A") + random.randint(0, 25))
		
		if not random_upper_character_temp in random_upper_characters:
			random_upper_characters.append(random_upper_character_temp)
		
	random_lower_characters = []
	while(len(random_lower_characters) != lower_number):
		random_lower_character_temp = chr(ord("a") + random.randint(0, 25))
		
		if not random_lower_character_temp in random_lower_characters:
			random_lower_characters.append(random_lower_character_temp)
		
	# append
	for i in range(upper_number):
		characters.append(random_upper_characters[i])
		
	for j in range(lower_number):
		characters.append(random_lower_characters[j])
	
	return characters
	
def get_four_special_character_list():
	special_characters = []
	
	special_character_list = ["!", "@", "#", "$", "%", "^", "&", "*"]
	
	# Not duplicated
	while(len(special_characters) != 5):
		special_character_temp = special_character_list[random.randint(0,7)]
		
		if not special_character_temp in special_characters:
			special_characters.append(special_character_temp)
				
	return special_characters

def create_password(*password_source):
	password = []
	
	for j in range(5):
		random_integer = [0, 1, 2]
		
		for i in range(3):
			max_random_index = len(random_integer) - 1
			random_index = random.randint(0,max_random_index)
			random_index_value = random_integer[random_index]
			
			random_integer.remove(random_index_value)
			password.append(password_source[random_index_value][j])
		
	return password
	
def print_password(*password):
	print()
	
	for i in range(len(password)):
		print(password[i],sep="",end="")
	
	print()
		
four_numbers = get_four_number_list()
four_characters = get_four_character_list()
four_special_characters = get_four_special_character_list()
		
password_source = four_numbers, four_characters, four_special_characters
		
password = create_password(*password_source)
		
print_password(*password)

