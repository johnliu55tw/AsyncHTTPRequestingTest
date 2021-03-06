# Database :D
Users = {
    "1":
        {
            "name": "John Liu",
            "id": "1",
            "role": "sales",
        },
    "2":
        {
            "name": "Bruce Lee",
            "id": "2",
            "role": "sales",
        },
    "3":
        {
            "name": "Chuck Norris",
            "id": "3",
            "role": "manager",
        },
}

Customers = {
    "1":
        {
            "name": "Andy Ziemmer",
            "id": "1",
            "salesId": "1",
        },
    "2":
        {
            "name": "Michael Jordan",
            "id": "2",
            "salesId": "1",
        },
    "3":
        {
            "name": "Kobe Bryant",
            "id": "3",
            "salesId": "2",
        },
    "4":
        {
            "name": "Nick Kamar",
            "id": "4",
            "salesId": "2",
        },
    "5":
        {
            "name": "Jack Bledie",
            "id": "5",
            "salesId": "2",
        },
}


def getUsers(userId=None, searchName=None, searchRole=None):
    if userId is not None:
        return Users[userId]

    users = list(Users.values())

    if searchName is not None:
        users = [user for user in users
                 if user["name"].lower().find(searchName.lower()) >= 0]

    if searchRole is not None:
        users = [user for user in users
                 if user["role"].lower().find(searchRole.lower()) >= 0]

    return users


def getCustomers(customerId=None, searchName=None, salesId=None):
    if customerId is not None:
        return Customers[customerId]

    customers = list(Customers.values())

    if searchName is not None:
        customers = [customer for customer in customers
                     if customer["name"].lower().find(searchName.lower()) >= 0]

    if salesId is not None:
        customers = [customer for customer in customers
                     if customer["salesId"] == salesId]

    return customers
