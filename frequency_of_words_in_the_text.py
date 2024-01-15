"""
Vytvořil: Bc. Vít Švestka, UČO: 513122, jako závěrečný úkol do předmětu: ISKM55, Nástroje a metody datové analytiky.
Program vytváří slovníky z textových souborů jako .txt, které je pak možné exportovat jako soubor .csv.
Výsledný soubor csv. má tři sloupce. V prvním je pořadí slova, ve druhém slovo samotné a v posledním počet jeho výskytů.
Čištění textu od nealfanumerických znaků je prováděno pomocí regulárního výrazu. Komunikační část programu je v češtině,
ale s oddělenou textovou částí tak, aby vše bylo na jednom místě a bylo tak jednodušší jej například převést do jiných
jazyků.
Jednotlivé funkce jsou zdokumentovány v angličtině, aby programová část nebyla mix.
"""


import csv
import re
from typing import Dict


def prog_texts(key: str):
    dic_prog_texts = {
        's_m': '##########################################################################\n#                          '
               ' Vítejte v programu                           #\n#                         FREKVENCE SLOV V TEXTU      '
               '                   #\n##########################################################################\nV pro'
               'gramu lze vytvářet nebo tisknout slovnky, které lze buď nechat vypsat\nna obrazovce, nebo výsledky expo'
               'rtovat v .csv souboru pro budoucí použití.\n',
        'm_m': ['\nVítej v menu!\nTvé možnosti:\n',
                              'Vypiš neseřazený slovník slov s jejich výskyty ................. Zadej "1"',
                              'Vypiš seřazený slovník slov seřazený podle nejvyššího výskytu .. Zadej "2"',
                              'U volby 2, lze zadat počet záznamů, které chceme zobrazit.',
                              '',
                              'Pro ukončení programu ....................................... Zadej "exit"',
                              '\nZadej svoji volbu: ',
                              'Soubor který chceš použít, !! VLOŽ DO SLOŽKY S PROGRAMEM !!\n'
                              'a zadej jeho název (i s příponou): '],
        'err': ['Zadal jsi neplatnou volbu, zdej znovu!', '\n                        !!! SOUBOR  NENALEZEN !!!\nZkontol'
                                                          'uj název souboru, nebo zda jsi soubor přesunul do složky pro'
                                                          'gramu,\nnebo zda jsi zadal správnou cestu.\n'],
        'm_f_w': ['Zadej, kolik chceš vypsat záznamů: ', ''],
        'end': ['\nChcete znovu zadávat?\nZadáte-li "yes" program se spustí znovu\nklávesou "enter" program ukončí'
                'te: ', 'Program ukončen.'],
        'print_f_d': ['slovo', 'má počet výskytů'],
        'exp': ['\nChces tabulku uložit do souboru .csv? (y/n): ', 'Zadej název souboru (bez přípony .csv): ', 'pořadí',
                'slovo', 'výskyt', 'Soubor byl vytvořen.']}
    return dic_prog_texts[key]


def print_frequency_dict(dic):
    """
    A function that prints the values stored in a dictionary.
    """
    cnt = 1
    for item in dic:
        print(f'{str(cnt).ljust(2)}) {prog_texts("print_f_d")[0]}   {item.ljust(12)} {prog_texts("print_f_d")[1]}: '
              f'{dic[item]}')
        cnt += 1


def word_frequencies(text: str, ch) -> Dict[str, int]:
    """
    Returns a dictionary containing the number of occurrences of each word in the text.
    Ignores case these are reduced using the text.lover() function. The first if in the for loop, is also unnecessary
    here because it was alredy removed in the cleaning_text function. However, it is an example how to remove
    non-alphanumerical character without regex.
    """
    dic = {}
    text = text.lower()
    slc = text.split()
    print(slc)
    for word in slc:
        if word[-1] in '.,?!’":);':
            word = word[:(len(word) - 1)]
        if word not in dic:
            dic[word] = 0
        if word in dic:
            dic[word] += 1
    if ch == '2':
        return dic
    else:
        print_frequency_dict(dic)
        exp_frequency_dict(dic)


def exp_frequency_dict(dic):
    """
    A function that exports the incoming dictionary to a .csv file.
    """
    ch = str(input(prog_texts("exp")[0]))
    if ch == 'y' or ch == 'Y':
        with open(f'{input(prog_texts("exp")[1])}.csv', mode='w') as csv_f:  # ahoj
            writer = csv.writer(csv_f)
            cnt = 1
            writer.writerow([prog_texts("exp")[2], prog_texts("exp")[3], prog_texts("exp")[4]])
            for key, value in dic.items():
                writer.writerow([cnt, key, value])
                cnt += 1
        print(prog_texts("exp")[5])
        end_prog()
    elif ch == 'n' or ch == 'N':
        end_prog()
    else:
        print(prog_texts("err")[0])
        exp_frequency_dict(dic)


def most_frequent_words(text: str, ch: str):
    """
    A function that prints "n" most frequent words from the incoming text. Is used to find and sort the most frequent
    words via advanced lambda expression. The function calls the print and export functions and sends them the sorted
    dictionary.
    """
    n = int(input(prog_texts('m_f_w')[0]))
    dic = {}
    cnt = 1
    for key, values in sorted(word_frequencies(text, ch).items(), key=lambda kv: kv[1], reverse=True):
        if cnt <= n:
            dic[key] = values
            cnt += 1
        else:
            break
    print_frequency_dict(dic)
    exp_frequency_dict(dic)


def cleaning_text(text):
    """
    A function that removes non-alphanumeric characters from the text and returns the cleaned text.
    """
    cleaned_text = re.sub(r'[^\w\s]', '', text)
    return cleaned_text


def start_program():
    """
    An initialization function that calls a function to open a text file for parsing.
    """
    print(f'{prog_texts("s_m")}')
    open_file()


def open_file():
    """
    Functions to open a working text file. The wrong appearance of the file name is handled with FileNotFoundError.
    The function calls the function to clean the text from punctuation and sends it to the menu function.
    """
    try:
        with open(f"{str(input(prog_texts('m_m')[7]))}", 'r') as input_file:
            text = input_file.read()
        cleaned_text = cleaning_text(text)
        start_menu(cleaned_text)
    except FileNotFoundError:
        print(prog_texts('err')[1])
        open_file()


def start_menu(text):
    """
    A menu function that splits how text will be handled. Sends already cleaned text to create a dictionary function,
    or to the sort function.
    """
    print(f'{prog_texts("m_m")[0]}\n{prog_texts("m_m")[1]}\n{prog_texts("m_m")[2]}\n'
          f'{prog_texts("m_m")[3]}\n{prog_texts("m_m")[4]}\n{prog_texts("m_m")[5]}')
    ch = input(f'{prog_texts("m_m")[6]}')
    if ch == '1':
        word_frequencies(text, ch)
    elif ch == '2':
        most_frequent_words(text, ch)
    elif ch == 'exit':
        end_prog()
    else:
        print(f'{prog_texts("err")[0]}\n')


def end_prog():
    """
    An exit function that terminates or restarts the program when it calls the open_file function.
    """
    ch = str(input(f'{prog_texts("end")[0]}'))
    if ch == 'yes' or ch == 'YES':
        open_file()
    else:
        print(f'{prog_texts("end")[1]}')


start_program()

