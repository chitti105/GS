#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 11:18:25 2019

@author: nineleaps
"""

#importing libraries
import pandas as pd
import re
import random
from mydict import my_dictionary
import options
#just deleted this line...
import check
import valassign
from newcsv import create_csv
#this extra line craved to be added

class quiz(options.option_generator,check.check_condition,valassign.variable):
    
    
    def __init__(self):
        
        #List to store variables
        self.var=[]
        #List to store expressions which will give result
        
        self.cond=[]
        self.rows=[]
    '''
    Reading the Variable.csv file to extract required variables excluding 
    remove null items
    '''
    def get_input(self):
        #Reading the questions.csv file using pandas
        self.cat = pd.read_csv('Categories.csv')
        self.exp = pd.read_csv('Expression.csv')
        self.exp.fillna("None",inplace=True)
        
        print("Enter required number of questions for each category")
        for i in range(self.cat.shape[0]):
            print(self.cat['Category'][i])
            self.cat['No. Of Questions'][i]= int(input("No. Of Questions: "))
            
        self.read_file()
    
    def read_file(self):
        for i in range(self.cat.shape[0]):
            if self.cat['No. Of Questions'][i]>0:
                self.file_name = 'Questions/'+ self.cat['Category'][i]+'.csv'
                print(self.file_name)
                self.number_of_questions = self.cat['No. Of Questions'][i]
                self.ques = pd.read_csv(self.file_name)
               # self.ques_index = random.sample(range(self.ques.shape[0]),int(self.number_of_questions))
                self.ques_index=[] 
                for n in range(int(self.number_of_questions)):
                    self.ques_index.append(random.randint(0,self.ques.shape[0]-1))
                print(self.ques_index)
                self.seperate_variables()
            
    
    
    
    def seperate_variables(self):
        
        
        for j in self.ques_index:
            self.exp_index = self.ques['Index'][j]
            print(self.exp_index)
            self.var = my_dictionary()
            self.sp=re.split("[,.]",self.exp.values[self.exp_index][-1])
            self.expr = self.sp[0]
            self.cond=(self.sp[1:])

            while True:    
                for k in range(self.exp.shape[1]-1):
                    if self.exp.values[self.exp_index][k]!="None":
                        self.type_split = re.split("[,.]",self.exp.values[self.exp_index][k])
                        print(self.type_split)
                        self.var.add(self.type_split[0],self.type_value(int(self.type_split[1])))
                       
                if self.condition(self.cond,self.var):
                    break  
        
            self.question_generate(j)
        
                        
    
            
    def question_generate(self,j):
        '''    
        Iterating throught the Questions csv file to replace the random numbers 
        in the question adn calculate the result
        '''
        
        
        self.sub_row=[]  
        self.question=self.ques['Question'][j]
        for k,v in self.var.items():
                
                
                
            #Replacing the numbers in the question
            print(k,v)
            
            exec("%s=%s" % (k,v))
            self.question=((re.sub("#{0}".format(k),str(v),self.question)))
        print(self.question)
        self.sub_row.append(self.question)
        
        self.correct=(float("{0:.2f}".format(eval(self.expr))))
        self.sub_row.append(self.correct)
        self.generate_options(self.sub_row,self.correct)
        self.rows.append(self.sub_row)
        
            
        #print(a)
            
        '''    
                #Assining values to the variables using exec
                for k,v in self.var[i].items():
                    exec("%s=%s" % (k,v))
                
                #Calculating result using eval i.e evaluating string expression    
                self.df1.Correct[i]=float("{0:.2f}".format(eval(self.exp[i])))
                
                #Generating Options
                
                self.generate(self.df1,i)
        '''  
                
 #   def get_file(self):
  #      return self.df1
    
    
q = quiz()
q.get_input()
create_csv(q.rows)
