import numpy as np

points = {
    "a": 1,
    "b": 3,
    "c": 3,
    "ch": 5,
    "d": 2,
    "e": 1,
    "f": 4,
    "g": 2,
    "h": 4,
    "i": 1,
    "j": 8,
    "k": 8,
    "l": 1,
    "ll": 8,
    "m": 3,
    "n": 1,
    "ñ": 8,
    "o": 1,
    "p": 3,
    "q": 5,
    "r": 1,
    "rr": 8,
    "s": 1,
    "t": 1,
    "u": 1,
    "v": 4,
    "w": 8,
    "x": 8,
    "y": 4,
    "z": 10
}



def puntos(s):
    res = 0
    for i in s.replace(" ","").lower():
        res += points[i]
    return res

import unicodedata

def normalize(word):
    word = word.lower()
    word = unicodedata.normalize('NFD', word)
    word = ''.join(
        c for c in word
        if unicodedata.category(c) != 'Mn'
    )
    return word


def P(s):
    e = "Error"
    
    s = normalize(s)
    
    if len(s) == 0:
        return e

    res = 0
    name = []
    i = 0

   
    while i < len(s):
        if  i+1 < len(s) and s[i]+s[i+1] in points :
            name.append(str(s[i]+s[i+1]))
            res += points[s[i]+s[i+1]]
            i += 2
        else:
            if s[i] in points:
                name.append(s[i])
                res += points[s[i]]
                i += 1
            else:
                return e
    return [name, res]

class Node:
    def __init__(self, letter):
        self.letter = letter
        self.id = 0
        self.prev = None
        self.next = None
        self.before = 0
        self.after = 0
        self.value = points[letter]

def build_linked_list(word: str):
    """
    Construye una doubly linked list a partir de un string.
    Devuelve el nodo raíz (head).
    """

    if not word:
        return None

    word = P(word)[0]

    if word[0] == "E":
        return None
    # Crear el primer nodo
    head = Node(word[0])
    m = 0
    head.id = m
    current = head
    # Construir el resto de la lista
    for letter in word[1:]:
        new_node = Node(letter)
        new_node.id = m+1

        current.next = new_node
        new_node.prev = current

        current = new_node
        m+=1

    # Calcular before y after
    # Primero recorremos hacia delante
    length = 0
    temp = head
    while temp:
        length += 1
        temp = temp.next

    index = 0
    temp = head
    while temp:
        temp.before = index
        temp.after = length - index - 1
        temp = temp.next
        index += 1

    return head