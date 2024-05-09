my_list = ['M:1;S:48:T:31.20:M:1;S:49:T:1.20:M:1;\r\n']

# Extracting the string from the list (assuming there's only one element in the list)
string_to_split = my_list[0]

# Splitting the string by ";"
split_list = string_to_split.split(";")

print(split_list)