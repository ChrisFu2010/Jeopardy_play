import pandas as pd
import re
import numpy as np


pd.set_option('display.max_colwidth', 1000)
pd.set_option('display.max_columns', 20)
pd.set_option('display.max_rows', 50)

jeopardy_data = pd.read_csv('jeopardy.csv')
# rename each column(delete beginning white space)
jeopardy_data = jeopardy_data.rename(columns={" Air Date": "Air Date", " Round": "Round",
                                              " Category": "Category", " Value": "Value", " Question": "Question", " Answer": "Answer"})

print(jeopardy_data['Air Date'].min())

# print(jeopardy_data.columns)

print(jeopardy_data.head(5))

# define a function that can select questions based on specific key words


def filter_data(data, words):
    # Lowercases all words in the list of words as well as the questions. Returns true is all of the words in the list appear in the question. Using Regular expression to check string
    def filter(question):
        # create a list of True/False value, then use all()
        # using regular expression to search for string
        false_or_true = []
        for word in words:
            false_or_true.append(
                re.search(' '+word.lower()+' ', question.lower()))
        return all(false_or_true)

    # Applies the function to the Question column and returns the rows where the filter function returns True
    return data.loc[data["Question"].apply(filter)]


# define a function that returns categories and their question counts, decending order
def categories_count(data):
    return data.Category.value_counts()


print(categories_count(jeopardy_data))

# define a function that can select a specific category of questions and can randomly return specific number of questions from that category and their values and answers


def questions_from_categories(data, category, number):
    category_questions = data[data['Category'] == category]
    random_num = np.random.randint(len(category_questions.index), size=number)
    return category_questions.iloc[random_num]['Question'] + \
        ' , ' + category_questions.iloc[random_num]['Value'] + \
        ' , ' + category_questions.iloc[random_num]['Answer']


print(questions_from_categories(jeopardy_data, 'LITERATURE', 5))


# ======================================================================
# Some basic analysis of the jeopardy data set

# define a function that returns answers and their question counts, decending order
def most_counted_answer(data):
    return data['Answer'].value_counts()


# prepare data to have a float data structure for the question value
jeopardy_data['float_value'] = jeopardy_data['Value'].apply(
    lambda x: float((x[1:]).replace(',', '')) if x != 'None' else 0)


# average value of questions with a specific keyword
def filtered_word_value(word):
    return filter_data(jeopardy_data, [word])['float_value'].mean()


# average value of all questions
question_average_value = jeopardy_data['float_value'].mean()


print(filtered_word_value('china'))
print(question_average_value)
print(most_counted_answer(jeopardy_data))
