

q1 = ["What is capital of korea?", 1]
q1.append("seoul")
q1.append("beiging")
q1.append("tokyo")
q1.append("london")

q2 = ["What is capital of UK?", 4]
q2.append("seoul")
q2.append("beiging")
q2.append("tokyo")
q2.append("london")

q3 = ["What is capital of China?", 2]
q3.append("seoul")
q3.append("beiging")
q3.append("tokyo")
q3.append("london")


score = 0
gameOver = False
questions = [q1, q2, q3]

appText ={ "end message" : "GG",
            #"end message jp " : "djlsjfdslkjfk"
           "correct message": "Good Cool",
           "Quiz Empty": "모든 문제를 풀었음"}






print(len("hello"))
print("Size of questions {}".format (len(questions)) )

yourName = input("What is your name?")

#Show quiz

print("Size of questions {}".format (len(questions)) )

while gameOver == False:
    if len(questions) == 0:
        print(appText["Quiz Empty"])
        break


    quiz = questions.pop(0)

    #Ask answer
    answer= int(input(quiz[0]) )

    #print("{1}'s input is {0}".format(answer, yourName))



    if answer == quiz[1]:
        print("Good Cool")
        score = score+10
    else:
        gameOver = True
        print(appText["end message"])
        #pass
        #game over

    #if user typed correct answer, next .. other : game over

print("your socre is "+ str(score))

