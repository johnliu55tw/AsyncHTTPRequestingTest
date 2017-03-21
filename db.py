# Database :D
Users = {
    "1":
        {
            "name": "John Liu",
            "id": "1",
            "type": "sales",
        },
    "2":
        {
            "name": "William Ott",
            "id": "2",
            "type": "sales",
        },
    "3":
        {
            "name": "Jordan Lin",
            "id": "3",
            "type": "manager",
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


def getUsers(userId=None, searchName=None, searchType=None):
    if userId is not None:
        return Users[userId]

    users = list(Users.values())

    if searchName is not None:
        users = [user for user in users
                 if user["name"].lower().find(searchName.lower()) >= 0]

    if searchType is not None:
        users = [user for user in users
                 if user["type"].lower().find(searchType.lower()) >= 0]

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
