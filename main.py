import pandas as pd # type: ignore
import random
from colorama import init, Fore, Back, Style


#print(dataset)
class User:
    def __init__(self, username):
        self.username = username
        self.score = 0
        self.word = "ocean"
        self.attempts = 0

class Wordle:
    def __init__(self, dataset, user):
        self.dataset = dataset
        self.user = user
        self.random_word = self.select_random_word()
        self.letters_left = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

    def select_random_word(self):
        word = "ocean"
        #random_word = "ocean"
        while word == "ocean":
            word = random.choice(self.dataset['5_word'].tolist())
        #letters_left = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        return word


    def play(self):
        
        guessed = False
        game_attempts = 6
        #print(random_word)
        while not guessed and game_attempts > 0:
            print(Fore.WHITE + "\nType in your guess, attempts remaining:" + str(game_attempts))
            if game_attempts != 6:
                print("Unused letters: " + ''.join(self.letters_left))

            guess = input().lower()
            

            if len(guess) == 5 and guess.isalpha():
                game_attempts -= 1
                correct_pos = 0
                temp = [""] * 5
                random_word_list = list(self.random_word)
                guess_list = list(guess)
                #check for correct letter, in the correct position
                for i in range(5):
                    if guess[i] == self.random_word[i]:
                        temp[i] = Fore.GREEN + guess[i]
                        random_word_list[i] = None
                        #guess_list[i] = None
                        correct_pos += 1
                        if guess[i] in self.letters_left:
                                self.letters_left.remove(guess[i])

                for i in range(5):
                    #check for correct letter, in the wrong position
                    if temp[i] == "":  
                        if guess[i] in random_word_list:
                            temp[i] = Fore.YELLOW + guess[i]  
                            random_word_list[random_word_list.index(guess[i])] = None 
                            if guess[i] in self.letters_left:
                                self.letters_left.remove(guess[i]) 
                        else:
                            temp[i] = Fore.WHITE + guess[i]  
                            
                            if guess[i] in self.letters_left:
                                self.letters_left.remove(guess[i])
                
                print("Guess: " + "".join(temp))
                
                # Check if all letters are correct
                if correct_pos == 5:
                    print(Fore.GREEN + "Congratulations! You've guessed the word!")
                    guessed = True
                    return 1
        else:
            print("Invalid input! Please enter a 5-letter word containing only letters.")
        

        if not guessed:
            print(Fore.RED + "You ran out of attempts. The correct word was: " + Fore.GREEN + self.random_word)
        return 1 if guessed else 0



def main():
    dataset = pd.read_csv('data.csv')
    loopOn = True
    print("Enter your name to track your score")
    username = input().lower()

    if username not in dataset['users'].values:
        #print("h")
        new_row = {'users': username, 'score': int(0), '5_word': "ocean", 'attempts': int(0)}
        pd_new_row = pd.DataFrame([new_row])
        dataset = pd.concat([dataset,pd_new_row], ignore_index = True)
        dataset.to_csv('data.csv', index = False)


    user = User(username)

    while loopOn:
        print(Fore.WHITE + "What would you like to do? p: play game, s: check score, q: quit")
        action = input().lower()
        while(action != 's' and action !='p' and action !='q'):
            print("Invalid input: Please enter p, s, or q")
            action = input().lower()
        if(action == 'q'):
            loopOn = False
        if (action == 's'):
            user_row = dataset[dataset['users'] == username]
            user_score = user_row['score'].values[0]
            user_attempts = user_row['attempts'].values[0]
            print("you have gotten " + str(int(user_score)) + " correct out of " + str(int(user_attempts)) + " attempts")
        if(action == 'p'):
            old_score = user_row['score'].values[0]
            old_attempts = user_row['attempts'].values[0]
            wordle = Wordle(dataset, user)
            score_adjustment = wordle.play()
            #print(score_adjustment)
            new_score = score_adjustment + old_score
            old_attempts += 1
            dataset.loc[dataset['users'] == user.username, 'score'] = new_score
            dataset.loc[dataset['users'] == user.username, 'attempts'] = old_attempts
            dataset.to_csv('data.csv', index = False)


if __name__ == "__main__":
    main()


