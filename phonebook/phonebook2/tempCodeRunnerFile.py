 = """
1. Insert new user
2. Insert new user from csv file
3. Delete user
4. Filter by first letter
5. Exit
"""
while True:
    print(MENU)
    choice = input("Enter your choice: ")
    if choice == '1':     # insert user
        first_name = input("Enter user name: ")
        phone = input("Enter phone number: ")
        insert_new(first_name, phone)
    elif choice == '2':   # insert from csv
        csv_file_name = input("Enter csv file name without (.csv): ")
        with open(f"{csv_file_name}.csv", 'r') as file:
            reader = csv.reader(file)
            _ = next(reader) # getting rid of the headers
            for row in reader:
                insert_new_list(row)
    elif choice == '3':   # delete user
        user_2_del = input("Enter user name (Enter if you want to delete by phone): ")
        if user_2_del == '':
            phone_2_del = input("Enter phone number: ")
            delete_user(user_2_del, phone_2_del)
        else:
            phone_2_del = ''
            delete_user(user_2_del, phone_2_del)
    elif choice == '4':   # filter by first letter
        letter = tuple((input("Enter the first letter: ")).upper())
        print(call_function_w_args('filter_by_first_letter', letter))
    elif choice == '5':
        break
    else:
        print("Invalid choice. Please try again.")
