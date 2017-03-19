# Database :D
Users = {
    "1":
        {
            "name": "John Liu",
            "id": "1",
            "type": "nurse",
        },
    "2":
        {
            "name": "William Ott",
            "id": "2",
            "type": "nurse",
        },
    "3":
        {
            "name": "Jordan Lin",
            "id": "3",
            "type": "manager",
        },
}

Patients = {
    "1":
        {
            "name": "Andy Ziemmer",
            "id": "1",
            "nurseId": "1",
        },
    "2":
        {
            "name": "Michael Jordan",
            "id": "2",
            "nurseId": "1",
        },
    "3":
        {
            "name": "Kobe Bryant",
            "id": "3",
            "nurseId": "2",
        },
    "4":
        {
            "name": "Nick Kamar",
            "id": "4",
            "nurseId": "2",
        },
    "5":
        {
            "name": "Jack Bledie",
            "id": "5",
            "nurseId": "2",
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


def getPatients(patientId=None, searchName=None, nurseId=None):
    if patientId is not None:
        return Patients[patientId]

    patients = list(Patients.values())

    if searchName is not None:
        patients = [patient for patient in patients
                    if patient["name"].lower().find(searchName.lower()) >= 0]

    if nurseId is not None:
        patients = [patient for patient in patients
                    if patient["nurseId"] == nurseId]

    return patients
