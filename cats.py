"""Typing test implementation"""

from utils import lower, split, remove_punctuation, lines_from_file
from ucb import main, interact, trace
from datetime import datetime


###########
# Phase 1 #
###########


def choose(paragraphs, select, k):
    """Return the Kth paragraph from PARAGRAPHS for which SELECT called on the
    paragraph returns true. If there are fewer than K such paragraphs, return
    the empty string.
    """
    # BEGIN PROBLEM 1
    "*** YOUR CODE HERE ***"
    l=len(paragraphs)
    i=0
    while i<l:
        if select(paragraphs[i]) and not k:return paragraphs[i]
        elif select(paragraphs[i]):k-=1
        i+=1
    return ''
    # END PROBLEM 1


def about(topic):
    """Return a select function that returns whether a paragraph contains one
    of the words in TOPIC.

    >>> about_dogs = about(['dog', 'dogs', 'pup', 'puppy'])
    >>> choose(['Cute Dog!', 'That is a cat.', 'Nice pup!'], about_dogs, 0)
    'Cute Dog!'
    >>> choose(['Cute Dog!', 'That is a cat.', 'Nice pup.'], about_dogs, 1)
    'Nice pup.'
    """
    assert all([lower(x) == x for x in topic]), 'topics should be lowercase.'
    # BEGIN PROBLEM 2
    "*** YOUR CODE HERE ***"
    def select(s):
        s=remove_punctuation(s)
        s=lower(s)
        s=split(s)
        l1=len(s)
        l2=len(topic)
        i=0    
        while i<l1:
            j=0
            while j<l2:
                if s[i]==topic[j]:return True
                j+=1
            i+=1
        return False
    return select
    # END PROBLEM 2


def accuracy(typed, reference):
    """Return the accuracy (percentage of words typed correctly) of TYPED
    when compared to the prefix of REFERENCE that was typed.

    >>> accuracy('Cute Dog!', 'Cute Dog.')
    50.0
    >>> accuracy('A Cute Dog!', 'Cute Dog.')
    0.0
    >>> accuracy('cute Dog.', 'Cute Dog.')
    50.0
    >>> accuracy('Cute Dog. I say!', 'Cute Dog.')
    50.0
    >>> accuracy('Cute', 'Cute Dog.')
    100.0
    >>> accuracy('', 'Cute Dog.')
    0.0
    """
    typed_words = split(typed)
    reference_words = split(reference)
    # BEGIN PROBLEM 3
    "*** YOUR CODE HERE ***"
    total=len(typed_words)
    len2=len(reference_words)
    i=0
    correct=0
    if len2==0 and total==0:return 100.0
    elif len2==0 or total==0:return 0.0
    while i<total and i<len2:
        if typed_words[i]==reference_words[i]:correct+=1
        i+=1
    return (correct/total)*100
    # END PROBLEM 3


def wpm(typed, elapsed):
    """Return the words-per-minute (WPM) of the TYPED string."""
    assert elapsed > 0, 'Elapsed time must be positive'
    # BEGIN PROBLEM 4
    "*** YOUR CODE HERE ***"
    word_len=len(typed)
    total=0
    i=0
    while i<word_len:
        total+=len(typed[i])
        i+=1
    if word_len != total:total+=word_len-1
    return total/(elapsed/12)
    # END PROBLEM 4


def autocorrect(user_word, valid_words, diff_function, limit):
    """Returns the element of VALID_WORDS that has the smallest difference
    from USER_WORD. Instead returns USER_WORD if that difference is greater
    than LIMIT.
    """
    # BEGIN PROBLEM 5
    "*** YOUR CODE HERE ***"
    len_v=len(valid_words)
    i=0
    flag=False
    res=1000000000000000
    while i<len_v:
        if user_word==valid_words[i]:return user_word
        if diff_function(user_word,valid_words[i],limit)<res and diff_function(user_word,valid_words[i],limit)<=limit:
            res=diff_function(user_word,valid_words[i],limit)
            flag=True
            j=i
        i+=1
    if flag:return valid_words[j]
    else:return user_word
    
    # END PROBLEM 5


def shifty_shifts(start, goal, limit):
    """A diff function for autocorrect that determines how many letters
    in START need to be substituted to create GOAL, then adds the difference in
    their lengths.
    """
    # BEGIN PROBLEM 6
    'Remove this line'    
    l1=len(start)
    l2=len(goal)
    cnt=0
    def crychic(start,goal,limit,l1,l2,cnt):
        if l1 and l2 and cnt<=limit:
            if start[0]!=goal[0]:cnt+=1
            return crychic(start[1:],goal[1:],limit,l1-1,l2-1,cnt)
        if cnt>limit:
            cnt=limit+1
            return cnt
        if not l1 or not l2:
            cnt+=abs(l1-l2)
            if cnt>limit:
                cnt=limit+1
                return cnt
            else:return cnt
    return crychic(start,goal,limit,l1,l2,cnt)
    # END PROBLEM 6


"""
def pawssible_patches(start, goal, limit):
    A diff function that computes the edit distance from START to GOAL.
    'Remove this line'
    # BEGIN
    l1=len(start)
    l2=len(start)
    cnt=0
    def mygo(start,goal,limit,l1,l2,cnt):
        if l1==0:return l2
        if l2==0:return l1
        if cnt>limit:
            cnt=limit+1
            return cnt
        if l1 and l2 and cnt<=limit:
            if start[0]==goal[0]:return mygo(start[1:],goal[1:],limit,l1-1,l2-1,cnt)
            else:
                cnt+=1
                add_cnt=1+mygo(start,goal[1:],limit,l1,l2,cnt)
                rmv_cnt=1+mygo(start[1:],goal,limit,l1,l2,cnt)
                sub_cnt=1+mygo(start[1:],goal[1:],limit,l1-1,l2-1,cnt)
                return min(add_cnt,rmv_cnt,sub_cnt)
    return mygo(start,goal,limit,l1,l2,0)
    # END
"""

def pawssible_patches(start, goal, limit):
    m, n = len(start), len(goal)

    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if start[i - 1] == goal[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j],    
                                  dp[i][j - 1],      
                                  dp[i - 1][j - 1]) 

    if dp[m][n] <= limit:
        return dp[m][n]
    else:
        return limit+1  


def final_diff(start, goal, limit):
    """A diff function. If you implement this function, it will be used."""
    assert False, 'Remove this line to use your final_diff function'


###########
# Phase 3 #
###########


def report_progress(typed, prompt, user_id, send):
    """Send a report of your id and progress so far to the multiplayer server."""
    # BEGIN PROBLEM 8
    "*** YOUR CODE HERE ***"
    l1=len(typed)
    l2=len(prompt)
    i=0
    accunum=0
    while l1-i>0 and l2-i>0:
        if typed[i]==prompt[i]:accunum+=1
        if typed[i]!=prompt[i]:break
        i+=1
    progress=accunum/l2
    info={'id':user_id,'progress':progress}
    send(info)
    return progress

    # END PROBLEM 8


def fastest_words_report(times_per_player, words):
    """Return a text description of the fastest words typed by each player."""
    game = time_per_word(times_per_player, words)
    fastest = fastest_words(game)
    report = ''
    for i in range(len(fastest)):
        words = ','.join(fastest[i])
        report += 'Player {} typed these fastest: {}\n'.format(i + 1, words)
    return report


def time_per_word(times_per_player, words):
    """Given timing data, return a game data abstraction, which contains a list
    of words and the amount of time each player took to type each word.

    Arguments:
        times_per_player: A list of lists of timestamps including the time
                          the player started typing, followed by the time
                          the player finished typing each word.
        words: a list of words, in the order they are typed.
    """
    # BEGIN PROBLEM 9
    "*** YOUR CODE HERE ***"
    total_time=[]
    l1=len(times_per_player)
    i=0
    j=0
    while i<l1:
        j=0
        time_a_player=[]
        l2=len(times_per_player[i])
        while j<l2-1:
            time_a_player.append(times_per_player[i][j+1]-times_per_player[i][j])
            j+=1
        total_time.append(time_a_player)
        i+=1
    return game(words,total_time)
    # END PROBLEM 9


def fastest_words(game):
    """Return a list of lists of which words each player typed fastest.

    Arguments:
        game: a game data abstraction as returned by time_per_word.
    Returns:
        a list of lists containing which words each player typed fastest
    """
    player_indices = range(len(all_times(game)))  # contains an *index* for each player
    word_indices = range(len(all_words(game)))    # contains an *index* for each word
    # BEGIN PROBLEM 10
    "*** YOUR CODE HERE ***"
    l_time=range(len(all_times(game)))
    l_word=range(len(all_words(game)))
    ans_mat=[[]for _ in player_indices]
    for i in word_indices:
        j=0
        t=10000000000
        ans=0
        for j in player_indices:
            if time(game,j,i)<t:
                ans=j
                t=time(game,j,i)
            j+=1
        ans_mat[ans].append(word_at(game,i))
        i+=1
    return ans_mat

    # END PROBLEM 10


def game(words, times):
    """A data abstraction containing all words typed and their times."""
    assert all([type(w) == str for w in words]), 'words should be a list of strings'
    assert all([type(t) == list for t in times]), 'times should be a list of lists'
    assert all([isinstance(i, (int, float)) for t in times for i in t]), 'times lists should contain numbers'
    assert all([len(t) == len(words) for t in times]), 'There should be one word per time.'
    return [words, times]


def word_at(game, word_index):
    """A selector function that gets the word with index word_index"""
    assert 0 <= word_index < len(game[0]), "word_index out of range of words"
    return game[0][word_index]


def all_words(game):
    """A selector function for all the words in the game"""
    return game[0]


def all_times(game):
    """A selector function for all typing times for all players"""
    return game[1]


def time(game, player_num, word_index):
    """A selector function for the time it took player_num to type the word at word_index"""
    assert word_index < len(game[0]), "word_index out of range of words"
    assert player_num < len(game[1]), "player_num out of range of players"
    return game[1][player_num][word_index]


def game_string(game):
    """A helper function that takes in a game object and returns a string representation of it"""
    return "game(%s, %s)" % (game[0], game[1])

enable_multiplayer = False  # Change to True when you're ready to race.

##########################
# Command Line Interface #
##########################


def run_typing_test(topics):
    """Measure typing speed and accuracy on the command line."""
    paragraphs = lines_from_file('data/sample_paragraphs.txt')
    select = lambda p: True
    if topics:
        select = about(topics)
    i = 0
    while True:
        reference = choose(paragraphs, select, i)
        if not reference:
            print('No more paragraphs about', topics, 'are available.')
            return
        print('Type the following paragraph and then press enter/return.')
        print('If you only type part of it, you will be scored only on that part.\n')
        print(reference)
        print()

        start = datetime.now()
        typed = input()
        if not typed:
            print('Goodbye.')
            return
        print()

        elapsed = (datetime.now() - start).total_seconds()
        print("Nice work!")
        print('Words per minute:', wpm(typed, elapsed))
        print('Accuracy:        ', accuracy(typed, reference))

        print('\nPress enter/return for the next paragraph or type q to quit.')
        if input().strip() == 'q':
            return
        i += 1


@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions."""
    import argparse
    parser = argparse.ArgumentParser(description="Typing Test")
    parser.add_argument('topic', help="Topic word", nargs='*')
    parser.add_argument('-t', help="Run typing test", action='store_true')

    args = parser.parse_args()
    if args.t:
        run_typing_test(args.topic)