def chess_positions():
    return [f"{char}{num + 1}" for num in range(8) for char in "abcdefgh"]

def knight_moves():
    positions = chess_positions()
    moves = []
    for position in positions:
        position_alpha_ord = ord(position[0])
        position_digit = int(position[1])
        moves.append(f"{position}{chr(position_alpha_ord + 2)}{min(max(position_digit + 1, 0), 9)}")
        moves.append(f"{position}{chr(position_alpha_ord + 2)}{min(max(position_digit - 1, 0), 9)}")
        moves.append(f"{position}{chr(position_alpha_ord - 2)}{min(max(position_digit + 1, 0), 9)}")
        moves.append(f"{position}{chr(position_alpha_ord - 2)}{min(max(position_digit - 1, 0), 9)}")
        moves.append(f"{position}{chr(position_alpha_ord + 1)}{min(max(position_digit + 2, 0), 9)}")
        moves.append(f"{position}{chr(position_alpha_ord + 1)}{min(max(position_digit - 2, 0), 9)}")
        moves.append(f"{position}{chr(position_alpha_ord - 1)}{min(max(position_digit + 2, 0), 9)}")
        moves.append(f"{position}{chr(position_alpha_ord - 1)}{min(max(position_digit - 2, 0), 9)}")

    return [move for move in moves if move[-2:] in positions]

def bishop_moves():
    def helper(position, positions, x, y):
        position_alpha_ord = ord(position[0])
        position_digit = int(position[1])
        next_pos = f"{chr(position_alpha_ord + x)}{min(max(position_digit + y, 0), 9)}"
        if next_pos in positions:
            return [next_pos] + helper(next_pos, positions, x, y)
        else:
            return []
        
    positions = chess_positions()
    moves = []
    for position in positions:
        moves += [position + next_pos for next_pos in helper(position, positions, 1, 1)]
        moves += [position + next_pos for next_pos in helper(position, positions, 1, -1)]
        moves += [position + next_pos for next_pos in helper(position, positions, -1, 1)]
        moves += [position + next_pos for next_pos in helper(position, positions, -1, -1)]
    return moves

def rook_moves():
    def helper(position, positions, x, y):
        position_alpha_ord = ord(position[0])
        position_digit = int(position[1])
        next_pos = f"{chr(position_alpha_ord + x)}{min(max(position_digit + y, 0), 9)}"
        if next_pos in positions:
            return [next_pos] + helper(next_pos, positions, x, y)
        else:
            return []
    positions = chess_positions()
    moves = []
    for position in positions:
        moves += [position + next_pos for next_pos in helper(position, positions, 1, 0)]
        moves += [position + next_pos for next_pos in helper(position, positions, -1, 0)]
        moves += [position + next_pos for next_pos in helper(position, positions, 0, 1)]
        moves += [position + next_pos for next_pos in helper(position, positions, 0, -1)]
    return moves

def queen_moves():
    return rook_moves() + bishop_moves()

def pawn_promotion_moves():
    def helper(position, positions, x, y):
        position_alpha_ord = ord(position[0])
        position_digit = int(position[1])
        next_pos = f"{chr(position_alpha_ord + x)}{min(max(position_digit + y, 0), 9)}"
        if next_pos in positions:
            return [next_pos] + helper(next_pos, positions, x, y)
        else:
            return []
    positions = chess_positions()
    pawn_positions_white = [alpha + "7" for alpha in "abcdefgh"]
    pawn_positions_black = [alpha + "2" for alpha in "abcdefgh"]
    moves = []
    for position in pawn_positions_white:
        moves += [position + next_pos + "q" for next_pos in helper(position, positions, 0, 1)]
        moves += [position + next_pos + "r" for next_pos in helper(position, positions, 0, 1)]
        moves += [position + next_pos + "b" for next_pos in helper(position, positions, 0, 1)]
        moves += [position + next_pos + "n" for next_pos in helper(position, positions, 0, 1)]
        moves += [position + next_pos + "q" for next_pos in helper(position, positions, 1, 1)]
        moves += [position + next_pos + "r" for next_pos in helper(position, positions, 1, 1)]
        moves += [position + next_pos + "b" for next_pos in helper(position, positions, 1, 1)]
        moves += [position + next_pos + "n" for next_pos in helper(position, positions, 1, 1)]
        moves += [position + next_pos + "q" for next_pos in helper(position, positions, -1, 1)]
        moves += [position + next_pos + "r" for next_pos in helper(position, positions, -1, 1)]
        moves += [position + next_pos + "b" for next_pos in helper(position, positions, -1, 1)]
        moves += [position + next_pos + "n" for next_pos in helper(position, positions, -1, 1)]
    for position in pawn_positions_black:
        moves += [position + next_pos + "q" for next_pos in helper(position, positions, 0, -1)]
        moves += [position + next_pos + "r" for next_pos in helper(position, positions, 0, -1)]
        moves += [position + next_pos + "b" for next_pos in helper(position, positions, 0, -1)]
        moves += [position + next_pos + "n" for next_pos in helper(position, positions, 0, -1)]
        moves += [position + next_pos + "q" for next_pos in helper(position, positions, 1, -1)]
        moves += [position + next_pos + "r" for next_pos in helper(position, positions, 1, -1)]
        moves += [position + next_pos + "b" for next_pos in helper(position, positions, 1, -1)]
        moves += [position + next_pos + "n" for next_pos in helper(position, positions, 1, -1)]
        moves += [position + next_pos + "q" for next_pos in helper(position, positions, -1, -1)]
        moves += [position + next_pos + "r" for next_pos in helper(position, positions, -1, -1)]
        moves += [position + next_pos + "b" for next_pos in helper(position, positions, -1, -1)]
        moves += [position + next_pos + "n" for next_pos in helper(position, positions, -1, -1)]
    
    return moves

def possible_moves():
    # Naive way of determining action space, weeds out invalid actions
    return knight_moves() + queen_moves() + pawn_promotion_moves()

moves = possible_moves()
