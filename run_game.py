import story_game

class RunGame(object):

    def __init__(self, conn):
        self.all_games = {}
        self.need_partner = []
        self.final_stories = []
        self.conn = conn

    def add_story(self, player1, player2, game):
        self.all_games[player1] = game
        self.all_games[player2] = game

    def in_game(self, from_number):
        """
        Checks to see if a user is currently in a game.

        Returns their game object if they are, false otherwise.
        """
        if from_number in self.all_games:
            return self.all_games[from_number]
        else:
            return False

    def get_last_word(self, game, num_words, from_number):
        """
        Gets the last num_words in game
        """
        return game.last_X_words(num_words, from_number)

    def words_left(self, game, from_number):
        """
        Returns the number of words left in a game.
        """
        return game.words_left(from_number)

    def find_game(self, from_number):
        """
        Finds a game for a user to join
        """
        if from_number in self.all_games or from_number in self.need_partner:
            return (from_number, "Sorry, you can only play one game at a time! Concentrate on the one at hand or reply with !SUBMIT to end the current story!")
        return (from_number, "Reply !FRIEND if you would like to invite some to make a story with you or !RANDOM to get a random partner.")
        

    def invite_friend(self, from_number, friend_number):
        player1 = friend_number
        player2 = from_number
        aStory = story_game.Story(player1, player2, self.conn)
        self.all_games[player1] = aStory
        self.all_games[player2] = aStory
        return (from_number, friend_number, "Please wait while we ask your friend to play with you. If you are tired of waiting, reply with !DONE to start a new game.", "Hello! Your friend " + str(from_number) + " would like to play story game with you. To start, reply with a word to begin your story. Reply with !INFO for more information.")


    def get_partner(self, from_number):    
        if len(self.need_partner) == 0:
            self.need_partner.append(from_number)
            return (from_number, "Please wait while we look for a partner for you to play with.")
        else:
            player1 = from_number
            player2 = self.need_partner.pop()
            aStory = story_game.Story(player1, player2, self.conn)
            self.all_games[player1] = aStory
            self.all_games[player2] = aStory
            return aStory.intialize_game()

    def end_game(self, game):
        """
        Ends the game. Returns the full story.
        """
        del self.all_games[game.player1]
        del self.all_games[game.player2]
        self.final_stories.append(game.get_story(game.player1)[1])
        return game.end_game()

    def too_many_words(self, input_list, from_number):
        """
        Takes a list of words given and returns a message letting the user
        know that there are too many words. Gives a suggestion for what to
        respond with.
        """
        return (from_number, 'Sorry, you input ' + str(len(input_list)) + ' words. We can only accept 1. '\
        'Please reply with one word (we suggest "' + str(input_list[0]) + '") or !INFO for'\
        ' more options.')

    def no_words(self, from_number):
        """
        Returns a message telling the user to respond with a word god dammit.
        """
        return (from_number, "Please respond with a word to continue the story or !INFO for more options.")

    def receive_all_messages(self, from_number, message):        
        # split message/parse it
        input_list = message.split()

        if len(input_list) == 0:
            return self.no_words(from_number)

        first_word = input_list[0]

        # If it is a command (!command)
        if first_word[0] == "!":

            # Check command
            first_word = first_word.lower()
            command = first_word[1:]

            # START
            if command == "start":
                return self.find_game(from_number)

            # INFO
            elif command == "info":
                reply = "Reply with: "
                start = "!START, to start a new game. "
                friend = "!FRIEND, to start a game with a friend. "
                number = "!+15559992345 replacing the last 10 numbers with your friend's phone number, to start a game with that friend. "
                random = "!RANDOM, to start a game with a random partner. "
                done = "!DONE, to stop waiting for a game to start. "
                last  = "!LASTWORDX, to get the last X number of words" \
                        " in the story. "
                story = "!STORY, to get the full story so far. "
                left  = "!WORDSLEFT, to find out how many words are left before the end "
                submit = "!SUBMIT to end the story now."
                final = reply + start + friend + number + random + done + last + story + left + submit
                return (from_number, final)

            # Check if they are in a game
            game = self.in_game(from_number)
            if game != False:

                if len(first_word) >= 10:

                    # LASTWORDX
                    if first_word[1:9] == "lastword":
                        num_words = first_word[9:]
                        if num_words.isdigit():
                            num_words = int(num_words)
                            # Assuming games are capped at max_words words, find out how many words 
                            # have been used
                            words_used = game.max_words - int(game.words_left(from_number)[1])
                            if num_words <= words_used:
                                return game.last_X_words(num_words, from_number)
                            else:
                                return (from_number, "Requesting too many words. There are only "\
                                + str(words_used) + " currently in this game. Please"\
                                " try again or respond with !INFO")
                        else:
                            return (from_number, "Command not recognized. If you are trying to get"\
                            " the last words, please use an integer. (Ex. !LASTWORD13)"\
                            " Please try again or respond with !INFO")

                    # WORDSLEFT
                    elif command == "wordsleft":
                        return game.words_left(from_number)

                # STORY
                elif command == "story":
                    return game.get_story(from_number)

                #elif not game.is_your_turn(from_number) and command == "submit":
                #    return (from_number, "It's not your turn! Wait until your partner replies!")

                # SUBMIT
                elif command == "submit":
                    return self.end_game(game)

                elif command == "done" and game.num_words == 0:
                    player1 = game.player1
                    player2 = game.player2
                    del self.all_games[player1]
                    del self.all_games[player2]
                    return (from_number, "Game erased! Poof! Start another!")

            else:
                if command == "friend":
                    if from_number in self.need_partner:
                        return (from_number, "You are already in the queue for a new game!")
                    return (from_number, "Please reply with your friend's phone number. Phone numbers must be domestic USA numbers and formatted with no spaces beginning with !+1. (Ex. !+12402153687)")

                elif command == "random":
                    if from_number in self.need_partner:
                        return (from_number, "You are already in the queue for a new game!")
                    return self.get_partner(from_number)

                elif command == "done" and from_number in self.need_partner:
                    self.need_partner.remove(from_number)
                    return (from_number, "Game erased! Poof! Start another!")

                if command[0:2] == "+1":
                    if command == from_number:
                        return (from_number, "Sorry, you can't play with yourself.")
                    elif command not in self.all_games and command not in self.need_partner:
                        return self.invite_friend(from_number, command)
                    else:
                        return (from_number, "Sorry! Your friend is already playing a story game with someone else right now. Maybe try a different friend or a stranger!")

                # error: please start a game
                return (from_number, "You are not currently playing a game. To begin a game, reply with"\
                " !START or reply with !INFO")

            # INVALID
            return (from_number, "Command not recognized. Please try again or respond with !INFO")

        # If not a command
        else:
                
            # Figure out if the sender is in a game
            game = self.in_game(from_number)

            # If they are
            if game != False:

                if not game.is_your_turn(from_number):
                    return (from_number, "It's not your turn! Wait until your partner replies!")

                # If invalid word (has a space)
                if len(input_list) > 1:

                    # Send error
                    return self.too_many_words(input_list, from_number)

                # Continue game function
                return_val = game.add_word(first_word)

                if return_val == "Kill me now!":
                    return self.end_game(game)

                return return_val

            # If they aren't
            else:

                # error: please start a game
                return (from_number, "You are not currently playing a game. To begin a game, reply with"\
                " !START or reply with !INFO")



