import random

no_of_friends = int(input("Enter the number of friends joining (including you):\n"))
if no_of_friends <= 0:
    print("No one is joining for the party")
else:
    print("Enter the name of every friend (including you), each on a new line:")
    names = [input() for i in range(no_of_friends)]
    bill_total = float(input("Enter the total bill value:\n"))
    lucky_feature = input("Do you want to use the \"Who is lucky?\" feature? Write Yes/No:\n")
    if lucky_feature.lower() == "yes":
        lucky_one = random.choice(names)
        print("{} is the lucky one!".format(lucky_one))
        each_pay = bill_total / (no_of_friends - 1)
        friends_dict = dict.fromkeys(names, round(each_pay, 2))
        for key in friends_dict:
            if key == lucky_one:
                friends_dict[key] = 0
        print(friends_dict)
    else:
        print("No one is going to be lucky")
        each_pay = bill_total / no_of_friends
        friends_dict = dict.fromkeys(names, round(each_pay, 2))
        print(friends_dict)
