# Define an empty array to store the class parts and values
t = []

# Open the tokens.txt file for reading
with open('tokens.txt', 'r') as file:
    # Iterate through each line in the file
    for line in file:
        # Split each line into parts using a comma as the separator
        parts = line.strip().split(', ')
        if len(parts) >= 3:  # Make sure there are at least three parts
            # Remove the opening square bracket "[" from the first part
            class_part = parts[0].lstrip('[')
            # Get the second and third parts as value_part and line
            value_part = parts[1]
            line_part = parts[2]
            # Append the class part, value part, and line to the array
            t.append({'cp': class_part, 'vp': value_part, 'line': line_part})

# Access the 'vp' (value part) of the first item in the array
first_item_vp = t[0]['vp']
print("Value part of the first item:", first_item_vp)

# Access the 'vp' (value part) of the second item in the array
second_item_vp = t[1]['vp']
print("Value part of the second item:", second_item_vp)

# Access the 'vp' (value part) of any specific item by its index
specific_item_vp = t[2]['cp']  # Replace 3 with the desired index
print("Value part of the specified item:", specific_item_vp)
