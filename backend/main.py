"""
FastAPI backend para el Scrabble solver.
Expone el código Python existente (scrabble.py) como una API REST.

Arrancar con:
    uvicorn main:app --reload --port 8000
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import numpy as np
import itertools
import sys
import os

# Asegurarse de que los módulos del juego son accesibles
sys.path.insert(0, os.path.dirname(__file__))

import analize_word as aw
import scrabble_board as sb

# ─────────────────────────────────────────────
# Inicialización del tablero (igual que en scrabble.py)
# ─────────────────────────────────────────────

default_board = ["T", "D", "1", "2", "3", ".."]

hor = [["..","..","..","..","..","..","..","..","..","..","..","..","..","..",".."]]
ver = hor
for i in range(14):
    ver = np.concat([ver, hor], axis=0)

board_base = sb.generate_board()
main_board = np.concat([[ver], [board_base]], axis=0)
board_vacio = np.copy(main_board)

pos_ini = {}
for letter in aw.points.keys():
    pos_ini[letter] = []
    for dir in ["h", "v"]:
        pos_ini[letter].append([[7, 7], dir])

# ─────────────────────────────────────────────
# Diccionarios
# ─────────────────────────────────────────────

def load_dictionary(path):
    words = set()
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            w = line.strip()
            if w:
                words.add(aw.normalize(w))
    return words

dictionary = load_dictionary("spanish_words.txt")
nombres = load_dictionary("nombres_propios_es.txt")

def is_word_valid(word):
    return (aw.normalize(word) in dictionary) or (aw.normalize(word) in nombres)

# ─────────────────────────────────────────────
# Lógica del juego (idéntica a scrabble.py)
# ─────────────────────────────────────────────

played_words = []

def check_board_space(board, position, node):
    dummy_current_before = node.prev
    dummy_current_after = node.next
    mx, my = 1, 1
    move = []

    if position[1] == "v":
        move = [0, 1]
        if dummy_current_before and position[0][1] == 0:
            return False
        if dummy_current_after and position[0][1] == 15:
            return False
        if position[0][1] < node.before or position[0][1] + node.after > 14:
            return False
    if position[1] == "h":
        move = [1, 0]
        if dummy_current_before and position[0][0] == 0:
            return False
        if dummy_current_after and position[0][0] == 15:
            return False
        if position[0][0] < node.before or position[0][0] + node.after > 14:
            return False

    while dummy_current_before:
        if (board[position[0][0] - move[0]*mx, position[0][1] - move[1]*mx] != ".." and
                board[position[0][0] - move[0]*mx, position[0][1] - move[1]*mx] != dummy_current_before.letter):
            return False
        mx += 1
        dummy_current_before = dummy_current_before.prev

    while dummy_current_after:
        if (board[position[0][0] + move[0]*my, position[0][1] + move[1]*my] != ".." and
                board[position[0][0] + move[0]*my, position[0][1] + move[1]*my] != dummy_current_after.letter):
            return False
        my += 1
        dummy_current_after = dummy_current_after.next

    return True


def check_aux_words(board, pos, current, played_words):
    dummy_board = np.copy(board)
    fila = pos[0][0]
    columna = pos[0][1]
    direction = pos[1]
    aux_words = []
    ending_positions = []
    mx, my = 1, 1

    if direction == "h":
        move = [1, 0]; movet = [0, 1]; long_direction = "v"
        if (current.before > fila) or (current.after + fila > 14):
            return [False, []]
    if direction == "v":
        move = [0, 1]; movet = [1, 0]; long_direction = "h"
        if (current.before > columna) or (current.after + columna > 14):
            return [False, []]

    dummy_current = current
    while dummy_current.prev:
        dummy_board[fila - move[0]*mx, columna - move[1]*mx] = dummy_current.prev.letter
        dummy_current = dummy_current.prev
        mx += 1

    dummy_current = current
    while dummy_current.next:
        dummy_board[fila + move[0]*my, columna + move[1]*my] = dummy_current.next.letter
        dummy_current = dummy_current.next
        my += 1

    mx -= 1
    while dummy_board[fila - move[0]*mx, columna - move[1]*mx] not in default_board:
        mx += 1
        if max([abs(fila - move[0]*mx), abs(columna - move[1]*mx)]) == 15 or \
                min([fila - move[0]*mx, columna - move[1]*mx]) == -1:
            break

    long_word = []
    mx -= 1

    while dummy_board[fila - move[0]*mx, columna - move[1]*mx] not in default_board:
        short_word = []
        t = 1
        while dummy_board[fila - move[0]*mx - movet[0]*t, columna - move[1]*mx - movet[1]*t] not in default_board:
            t += 1
        t -= 1
        while dummy_board[fila - move[0]*mx - movet[0]*t, columna - move[1]*mx - movet[1]*t] not in default_board:
            short_word.append(dummy_board[fila - move[0]*mx - movet[0]*t, columna - move[1]*mx - movet[1]*t])
            t -= 1
            if max(fila - move[0]*mx - movet[0]*t, columna - move[1]*mx - movet[1]*t) == 15 or \
                    min(fila - move[0]*mx - movet[0]*t, columna - move[1]*mx - movet[1]*t) == -1:
                break

        short_word = ''.join(short_word)
        if len(short_word) > 1:
            if not is_word_valid(short_word):
                return [False, []]
            elif short_word not in played_words:
                ending_positions.append([[fila - move[0]*mx - movet[0]*(t+1),
                                          columna - move[1]*mx - movet[1]*(t+1)], direction])
                aux_words.append(short_word)

        long_word.append(dummy_board[fila - move[0]*mx, columna - move[1]*mx])
        mx -= 1
        if max(fila - move[0]*mx, columna - move[1]*mx) == 15:
            break

    long_word = ''.join(long_word)
    if not is_word_valid(long_word):
        return [False, []]

    ending_positions.append([[fila - move[0]*(mx+1), columna - move[1]*(mx+1)], long_direction])
    aux_words.append(long_word)
    return True, [ending_positions, aux_words]


def calculate_points(original_board, aux_words):
    words_board = np.copy(original_board[0])
    points_board = np.copy(original_board[1])
    last_letters = aux_words[0]
    words = aux_words[1]
    t = 0
    total_points = 0

    for position, direction in last_letters:
        word_points = 0
        word_mult = 1
        mx = 0
        move = [0, 1] if direction == "h" else [1, 0]
        word_letters = aw.P(words[t])[0]

        for i in range(len(word_letters)):
            row = position[0] - move[0] * i
            col = position[1] - move[1] * i
            words_board[row, col] = word_letters[len(word_letters)-i-1]

        while mx < len(word_letters):
            row = position[0] - move[0] * mx
            col = position[1] - move[1] * mx
            if original_board[0][row, col] == "..":
                letter = words_board[row, col]
                base_points = aw.points.get(letter, 0)
                mult = int(points_board[row, col]) if points_board[row, col].isdigit() else 1
                word_points += base_points * mult
                if points_board[row, col] == "D":
                    word_mult *= 2
                elif points_board[row, col] == "T":
                    word_mult *= 3
                points_board[row, col] = '1'
            mx += 1

        total_points += word_points * word_mult
        t += 1

    return [np.concat([[words_board], [points_board]], axis=0), total_points]


def add_to_pos(board):
    old_pos = {letter: [] for letter in aw.points.keys()}
    for i, fila in enumerate(board[0]):
        for j, letra in enumerate(fila):
            if letra != "..":
                old_pos[letra].append([[i, j], "v"])
                old_pos[letra].append([[i, j], "h"])
    return old_pos


def find_possible_unions(board, word, pos):
    pos_list = []
    max_points = 0
    new_board = board
    new_pos = pos

    if set(pos).intersection(set(aw.P(word)[0])):
        head = aw.build_linked_list(word)
        current = head

        while current:
            if current.letter in pos:
                for position in pos[current.letter]:
                    if check_board_space(board[0], position, current):
                        aux_words_status, aux_words = check_aux_words(board[0], position, current, played_words)
                        if not aux_words_status:
                            break
                        current_word = aux_words[1]
                        if current_word not in played_words:
                            played_words.append(current_word)
                        pos_list.append([current.letter, current.id, position])
                        possible_board, possible_points = calculate_points(board, aux_words)
                        if possible_points > max_points:
                            new_board = possible_board
                            max_points = possible_points
            current = current.next

        new_pos = add_to_pos(new_board)
    else:
        return board, pos, 0

    return new_board, new_pos, max_points


def create_empty_board():
    hor = [["..","..","..","..","..","..","..","..","..","..","..","..","..","..",".."]]
    ver = hor
    for i in range(14):
        ver = np.concatenate([ver, hor], axis=0)
    board_points = sb.generate_board()
    return np.concatenate([[ver], [board_points]], axis=0)


def place_best_word(word):
    board = create_empty_board()
    base_board = sb.generate_board()
    word_letters = aw.P(word)[0]
    word_length = len(word_letters)
    best_board = np.copy(board)
    best_points = 0
    best_pos = {}

    def calc_pts(positions):
        wp, wm = 0, 1
        for idx, (row, col) in enumerate(positions):
            lp = aw.points.get(word_letters[idx], 0)
            cb = base_board[row, col]
            if cb == '3': wp += lp * 3
            elif cb == '2': wp += lp * 2
            elif cb == 'D': wp += lp; wm *= 2
            elif cb == 'T': wp += lp; wm *= 3
            else: wp += lp
        return wp * wm

    for start_col in range(16 - word_length):
        if start_col <= 7 < start_col + word_length:
            dummy = np.copy(board)
            positions = []
            for idx, letter in enumerate(word_letters):
                col = start_col + idx
                dummy[0][7][col] = letter
                dummy[1][7][col] = '1'
                positions.append([7, col])
            pts = calc_pts(positions)
            if pts > best_points:
                best_points = pts
                best_board = np.copy(dummy)
                best_pos = {}
                for idx, letter in enumerate(word_letters):
                    best_pos.setdefault(letter, []).append([positions[idx], "h"])

    for start_row in range(16 - word_length):
        if start_row <= 7 < start_row + word_length:
            dummy = np.copy(board)
            positions = []
            for idx, letter in enumerate(word_letters):
                row = start_row + idx
                dummy[0][row][7] = letter
                dummy[1][row][7] = '1'
                positions.append([row, 7])
            pts = calc_pts(positions)
            if pts > best_points:
                best_points = pts
                best_board = np.copy(dummy)
                best_pos = {}
                for idx, letter in enumerate(word_letters):
                    best_pos.setdefault(letter, []).append([positions[idx], "v"])

    return best_board, best_pos, best_points


def play_words(word_list):
    max_total = 0
    best_board = None
    for perm in itertools.permutations(word_list):
        _played_words = []
        board = np.copy(board_vacio)
        pos = {k: list(v) for k, v in pos_ini.items()}
        total_points = 0
        success = True
        for index, word in enumerate(perm):
            if index == 0:
                board, pos, points = place_best_word(word)
            else:
                board, pos, points = find_possible_unions(board, word, pos)
            if points == 0:
                success = False
                break
            total_points += points
        if success and total_points > max_total:
            max_total = total_points
            best_board = board
    return best_board, max_total

# ─────────────────────────────────────────────
# FastAPI app
# ─────────────────────────────────────────────

app = FastAPI(title="Scrabble Solver API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class WordsRequest(BaseModel):
    words: List[str]


@app.get("/")
def root():
    return {"status": "ok", "message": "Scrabble Solver API"}


@app.get("/empty-board")
def get_empty_board():
    """Devuelve el tablero vacío con los multiplicadores."""
    board = create_empty_board()
    return {
        "letters_board": board[0].tolist(),
        "points_board": board[1].tolist(),
    }


@app.post("/play")
def play(request: WordsRequest):
    """
    Recibe una lista de palabras y devuelve el tablero óptimo y los puntos.
    """
    if not request.words:
        raise HTTPException(status_code=400, detail="La lista de palabras está vacía.")
    if len(request.words) > 8:
        raise HTTPException(status_code=400, detail="Máximo 8 palabras.")

    global played_words
    played_words = []

    best_board, total_points = play_words(request.words)

    if best_board is None:
        raise HTTPException(status_code=422, detail="No se encontró ninguna colocación válida para las palabras dadas.")

    return {
        "letters_board": best_board[0].tolist(),
        "points_board": best_board[1].tolist(),
        "total_points": int(total_points),
    }


if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)