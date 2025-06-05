#!/usr/bin/env python3
"""
Generate SVG chess board visualization
"""

import chess
import os

class BoardGenerator:
    def __init__(self):
        """Initialize board generator with piece symbols"""
        # Unicode chess pieces
        self.piece_symbols = {
            'P': '♟', 'R': '♜', 'N': '♞', 'B': '♝', 'Q': '♛', 'K': '♚',  # Black pieces
            'p': '♙', 'r': '♖', 'n': '♘', 'b': '♗', 'q': '♕', 'k': '♔'   # White pieces
        }
        
        # Colors
        self.light_square = '#F0D9B5'
        self.dark_square = '#B58863'
        self.text_color = '#333333'
        
    def get_piece_symbol(self, piece):
        """Get Unicode symbol for chess piece"""
        if piece is None:
            return ''
        
        # Convert python-chess piece to our symbol mapping
        symbol = piece.symbol()
        return self.piece_symbols.get(symbol, '')
    
    def generate_board_svg(self, board):
        """Generate SVG representation of chess board"""
        square_size = 60
        board_size = square_size * 8
        margin = 30
        total_size = board_size + 2 * margin
        
        # Start SVG
        svg_lines = [
            f'<svg width="{total_size}" height="{total_size}" xmlns="http://www.w3.org/2000/svg">',
            f'<rect width="{total_size}" height="{total_size}" fill="#FFFFFF"/>',
            f'<!-- Chess Board -->',
        ]
        
        # Draw squares and pieces
        for rank in range(8):
            for file in range(8):
                x = margin + file * square_size
                y = margin + (7 - rank) * square_size  # Flip vertically for proper orientation
                
                # Square color
                is_light = (rank + file) % 2 == 0
                square_color = self.light_square if is_light else self.dark_square
                
                # Draw square
                svg_lines.append(
                    f'<rect x="{x}" y="{y}" width="{square_size}" height="{square_size}" fill="{square_color}"/>'
                )
                
                # Get piece at this square
                square = chess.square(file, rank)
                piece = board.piece_at(square)
                
                if piece:
                    piece_symbol = self.get_piece_symbol(piece)
                    if piece_symbol:
                        # Center piece in square
                        text_x = x + square_size // 2
                        text_y = y + square_size // 2 + 8  # Offset for text centering
                        
                        svg_lines.append(
                            f'<text x="{text_x}" y="{text_y}" text-anchor="middle" '
                            f'font-family="serif" font-size="{square_size-10}" fill="{self.text_color}">'
                            f'{piece_symbol}</text>'
                        )
        
        # Add coordinate labels
        # Files (a-h) at bottom
        for file in range(8):
            x = margin + file * square_size + square_size // 2
            y = total_size - 10
            file_label = chr(ord('a') + file)
            svg_lines.append(
                f'<text x="{x}" y="{y}" text-anchor="middle" '
                f'font-family="monospace" font-size="14" fill="{self.text_color}">'
                f'{file_label}</text>'
            )
        
        # Ranks (1-8) at left
        for rank in range(8):
            x = 15
            y = margin + (7 - rank) * square_size + square_size // 2 + 5
            rank_label = str(rank + 1)
            svg_lines.append(
                f'<text x="{x}" y="{y}" text-anchor="middle" '
                f'font-family="monospace" font-size="14" fill="{self.text_color}">'
                f'{rank_label}</text>'
            )
        
        # Close SVG
        svg_lines.append('</svg>')
        
        # Write to file
        svg_content = '\n'.join(svg_lines)
        try:
            with open('board.svg', 'w') as f:
                f.write(svg_content)
            print("Board SVG generated successfully")
        except Exception as e:
            print(f"Error writing SVG file: {e}")
        
        return svg_content
    
    def generate_minimal_board_svg(self, board):
        """Generate a minimal SVG board for embedding"""
        square_size = 40
        board_size = square_size * 8
        
        # Start SVG
        svg_lines = [
            f'<svg width="{board_size}" height="{board_size}" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {board_size} {board_size}">',
        ]
        
        # Draw squares and pieces
        for rank in range(8):
            for file in range(8):
                x = file * square_size
                y = (7 - rank) * square_size  # Flip vertically
                
                # Square color
                is_light = (rank + file) % 2 == 0
                square_color = self.light_square if is_light else self.dark_square
                
                # Draw square
                svg_lines.append(
                    f'<rect x="{x}" y="{y}" width="{square_size}" height="{square_size}" fill="{square_color}"/>'
                )
                
                # Get piece
                square = chess.square(file, rank)
                piece = board.piece_at(square)
                
                if piece:
                    piece_symbol = self.get_piece_symbol(piece)
                    if piece_symbol:
                        text_x = x + square_size // 2
                        text_y = y + square_size // 2 + 6
                        
                        svg_lines.append(
                            f'<text x="{text_x}" y="{text_y}" text-anchor="middle" '
                            f'font-family="serif" font-size="{square_size-8}" fill="{self.text_color}">'
                            f'{piece_symbol}</text>'
                        )
        
        svg_lines.append('</svg>')
        return '\n'.join(svg_lines)
