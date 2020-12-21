#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 23 21:03:29 2020

@author: muntasirmeah
"""
import math 

def clean_text(txt):
    """takes a string of text txt as a parameter and returns a list 
       containing the words in txt after it has been “cleaned”
    """
    txt = txt.lower()
    text = ''
    for i in (txt):
        if i in '.,?!;"":':
            text += ''
        else:
            text += i 
    text = text.split()
    return text

def sample_file_write(filename):
    """A function that demonstrates how to write a
       Python dictionary to an easily-readable file.
    """
    d = {'test': 1, 'foo': 42}   # Create a sample dictionary.
    f = open(filename, 'w')      # Open file for writing.
    f.write(str(d))              # Writes the dictionary to the file.
    f.close()                    # Close the file.

def sample_file_read(filename):
    """A function that demonstrates how to read a
       Python dictionary from a file.
    """
    f = open(filename, 'r')    # Open for reading.
    d_str = f.read()           # Read in a string that represents a dict.
    f.close()

    d = dict(eval(d_str))      # Convert the string to a dictionary.

    print("Inside the newly-read dictionary, d, we have:")
    print(d)
    
def stem(s):
    """returns the stem of s
    """
    if s[-1] == 's':
        s = s[:-1]
        s = stem(s)
    if s[-4:] == 'able' or s[-4:] == 'ible':
        if len(s) <= 5:
            s = s 
        else:
            s = s[:-4]
    elif s[-3:] == 'ing' or s[-3:] == 'ion':
        if len(s) <= 4:
            s = s
        elif s[-4] == s[-5]:
            s = s[:-3]
            if len(s) == 5:
                s = s[:-1]
        else:
            s = s[:-3]
    elif s[-3:] == 'est':
        if len(s) <= 4:
            s = s
        elif s[-4] == s[-5]:
            s = s[:-3]
            if len(s) == 5:
                s = s[:-1]
        else:
            s = s[:-3]
    elif s[-2:] == 'er':
        if len(s) <= 4:
            s = s
        elif s[-3] == s[-4]:
            s = s[:-3]
        else:
            s = s[:-2]
    elif s[-1] == 'y':
        if len(s) <= 3:
            s = s
        elif s[-2:] == 'ly':
            if s[-3] == s[-4]:
                s = s[:-2]
            else:
                s = s[:-2]
        else:
            s = s[:-1] + 'i'
    elif s[-1] == 'e': 
        if len(s) <= 3:
            s = s
        else:
            s = s[:-1]
    elif s[-2:] == 'ed':
        if len(s) <= 3:
            s = s
        elif s[-3] == s[-4]:
            s = s[:-3]
        else:
            s = s[:-2]
    elif s[-2:] == 'es':
        if len(s) == 4:
            s = s[:-1]
        elif s[-3] == s[-4]:
            s = s[:-3]
        else:
            s = s[:-2]
    return s

def compare_dictionaries(d1, d2):
    """takes two feature dictionaries d1 and d2 as inputs, and computes 
       and returns their log similarity score
    """
    score = 0
    total = 0
    for i in d1:
        total += d1[i]
    for i in d2:
        if i in d1:
            score += d2[i]*math.log(d1[i]/total)
        else:
            score += d2[i]*math.log(0.5/total)
    return score
    
            
class TextModel:
    """ will serve as a blueprint for objects that model a body 
        of text
    """
    def __init__(self, model_name):
      """ constructs a new TextModel object by accepting a string model_name 
          as a parameter and initializing the following three attributes 
      """
      self.name = model_name
      self.words = {}
      self.word_lengths = {}
      self.stems = {}
      self.sentence_lengths = {}
      self.punctuation = {}
    
    def __repr__(self):
        """Return a string representation of the TextModel."""
        s = 'text model name: ' + self.name + '\n'
        s += '  number of words: ' + str(len(self.words)) + '\n'
        s += '  number of word lengths: ' + str(len(self.word_lengths)) + '\n'
        s += '  number of stems: ' + str(len(self.stems)) + '\n'
        s += '  number of sentence lengths: ' + str(len(self.sentence_lengths)) + '\n'
        s += '  number of punctuation marks: ' + str(len(self.punctuation))
        return s  
    
    def add_string(self, s):
        """adds a string of text s to the model by augmenting the 
           feature dictionaries defined in the constructor
        """
        s1 = s.split()
        wc = 0
        for w in s1:
            if w[-1] not in '.?!':
                wc += 1
            else:
                wc += 1
                if wc not in self.sentence_lengths:
                    self.sentence_lengths[wc] = 1
                    wc = 0
                else:
                    self.sentence_lengths[wc] += 1
                    wc = 0
        
        s2 = s
        pmarks = ''
        for w in s2:
            if w in '.,?!;"":/_-()[]':
                pmarks += w
        for w in pmarks:
            if w not in self.punctuation:
                self.punctuation[w] = 1 
            else:
                self.punctuation[w] += 1
        
        word_list = clean_text(s)      
        for w in word_list:
            if w not in self.words:
                self.words[w] = 1
            else:
                self.words[w] += 1
        for w in range(len(word_list)):
            lengths = len(word_list[w])
            if lengths not in self.word_lengths: 
                self.word_lengths[lengths] = 1
            else:
                self.word_lengths[lengths] += 1
        for w in word_list:
            w = stem(w)
            if w not in self.stems: 
                self.stems[w] = 1
            else:
                self.stems[w] += 1

                
    def add_file(self, filename):
        """ adds all of the text in the file identified by filename to the 
            model
        """
        f = open(filename, 'r', encoding='utf8', errors='ignore')
        text = f.read()
        self.add_string(text)
        f.close()
        
    def save_model(self):
        """ saves the TextModel object self by writing its various feature
            dictionaries to files
        """
        wordsfile = open(self.name + '_' + 'words', 'w')
        wordsfile.write(str(self.words))
        wordsfile.close()
        
        word_lengths_file= open(self.name + '_' + 'word lengths', 'w')
        word_lengths_file.write(str(self.word_lengths))
        word_lengths_file.close()

        stemsfile= open(self.name + '_' + 'stems', 'w')
        stemsfile.write(str(self.stems))
        stemsfile.close()                 
               
        sentence_lengths_file= open(self.name + '_' + 'sentence lengths', 'w')
        sentence_lengths_file.write(str(self.sentence_lengths))
        sentence_lengths_file.close() 
                
        punctuation_file= open(self.name + '_' + 'punctuation', 'w')
        punctuation_file.write(str(self.punctuation))
        punctuation_file.close() 
        
  
    def read_model(self):
        """reads the stored dictionaries for the called TextModel object from
           their files and assigns them to the attributes of the called 
           TextModel
        """
        wordsfile = open(self.name + '_' + 'words', 'r')
        words_str = wordsfile.read()
        wordsfile.close()
        d1 = dict(eval(words_str))
        self.words = d1
        
        word_lengths_file = open(self.name + '_' + 'word lengths', 'r')
        word_lengths_str = word_lengths_file.read()
        word_lengths_file.close()
        d2 = dict(eval(word_lengths_str))        
        self.word_lengths = d2

        stemsfile = open(self.name + '_' + 'stems', 'r')
        stemsfile_str = stemsfile.read()
        stemsfile.close()
        d3 = dict(eval(stemsfile_str))        
        self.stems = d3
        
        sentence_lengths_file = open(self.name + '_' + 'sentence lengths', 'r')
        sentence_lengths_file_str = sentence_lengths_file.read()
        sentence_lengths_file.close()
        d4 = dict(eval(sentence_lengths_file_str))        
        self.sentence_lengths = d4      
        
        punctuation_file = open(self.name + '_' + 'punctuation', 'r')
        punctuation_file_str = punctuation_file.read()
        punctuation_file.close()
        d5 = dict(eval(punctuation_file_str))        
        self.punctuation = d5     

    def similarity_scores(self,other):
        """ computes and returns a list of log similarity scores measuring 
            the similarity of self and other between every feature dictionary
        """         
        word_score = compare_dictionaries(other.words,self.words)
        word_lengths_score = compare_dictionaries(other.word_lengths,self.word_lengths)
        stems_score = compare_dictionaries(other.stems, self.stems)
        sentence_lengths_score = compare_dictionaries(other.sentence_lengths, self.sentence_lengths)
        punctuation_score = compare_dictionaries(other.punctuation, self.punctuation)
        return ([word_score] + [word_lengths_score] + [stems_score] + [sentence_lengths_score] + [punctuation_score]) 
        
    def classify(self, source1, source2):
        """ compares the TextModel self to two other source TextModel objects
            and determines which source is more similar 
        """
        scores1 = self.similarity_scores(source1)
        scores2 = self.similarity_scores(source2)
        scores1rounded = []
        for i in range(len(scores1)):
            y = round(scores1[i], 3)
            scores1rounded += [y]

        scores2rounded = []
        for i in range(len(scores2)):
            z = round(scores2[i], 3)
            scores2rounded += [z]

        print('scores for source 1: ' + str(scores1rounded))
        print('scores for source 2: ' + str(scores2rounded))
        count1 = 0
        count2 = 0
        for i in range(len(scores1)):
            if scores1[i] > scores2[i]:
                count1 += 1 
            elif scores1[i] < scores2[i]: 
                count2 += 1
            else:
                count1 += 0
                count2 += 0
        if count1 > count2:
            print(self.name + ' is more like ' + source1.name)
        else:
            print(self.name + ' is more like ' + source2.name)
        
def test():
    """ test function """
    source1 = TextModel('source1')
    source1.add_string('It is interesting that she is interested.')

    source2 = TextModel('source2')
    source2.add_string('I am very, very excited about this!')

    mystery = TextModel('mystery')
    mystery.add_string('Is he interested? No, but I am.')
    mystery.classify(source1, source2)
    
def run_tests():
    """ test functions for multiple texts """
    source1 = TextModel('the Friends pilot episode')
    source1.add_file('friendsep1.txt')

    source2 = TextModel('the How I Met Your Mother pilot episode')
    source2.add_file('himymep1.txt')

    new1 = TextModel('The second episode of Friends')
    new1.add_file('friendsep2.txt')
    new1.classify(source1, source2)
    
    print()
    
    source1 = TextModel('the Friends pilot episode')
    source1.add_file('friendsep1.txt')

    source2 = TextModel('the How I Met Your Mother pilot episode')
    source2.add_file('himymep1.txt')

    new1 = TextModel('The second episode of How I Met Your Mother')
    new1.add_file('himymep2.txt')
    new1.classify(source1, source2)
    
    print()
    source1 = TextModel('the Friends pilot episode')
    source1.add_file('friendsep1.txt')

    source2 = TextModel('the How I Met Your Mother pilot episode')
    source2.add_file('himymep1.txt')

    new1 = TextModel('The pilot episode of The Office')
    new1.add_file('office.txt')
    new1.classify(source1, source2)
    
    print()
    source1 = TextModel('the Friends pilot episode')
    source1.add_file('friendsep1.txt')

    source2 = TextModel('the How I Met Your Mother pilot episode')
    source2.add_file('himymep1.txt')

    new1 = TextModel('The first episode of season 2 of Saved by the Bell')
    new1.add_file('savedbythebell.txt')
    new1.classify(source1, source2)