import flet as ft

def main(page: ft.Page):
    page.title = "Jogo da Velha"
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 400
    page.window_height = 500
    
    # Variáveis do jogo
    current_player = "X"
    board = [["", "", ""], ["", "", ""], ["", "", ""]]
    scores = {"X": 0, "O": 0}
    game_over = False
    
    # Elementos da interface
    title = ft.Text("Jogo da Velha", size=30, weight="bold")
    player_turn = ft.Text(f"Vez do jogador: {current_player}", size=20)
    score_display = ft.Text(f"Placar: X - {scores['X']} | O - {scores['O']}", size=16)
    restart_button = ft.ElevatedButton("Reiniciar Jogo", on_click=lambda e: reset_game())
    
    # Criar o tabuleiro
    board_ui = ft.Column(controls=[], spacing=5)
    
    def create_board():
        board_ui.controls.clear()
        for row in range(3):
            row_controls = []
            for col in range(3):
                cell = ft.Container(
                    content=ft.Text(
                        board[row][col], 
                        size=40, 
                        weight="bold",
                        text_align="center"
                    ),
                    width=80,
                    height=80,
                    alignment=ft.alignment.center,
                    bgcolor=ft.Colors.BLUE_100,
                    border_radius=5,
                    on_click=lambda e, r=row, c=col: make_move(r, c),
                )
                row_controls.append(cell)
            board_ui.controls.append(ft.Row(controls=row_controls, spacing=5))
        page.update()
    
    def make_move(row, col):
        nonlocal current_player, game_over
        
        if board[row][col] == "" and not game_over:
            board[row][col] = current_player
            create_board()
            
            if check_winner(current_player):
                scores[current_player] += 1
                score_display.value = f"Placar: X - {scores['X']} | O - {scores['O']}"
                player_turn.value = f"Jogador {current_player} venceu!"
                game_over = True
            elif is_board_full():
                player_turn.value = "Empate!"
                game_over = True
            else:
                current_player = "O" if current_player == "X" else "X"
                player_turn.value = f"Vez do jogador: {current_player}"
            
            page.update()
    
    def check_winner(player):
        # Verificar linhas
        for row in board:
            if all(cell == player for cell in row):
                return True
        
        # Verificar colunas
        for col in range(3):
            if all(board[row][col] == player for row in range(3)):
                return True
        
        # Verificar diagonais
        if board[0][0] == board[1][1] == board[2][2] == player:
            return True
        if board[0][2] == board[1][1] == board[2][0] == player:
            return True
        
        return False
    
    def is_board_full():
        return all(board[row][col] != "" for row in range(3) for col in range(3))
    
    def reset_game():
        nonlocal current_player, board, game_over
        current_player = "X"
        board = [["", "", ""], ["", "", ""], ["", "", ""]]
        game_over = False
        player_turn.value = f"Vez do jogador: {current_player}"
        create_board()
        page.update()
    
    # Layout principal
    page.add(
        ft.Column(
            [
                title,
                player_turn,
                score_display,
                ft.Divider(),
                board_ui,
                ft.Divider(),
                restart_button
            ],
            spacing=20,
            horizontal_alignment="center"
        )
    )
    
    # Inicializar o tabuleiro
    create_board()

ft.app(target=main)