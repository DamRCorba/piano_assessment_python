#################################################################################################################################################################
# @file merge.py
# @fileoverview this script merge to csv fileA.csv and fileB.csv in a single and verifies the keys with Piano systems sandbox
#
# @author Ing. Damian Corbalan
#################################################################################################################################################################

import requests
import csv

aid = "o1sRRZSLlw"
token = "zziNT81wShznajW2BD5eLA4VCkmNJ88Guye7Sw4D"

# readCSV
# reads a csv file
# params: 
#   - filename String - Name of the csv file
# returns: dictionary list
def readCSV(filename):
    csv_response = []
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            csv_response.append(row)
    return csv_response

# writeCSV
# Writes a csv file
# params: 
#   - filename {string} - Name of the csv file
#   - fieldnames {string[]} - List of key values
#   - Objlist {object[]} - List of objects
# returns: string
def writeCSV(filename, fieldnames, Objlist):
    with open(filename, 'w') as csvfile:
        out = csv.DictWriter(csvfile, fieldnames=fieldnames)
        out.writeheader()
        for user in Objlist:
            out.writerow({'user_id': user['user_id'], 'email': user['email'], 'first_name': user['first_name'], 'last_name': user['last_name']})
    return "File created"

# getPianoUserList
# fetchs list of users in Piano
# params: 
#   - a_id {string} - Pioano aid
#   - api_token {string} - Piano api_token
# returns: dictionary list
def getPianoUserList(a_id, api_token):
    response = requests.get("https://sandbox.piano.io/api/v3/publisher/user/list?aid="+a_id+"&api_token="+api_token)
    response = response.json()
    return response["users"]

# merge
# merge the content of the two csv files with the user data in piano and writes the result in a csv file.
def merge():
    mergedDict = []
    fileA = readCSV('filea.csv')
    fileB = readCSV('fileb.csv')
    pianoUsers = getPianoUserList(aid,token)
    for el in fileA:
        el2 = next((user for user in fileB if user["user_id"] == el["user_id"]), None)
        userPiano = next((user for user in pianoUsers if user["email"] == el["email"]), None)

        uid = el["user_id"]
        if userPiano != None:
            uid = userPiano["uid"]

        mergedDict.append({
            "user_id": uid,
            "email": el['email'],
            "first_name": el2['first_name'],
            "last_name": el2['last_name']
            })  


    return writeCSV('output.csv', ['user_id', 'email','first_name', 'last_name'], mergedDict)
    


# Execution
merged = merge()
print(merged)