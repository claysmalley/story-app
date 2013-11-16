import os
import database_access

class Story(object):

    def __init__(self, player1, player2, conn):
        self.player1 = player1
        self.player2 = player2
        self.turn = player1
        self.story_text = []
        self.num_words = 0
        self.max_words = 10
        self.first_time = True
        self.conn = conn

    def intialize_game(self):
        return (self.turn, "Welcome to Story Game! To start, reply with a word to begin your story. Reply with !INFO for more information.")

    def is_your_turn(self, player):
        return self.turn == player

    
    def last_X_words(self, x, current_number):
        last_X_list = self.story_text[self.num_words - x:]
        last_X_string = ""
        for word in last_X_list:
            last_X_string += word + " "
        output = ""
        for ltr in range(len(last_X_string) - 1):
            output += last_X_string[ltr].lower()
            if last_X_string[ltr - 2 : ltr] == ". " or ltr == 0:
                output = output[:ltr] + output[ltr].upper()
        return (current_number, "The last " + str(x) + " word(s): " + output)


    def words_left(self, current_number):
        return (current_number, str(self.max_words - self.num_words))

    def get_story(self, current_number):
        story = ""
        for word in self.story_text:
            story += word + " "
        output = ""
        for ltr in range(len(story) - 1):
            output += story[ltr].lower()
            if story[ltr - 2 : ltr] == ". " or ltr == 0:
                output = output[:ltr] + output[ltr].upper()
        return (current_number, output)

    def add_word(self, word):
        self.story_text.append(word)
        self.num_words += 1
        if self.num_words == self.max_words:
            return "Kill me now!"
        else:
            if self.turn == self.player1:
                self.turn = self.player2
            else:
                self.turn = self.player1
            if self.first_time == True:
                self.first_time = False
                return (self.turn, 'Your partner has begun the game! The first word is: "' + word + '". ' + self.words_left(self.turn)[1] + ' words left. Reply with your word! ')
            return (self.turn, 'The last word was: "' + word + '". ' + self.words_left(self.turn)[1] + ' words left. Reply with your word! ')

    def end_game(self):
        story = self.get_story(self.turn)[1]
        insertion = self.conn.add_story(story)
        #story_id = insertion.generated_keys[0]
        return (self.player1, self.player2, "Game over! Here is your story:\n" + story + ". Check out stories at https://story-app-api.herokuapp.com/")
        #return (self.player1, self.player2, "Game over! Share your story at http://story-app-api.herokuapp.com/story/" + story_id + ". Here is your story:\n" + story)
