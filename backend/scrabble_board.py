import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


def generate_board():
    """
    Construye y devuelve la matriz 15x15 del tablero Scrabble.
    Codificación:
        T -> triple palabra
        D -> doble palabra
        3 -> triple letra
        2 -> doble letra
        1 -> normal
    """
    N = 15
    board = np.full((N, N), "1")

    triple_word = [
        (0,0),(0,7),(0,14),
        (7,0),(7,14),
        (14,0),(14,7),(14,14)
    ]

    double_word = [
        (1,1),(2,2),(3,3),(4,4),
        (10,10),(11,11),(12,12),(13,13),
        (1,13),(2,12),(3,11),(4,10),
        (10,4),(11,3),(12,2),(13,1),
        (7,7)
    ]

    triple_letter = [
        (1,5),(1,9),
        (5,1),(5,5),(5,9),(5,13),
        (9,1),(9,5),(9,9),(9,13),
        (13,5),(13,9)
    ]

    double_letter = [
        (0,3),(0,11),
        (2,6),(2,8),
        (3,0),(3,7),(3,14),
        (6,2),(6,6),(6,8),(6,12),
        (7,3),(7,11),
        (8,2),(8,6),(8,8),(8,12),
        (11,0),(11,7),(11,14),
        (12,6),(12,8),
        (14,3),(14,11)
    ]

    for i, j in triple_word:
        board[i, j] = "T"

    for i, j in double_word:
        board[i, j] = "D"

    for i, j in triple_letter:
        board[i, j] = "3"

    for i, j in double_letter:
        board[i, j] = "2"

    return board


def plot_board(board, save_path=None):
    """
    Genera la figura matplotlib del tablero.
    Si save_path no es None, guarda la imagen en disco.
    Devuelve el objeto figura.
    """
    N = board.shape[0]
    fig, ax = plt.subplots()

    for i in range(N):
        for j in range(N):
            cell = board[i, j]

            if cell == "T":
                color = "#d73027"
            elif cell == "D":
                color = "#fdae61"
            elif cell == "3":
                color = "#4575b4"
            elif cell == "2":
                color = "#91bfdb"
            else:
                color = "#f7f1d5"

            rect = Rectangle((j, N-1-i), 1, 1,
                             facecolor=color,
                             edgecolor="black")
            ax.add_patch(rect)

    ax.set_xlim(0, N)
    ax.set_ylim(0, N)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_aspect("equal")

    if save_path is not None:
        fig.savefig(save_path, dpi=300, bbox_inches="tight")

    return fig


def create_scrabble_board(save_image=False, image_path="scrabble_board.png"):
    """
    Función de alto nivel:
    - Construye la matriz
    - Genera la figura
    - Opcionalmente guarda la imagen
    Devuelve (board, fig)
    """
    board = generate_board()
    fig = plot_board(board, save_path=image_path if save_image else None)

    return board, fig


def print_board_text(letters_board):
    """
    Imprime en la consola una representación textual del tablero con letras.
    letters_board: matriz 15x15 con letras (str) o ".." para vacío.
    """
    for row in letters_board:
        print(' '.join(cell.upper() if cell != ".." else '.' for cell in row))


def plot_board_with_letters(letters_board, save_path=None):
    """
    Genera la figura matplotlib del tablero con letras colocadas.
    letters_board: matriz 15x15 con letras (str) o ".." para vacío.
    Si save_path no es None, guarda la imagen en disco.
    Devuelve el objeto figura.
    """
    N = letters_board.shape[0]
    fig, ax = plt.subplots()

    # Primero, obtener el tablero base de puntuaciones
    base_board = generate_board()

    for i in range(N):
        for j in range(N):
            cell = base_board[i, j]
            letter = letters_board[i, j]

            # Color basado en el tipo de casilla
            if cell == "T":
                color = "#d73027"  # Rojo para triple palabra
            elif cell == "D":
                color = "#fdae61"  # Naranja para doble palabra
            elif cell == "3":
                color = "#4575b4"  # Azul para triple letra
            elif cell == "2":
                color = "#91bfdb"  # Azul claro para doble letra
            else:
                color = "#f7f1d5"  # Beige para normal

            rect = Rectangle((j, N-1-i), 1, 1,
                             facecolor=color,
                             edgecolor="black")
            ax.add_patch(rect)

            # Si hay una letra, dibujarla en el centro de la casilla
            if letter != "..":
                ax.text(j + 0.5, N-1-i + 0.5, letter.upper(),
                        ha='center', va='center',
                        fontsize=12, fontweight='bold', color='black')

    ax.set_xlim(0, N)
    ax.set_ylim(0, N)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_aspect("equal")

    if save_path is not None:
        fig.savefig(save_path, dpi=300, bbox_inches="tight")

    return fig
