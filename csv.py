import csv

# Create an empty 'user_data.csv' file
with open('user_data.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Name', 'Password', 'Email'])
