import chess
import chess.engine
import chess.pgn
import os
from datetime import datetime

class ChessEngine:
    def __init__(self):
        """Initialize chess engine with current game state"""
        self.board = chess.Board()
        self.load_game_state()
        
    def load_game_state(self):
        """Load game state from FEN file"""
        try:
            if os.path.exists('game_state.fen'):
                with open('game_state.fen', 'r') as f:
                    fen = f.read().strip()
                    if fen:
                        self.board = chess.Board(fen)
                        print(f"Loaded game state: {fen}")
        except Exception as e:
            print(f"Error loading game state: {e}")
            self.board = chess.Board()
            
    def save_game_state(self):
        """Save current game state to FEN file"""
        try:
            with open('game_state.fen', 'w') as f:
                f.write(self.board.fen())
            print(f"Saved game state: {self.board.fen()}")
        except Exception as e:
            print(f"Error saving game state: {e}")
            
    def get_fen(self):
        """Get current board FEN"""
        return self.board.fen()
        
    def make_player_move(self, move_str):
        """
        Attempt to make a player move
        Returns (success: bool, message: str)
        """
        try:
            move = None
            
            try:
                move = self.board.parse_san(move_str)
            except ValueError:
                pass
                
            if move is None:
                try:
                    move = chess.Move.from_uci(move_str)
                except ValueError:
                    pass
            
            if move is None:
                return False, f"Could not parse move: {move_str}"
                
            if move not in self.board.legal_moves:
                legal_moves = [self.board.san(m) for m in self.board.legal_moves]
                return False, f"Illegal move. Legal moves: {', '.join(legal_moves[:10])}{'...' if len(legal_moves) > 10 else ''}"
            
            self.board.push(move)
            return True, f"Move {move_str} played successfully"
            
        except Exception as e:
            return False, f"Error processing move: {str(e)}"
    
    def get_ai_move(self):

        try:
            if self.board.is_game_over():
                return None, "Game is over"
                
            stockfish_path = '/usr/games/stockfish'
            if not os.path.exists(stockfish_path):
                stockfish_path = 'stockfish'
                
            with chess.engine.SimpleEngine.popen_uci(stockfish_path) as engine:
               
                engine.configure({
                    "Skill Level": 20,
                    "Threads": 2,
                    "Hash": 128,
                    "MultiPV": 1,
                    "UCI_LimitStrength": False,
                    "UCI_Elo": 3200
                })
                
                result = engine.play(self.board, chess.engine.Limit(time=5.0, depth=15))
                
                if result.move:
                    move_san = self.board.san(result.move)
                    return move_san, f"AI plays {move_san}"
                    
        except Exception as e:
            print(f"Stockfish engine error: {e}")
            
       
        return self._get_strategic_move()
    
    def _get_strategic_move(self):
        """
        Ultra-advanced AI strategy designed to be unbeatable
        Multi-layered analysis: tactical, positional, and endgame patterns
        """
        legal_moves = list(self.board.legal_moves)
        if not legal_moves:
            return None, "No legal moves available"
        
        critical_moves = self._find_critical_moves(legal_moves)
        if critical_moves:
            return critical_moves
        
        best_move = self._evaluate_positional_moves(legal_moves)
        if best_move:
            return best_move
        
        if len(self.board.move_stack) < 12:
            opening_move = self._get_opening_book_move(legal_moves)
            if opening_move:
                return opening_move
        
        if self._is_endgame():
            endgame_move = self._get_endgame_move(legal_moves)
            if endgame_move:
                return endgame_move
        
        return self._minimax_evaluation(legal_moves, depth=3)
    
    def _find_critical_moves(self, legal_moves):
        """Find game-critical moves: checkmate, check escape, major threats"""
        
        for move in legal_moves:
            self.board.push(move)
            if self.board.is_checkmate():
                move_san = self.board.san(move)
                self.board.pop()
                return move_san, f"AI plays {move_san} - Checkmate!"
            self.board.pop()
        
        for move in legal_moves:
            self.board.push(move)
            opponent_moves = list(self.board.legal_moves)
            mate_in_2 = True
            for opp_move in opponent_moves:
                self.board.push(opp_move)
                ai_moves_2 = list(self.board.legal_moves)
                has_mate = False
                for ai_move_2 in ai_moves_2:
                    self.board.push(ai_move_2)
                    if self.board.is_checkmate():
                        has_mate = True
                        self.board.pop()
                        break
                    self.board.pop()
                self.board.pop()
                if not has_mate:
                    mate_in_2 = False
                    break
            self.board.pop()
            if mate_in_2 and opponent_moves:
                move_san = self.board.san(move)
                return move_san, f"AI plays {move_san} - Forced mate in 2!"
        
        if self.board.is_check():
            defensive_moves = []
            for move in legal_moves:
                self.board.push(move)
                if not self.board.is_check():
                    safety_score = self._evaluate_king_safety()
                    defensive_moves.append((move, safety_score))
                self.board.pop()
            
            if defensive_moves:
                defensive_moves.sort(key=lambda x: x[1], reverse=True)
                best_defense = defensive_moves[0][0]
                move_san = self.board.san(best_defense)
                return move_san, f"AI plays {move_san} - Defending!"
        
        tactical_moves = []
        for move in legal_moves:
            material_gain = self._calculate_material_gain(move)
            if material_gain > 0:
                tactical_moves.append((move, material_gain))
        
        if tactical_moves:
            tactical_moves.sort(key=lambda x: x[1], reverse=True)
            best_tactical = tactical_moves[0][0]
            move_san = self.board.san(best_tactical)
            return move_san, f"AI plays {move_san} - Wins material!"
        
        return None
    
    def _evaluate_positional_moves(self, legal_moves):
        """Advanced positional evaluation"""
        scored_moves = []
        
        for move in legal_moves:
            score = 0
            piece = self.board.piece_at(move.from_square)
            
            score += self._piece_square_value(piece, move.to_square)
            
            center_squares = [chess.D4, chess.D5, chess.E4, chess.E5]
            if move.to_square in center_squares:
                score += 30
            
            if len(self.board.move_stack) < 16:
                if piece and piece.piece_type in [chess.KNIGHT, chess.BISHOP]:
                    if move.from_square in [chess.B1, chess.G1, chess.C1, chess.F1]:
                        score += 25
            
            if piece and piece.piece_type == chess.KING:
                if len(self.board.move_stack) < 20: 
                    if move.to_square in [chess.G1, chess.C1]: 
                        score += 50
            
            self.board.push(move)
            controlled_squares = len(list(self.board.attacks(move.to_square)))
            score += controlled_squares * 2
            self.board.pop()
            
            scored_moves.append((move, score))
        
        if scored_moves:
            scored_moves.sort(key=lambda x: x[1], reverse=True)
            best_positional = scored_moves[0][0]
            move_san = self.board.san(best_positional)
            return move_san, f"AI plays {move_san} - Positional advantage!"
        
        return None
    
    def _get_opening_book_move(self, legal_moves):
        """Opening book with strong theoretical moves"""
        move_stack_length = len(self.board.move_stack)
        
        opening_responses = {
            "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR": ["c5", "e5", "c6"], 
            "rnbqkbnr/pppppppp/8/8/3P4/8/PPP1PPPP/RNBQKBNR": ["Nf6", "d5", "f5"],
            "r1bqkbnr/pppp1ppp/2n5/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R": ["f5", "Be7", "Nf6"]
        }
        
        current_fen = self.board.fen().split()[0] 
        if current_fen in opening_responses:
            for response in opening_responses[current_fen]:
                try:
                    move = self.board.parse_san(response)
                    if move in legal_moves:
                        return response, f"AI plays {response} - Opening theory!"
                except:
                    continue
        
        if move_stack_length < 8:
            priority_moves = []
            for move in legal_moves:
                piece = self.board.piece_at(move.from_square)
                if piece:
                    if piece.piece_type == chess.PAWN and move.to_square in [chess.D4, chess.D5, chess.E4, chess.E5]:
                        priority_moves.append((move, 40))
                    elif piece.piece_type == chess.KNIGHT:
                        good_squares = [chess.F3, chess.C3, chess.F6, chess.C6]
                        if move.to_square in good_squares:
                            priority_moves.append((move, 35))
                    elif piece.piece_type == chess.BISHOP:
                        good_squares = [chess.C4, chess.F4, chess.E2, chess.C5, chess.F5, chess.E7]
                        if move.to_square in good_squares:
                            priority_moves.append((move, 30))
            
            if priority_moves:
                priority_moves.sort(key=lambda x: x[1], reverse=True)
                best_opening = priority_moves[0][0]
                move_san = self.board.san(best_opening)
                return move_san, f"AI plays {move_san} - Opening principles!"
        
        return None
    
    def _is_endgame(self):
        """Determine if we're in endgame phase"""
        piece_count = len([sq for sq in chess.SQUARES if self.board.piece_at(sq) is not None])
        return piece_count <= 12 or (piece_count <= 16 and not any([
            self.board.pieces(chess.QUEEN, chess.WHITE),
            self.board.pieces(chess.QUEEN, chess.BLACK)
        ]))
    
    def _get_endgame_move(self, legal_moves):
        
        scored_moves = []
        for move in legal_moves:
            score = 0
            piece = self.board.piece_at(move.from_square)
            
            if piece and piece.piece_type == chess.KING:
                
                king_advancement = chess.square_rank(move.to_square) if piece.color else 7 - chess.square_rank(move.to_square)
                score += king_advancement * 10   
                center_distance = abs(chess.square_file(move.to_square) - 3.5) + abs(chess.square_rank(move.to_square) - 3.5)
                score += (7 - center_distance) * 5
            
            if piece and piece.piece_type == chess.PAWN:
                promotion_distance = 7 - chess.square_rank(move.to_square) if piece.color else chess.square_rank(move.to_square)
                score += (7 - promotion_distance) * 15
            
            scored_moves.append((move, score))
        
        if scored_moves:
            scored_moves.sort(key=lambda x: x[1], reverse=True)
            best_endgame = scored_moves[0][0]
            move_san = self.board.san(best_endgame)
            return move_san, f"AI plays {move_san} - Endgame technique!"
        
        return None
    
    def _minimax_evaluation(self, legal_moves, depth=3):
        
        best_score = float('-inf')
        best_move = None
        
        for move in legal_moves:
            self.board.push(move)
            score = self._evaluate_position() - self._minimax_helper(depth - 1, False, float('-inf'), float('inf'))
            self.board.pop()
            
            if score > best_score:
                best_score = score
                best_move = move
        
        if best_move:
            move_san = self.board.san(best_move)
            return move_san, f"AI plays {move_san} - Deep calculation!"
        
        # Fallback
        import random
        move = random.choice(legal_moves)
        move_san = self.board.san(move)
        return move_san, f"AI plays {move_san} - Strategic!"
    
    def _minimax_helper(self, depth, maximizing, alpha, beta):
        
        if depth == 0 or self.board.is_game_over():
            return self._evaluate_position()
        
        legal_moves = list(self.board.legal_moves)
        
        if maximizing:
            max_eval = float('-inf')
            for move in legal_moves[:8]: 
                self.board.push(move)
                eval_score = self._minimax_helper(depth - 1, False, alpha, beta)
                self.board.pop()
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for move in legal_moves[:8]:
                self.board.push(move)
                eval_score = self._minimax_helper(depth - 1, True, alpha, beta)
                self.board.pop()
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
            return min_eval
    
    def _evaluate_position(self):
        
        if self.board.is_checkmate():
            return -10000 if self.board.turn else 10000
        if self.board.is_stalemate() or self.board.is_insufficient_material():
            return 0
        
        score = 0
        piece_values = {chess.PAWN: 100, chess.KNIGHT: 320, chess.BISHOP: 330, 
                       chess.ROOK: 500, chess.QUEEN: 900, chess.KING: 0}
        
        
        for square in chess.SQUARES:
            piece = self.board.piece_at(square)
            if piece:
                value = piece_values[piece.piece_type]
                score += value if piece.color else -value
        
        
        score += self._evaluate_king_safety() * 20
        score += self._evaluate_piece_mobility() * 10
        
        return score
    
    def _evaluate_king_safety(self):
        
        safety = 0
        return safety
    
    def _evaluate_piece_mobility(self):
        
        mobility = len(list(self.board.legal_moves))
        return mobility
    
    def _calculate_material_gain(self, move):
        
        if not self.board.is_capture(move):
            return 0
        
        captured_piece = self.board.piece_at(move.to_square)
        if captured_piece:
            piece_values = {chess.PAWN: 1, chess.KNIGHT: 3, chess.BISHOP: 3, 
                           chess.ROOK: 5, chess.QUEEN: 9}
            return piece_values.get(captured_piece.piece_type, 0)
        return 0
    
    def _piece_square_value(self, piece, square):
        
        if not piece:
            return 0
        
        rank = chess.square_rank(square)
        file = chess.square_file(square)
        
        if piece.piece_type == chess.PAWN:
            return rank * 5 if piece.color else (7 - rank) * 5
        elif piece.piece_type in [chess.KNIGHT, chess.BISHOP]:
            center_distance = abs(file - 3.5) + abs(rank - 3.5)
            return int(10 - center_distance * 2)
        
        return 0
    
    def make_ai_move(self, move_str):
        
        try:
            
            move = self.board.parse_san(move_str)
            if move in self.board.legal_moves:
                self.board.push(move)
                return True
            else:
                print(f"Illegal AI move attempted: {move_str}")
                return False
        except Exception as e:
            print(f"Error making AI move {move_str}: {e}")
            return False
    
    def get_game_status(self):
        
        if self.board.is_checkmate():
            winner = "Black" if self.board.turn else "White"
            return f"Checkmate! {winner} wins!"
        elif self.board.is_stalemate():
            return "Stalemate! It's a draw!"
        elif self.board.is_insufficient_material():
            return "Draw by insufficient material!"
        elif self.board.is_seventyfive_moves():
            return "Draw by 75-move rule!"
        elif self.board.is_fivefold_repetition():
            return "Draw by fivefold repetition!"
        elif self.board.is_check():
            return "Check!"
        else:
            turn = "White" if self.board.turn else "Black"
            return f"{turn} to move"
    
    def get_move_count(self):
        
        return len(self.board.move_stack)
    
    def get_last_moves(self, count=5):
        
        moves = []
        board_copy = chess.Board()
        
        for i, move in enumerate(self.board.move_stack[-count*2:]):
            move_san = board_copy.san(move)
            board_copy.push(move)
            
            move_number = (len(self.board.move_stack) - len(self.board.move_stack[-count*2:]) + i) // 2 + 1
            
            if i % 2 == 0: 
                moves.append(f"{move_number}. {move_san}")
            else:  
                moves.append(f"{move_san}")
                
        return " ".join(moves)
    
    def reset_game(self):
        
        self.board = chess.Board()
        self.save_game_state()
        
        try:
            with open('game_history.pgn', 'w') as f:
                f.write("")
        except Exception as e:
            print(f"Error clearing PGN: {e}")
