#find who is policeOfficer
graph = {}
graph["you"] = [{'name': "ana" , 'job': "artist"},{'name': "bob" , 'job': "chef"},{'name': "cat" , 'job': "pianist"}]
graph["bob"] = [{'name': "dao", 'job': "dentist"},{'name': "evy", 'job': "model"}]
graph["ana"] = [{'name': "evy", 'job': "model"}]
graph["cat"] = [{'name': "fom", 'job': "policeOffice"},{'name': "gil", 'job': "teacher"}]
graph["dao"] = []
graph["evy"] = []
graph["fom"] = []
graph["gil"] = []


from collections import deque
search_queue = deque()
search_queue += graph["you"]
print(search_queue)



def search(name):
    search_queue = deque()
    search_queue += graph[name]
    searched = []
    
    while search_queue:
        person = search_queue.popleft()
        print('person = ', person)
        if person_is_police(person):
            if not person in searched:
                print (person['name'] + " is a policeOfficer!")
                return True
        else:
            search_queue += graph[person['name']]
            searched.append(person)
    return False

def person_is_police(personDict):
    return personDict['job'] == 'policeOffice'

search("you")