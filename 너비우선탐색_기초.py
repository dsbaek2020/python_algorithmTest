# -*- coding: utf-8 -*-


friends = { }
friends['me'] = ['밥','앨리스','클레오']
friends['밥'] = ['톰','매기']
friends['앨리스'] = ['매기']
friends['톰'] = [ ]
friends['매기'] = [ ]
friends['클레오'] = ['닉스','조니']
friends['닉스'] = [ ]
friends['조니'] = [ ]

checkperson = [ ]

def addperson(key) : 
    for data in friends[key] :
        checkperson.append(data)

person = 'me'
addperson(person)

while True :
    person = checkperson.pop(0)
    if person[-1] == '톰' :
       print('찾았음')
       break
    else :
       addperson(person)
       
print(f'{person}가 군인입니다')

   
    

