from tkinter import *
from random import choice
from random import shuffle
import os
import sys

py = sys.executable


file = open('score.txt','w')
root = Tk()
root.title('IP Enigma')
root.geometry("900x900")
root.configure(background='#CBD18F')
#define a score variable
global score
score = 0

global no_of_questions
no_of_questions = 0

# defining a lives variable

global lives 
lives = 5

# defining a variable to keep count of pick another word pressed
global paw
paw = 0 

#question label
my_label = Label(root, text="", font=("Arial", 23), bg='#CBD18F',wraplength= 300)
my_label.pack(pady=20)

#scoring label
label_score= Label(root, text="", font=("Arial", 48), bg='#CBD18F')
label_score.pack()

# lives label

label_lives = Label(root, text="", font=("Arial", 48), bg='#CBD18F')
label_lives.pack()

def end_screen(): 
    py = sys.executable
    os.system('%s %s' % (py, 'ending.py'))



# main functions that generates a random question
def shuffler():
    global no_of_questions
    no_of_questions +=1
    #setting all the parameters to default
    hint_label.config(text='')
    global hint_count
    hint_count = 0
    entry_answer.delete(0, END)
    answer_label.config(text='', bg='#CBD18F')
    
    #defining the list of IP words

    racing_questions = [
    "What is the highest class of open-wheel car racing in the United States?",
    "In Formula 1 racing, what does DRS stand for?",
    "Which circuit hosts the famous '24 Hours of Le Mans' endurance race?",
    "Who holds the record for the most wins in NASCAR Cup Series history?",
    "Which country is known for the Isle of Man TT, a famous motorcycle racing event?",
    "What does the abbreviation 'WRC' stand for in the context of motorsport?",
    "Who is known as the 'Flying Finn' and is a legendary Formula 1 driver?",
    "Which type of racing features cars racing on oval tracks, often turning left?",
    "What is the term for the act of one racing driver allowing another to pass them during a race?",
    "In horse racing, what is the maximum number of horses allowed in the Kentucky Derby?",
    "What is the name of the most famous steeplechase horse race held at Aintree Racecourse in England?",
    "Which racing series is known for its iconic 'Black Beast' car and races on dirt tracks?",
    "Which horse won the Triple Crown in 2018, ending a 37-year drought?",
    "In drag racing, what do the letters 'NHRA' stand for?",
    "What is the total distance covered in the Tour de France, the most famous cycling race?",
    "In Formula 1, which team is known for its 'Prancing Horse' logo?",
    "What racing event takes place in Monaco and is often referred to as the 'Jewel in the Crown'?",
    "Who was the first woman to compete in an Indianapolis 500 race?",
    "Which horse racing event is sometimes called 'The Run for the Roses'?",
    "What is the term for a horse race run over a distance of 1 mile and 4 furlongs?",
    "What is the longest distance race in Formula 1, lasting for 24 hours?",
    "Which circuit is known for its famous Eau Rouge corner and hosts Formula 1 races?",
    "In motorcycle racing, what does 'MotoGP' stand for?",
    "Which racing event is also known as 'The Great American Race'?",
    "Who is the most successful female driver in the history of Formula 1?",
    "In the world of drag racing, what does 'Christmas Tree' refer to?",
    "What is the highest class of road racing for motorcycles?",
    "Which racing driver holds the record for the most Formula 1 World Championships?",
    "What is the term for the act of a horse being disqualified from a race for an infraction?",
    "In horse racing, what is the term for a race on a straight course without obstacles?",
    ]
    
    racing_answers = [
    "IndyCar",
    "Drag Reduction System",
    "Circuit de la Sarthe",
    "Richard Petty",
    "Isle of Man",
    "World Rally Championship",
    "Kimi Räikkönen",
    "Stock Car Racing",
    "Overtaking or Letting By",
    "20",
    "The Grand National",
    "Sprint Car Racing",
    "Justify",
    "National Hot Rod Association",
    "Approximately 3,500 kilometers (2,200 miles)",
    "Ferrari",
    "Monaco Grand Prix",
    "Janet Guthrie",
    "Kentucky Derby",
    "The Derby (Epsom Derby)",
    "Le Mans 24 Hours",
    "Circuit de Spa-Francorchamps",
    "Motorcycle Grand Prix",
    "Daytona 500",
    "Lella Lombardi",
    "The starting lights system",
    "MotoGP",
    "Lewis Hamilton",
    "Disqualification or DQ",
    "Flat racing",
    ]
    global word    # using global to access it across the program
    word = choice(racing_questions) 
    index = racing_questions.index(word)
    global ans
    ans = racing_answers[index]


    # # creating shuffled word outta the random selected word
    # break_apart_word = list(word)
    # shuffle(break_apart_word)
     
    
    # # shuffle the letters stored in the list
    # global shuffled_word
    # shuffled_word = ''
    # for letter in break_apart_word:
    #     shuffled_word += letter

    # # #putting on screen
    my_label.config(text=word)

    #quiting game or relaunching the landing page
    if int(score) > 5:
        file.write(str(score))
        file.close()
        os.system('%s %s' % (py, 'main_copy.py'))
        root.destroy()
        root.quit()
    elif int(lives) <=0:
        file.write(str(score))
        file.close()
        os.system('%s %s' % (py, 'main_copy.py'))
        root.destroy()
        root.quit()
    elif int(no_of_questions)>=10:
        file.write(str(score))
        # os.system('%s %s' % (py, 'main_copy.py'))
        root.destroy()
        os.system('%s %s' % (py, 'main_copy.py'))
        root.quit()
        



# fun to check the answer when button presed and increase score by 1
def answer():
    global score
    if ans.lower() == entry_answer.get().lower():
        answer_label.config(text="Correct answer!", bg='#CBD18F', fg='#3A6B35')
        score+=1
        label_score.config(text = score)
    else:
        answer_label.config(text="Wrong answer, please try again.", bg='#CBD18F', fg='#3A6B35')
        label_score.config(text = score)

global hint_count
hint_count = 0



# func that will give hint and remove live by .25
def hint():
    global hint_count
    global lives
    word_length = len(ans)
    if hint_count < word_length:
        hint_label.config(text=f'{hint_label["text"]} {ans[hint_count]}', bg='#CBD18F')
        hint_count += 1
        lives -=.25
        label_lives.config(text = lives )

# basic GUI
entry_answer = Entry(root, font=("Arial", 24))
entry_answer.pack(pady=20)
button_frame = Frame(root, bg='#CBD18F')
button_frame.pack(pady=20)

answer_button = Button(button_frame, text="Answer", command=answer, bg='#E3B448', width=8, font=10)
answer_button.grid(row=0, column=0, padx=10)
change_button = Button(button_frame, text="Pick Another Word", command=shuffler, bg='#E3B448', width=15, font=10)
change_button.grid(row=0, column=1, padx=10)
hint_button = Button(button_frame, text="Hint", command=lambda: hint(), bg='#E3B448', width=5, font=10)
hint_button.grid(row=0, column=2, padx=10)

answer_label = Label(root, text='', font=("Arial", 22))
answer_label.pack(pady=20)
hint_label = Label(root, text='', font=("Arial", 22), bg='#CBD18F')
hint_label.pack(pady=10)

shuffler()
root.mainloop()