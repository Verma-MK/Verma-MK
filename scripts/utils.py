#!/usr/bin/env python3
"""
Utility functions for chess game management
"""

import os
from datetime import datetime
import chess

def log_move(move_info):
    """Log move to console and optionally to file"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {move_info}"
    print(log_entry)
    
    # Optionally write to log file
    try:
        with open('moves.log', 'a') as f:
            f.write(log_entry + '\n')
    except Exception as e:
        print(f"Error writing to log file: {e}")

def update_readme(engine, stats=None):
    """Update README.md with current game state and statistics"""
    try:
        # Read current README template or create new one
        readme_template = get_readme_template(engine, stats)
        
        with open('README.md', 'w') as f:
            f.write(readme_template)
            
        print("README.md updated successfully")
    except Exception as e:
        print(f"Error updating README: {e}")

def get_readme_template(engine, stats=None):
    """Generate README content with current game state and statistics"""
    game_status = engine.get_game_status()
    move_count = engine.get_move_count()
    last_moves = engine.get_last_moves(3)
    current_fen = engine.get_fen()
    
    # Determine whose turn it is and game state
    turn_indicator = "⚪ **White to move**" if engine.board.turn else "⚫ **Black to move (AI)**"
    
    if engine.board.is_game_over():
        turn_indicator = "🏁 **Game Over**"
    
    # Generate leaderboard section if stats available
    leaderboard_section = ""
    achievements_section = ""
    game_stats_section = ""
    
    if stats:
        try:
            # Get leaderboard
            leaderboard = stats.get_leaderboard(5)
            if leaderboard:
                leaderboard_section = "\n## 🏆 Leaderboard\n\n"
                leaderboard_section += "| Rank | Player | Score | W/L/D | Win Rate | Moves |\n"
                leaderboard_section += "|------|--------|-------|-------|----------|-------|\n"
                
                for i, player in enumerate(leaderboard, 1):
                    win_rate = f"{player['win_rate']:.1%}" if player['games'] > 0 else "0%"
                    leaderboard_section += f"| {i} | {player['username']} | {player['score']} | {player['wins']}/{player['losses']}/{player['draws']} | {win_rate} | {player['moves']} |\n"
            
            # Get recent achievements
            recent_players = list(stats.stats['players'].keys())[-3:] if stats.stats['players'] else []
            if recent_players:
                achievements_section = "\n## 🎖️ Recent Achievements\n\n"
                for player in recent_players:
                    achievements = stats.get_player_achievements(player)
                    if achievements:
                        achievements_section += f"**{player}**: {', '.join(achievements[:2])}\n\n"
            
            # Game statistics
            total_games = stats.stats.get('total_games', 0)
            ai_wins = stats.stats.get('ai_wins', 0)
            player_wins = stats.stats.get('player_wins', 0)
            draws = stats.stats.get('draws', 0)
            
            if total_games > 0:
                ai_win_rate = ai_wins / total_games * 100
                game_stats_section = f"\n## 📈 Game Statistics\n\n"
                game_stats_section += f"- **Total Games Played**: {total_games}\n"
                game_stats_section += f"- **AI Win Rate**: {ai_win_rate:.1f}% ({ai_wins} wins)\n"
                game_stats_section += f"- **Player Victories**: {player_wins}\n"
                game_stats_section += f"- **Draws**: {draws}\n"
                game_stats_section += f"- **Total Moves**: {stats.stats.get('total_moves', 0)}\n"
        except Exception as e:
            print(f"Error generating stats sections: {e}")
    
    readme_content = f"""# ♟️ Interactive Chess Game

Welcome to my GitHub profile chess game! Challenge a competitive AI opponent by opening a GitHub Issue.

## 🏁 Current Game Status

{turn_indicator}

**Game Status:** {game_status}  
**Total Moves:** {move_count}  
**Last Moves:** {last_moves if last_moves else "Game just started"}

## 📋 Current Board

![Chess Board](board.svg)

## 🎮 How to Play

1. **Make a Move**: Open a new [GitHub Issue](../../issues/new) with the title format: `Move: [your_move]`
   
   Examples:
   - `Move: e2e4` (pawn from e2 to e4)
   - `Move: Nf3` (knight to f3)
   - `Move: O-O` (kingside castling)
   - `Move: Qxd7+` (queen captures with check)

2. **Wait for Processing**: The GitHub Action will automatically:
   - Validate your move
   - Update the board
   - Generate a strategic AI response
   - Track your statistics and achievements
   - Comment on your issue with the result
   - Close the issue

3. **Check the Board**: Return to this README to see the updated position!

## 📝 Move Format Guide

Use standard algebraic notation:
- **Pawn moves**: `e4`, `d5`, `exd5` (capture)
- **Piece moves**: `Nf3`, `Bb5`, `Qh5`, `Ra1`
- **Castling**: `O-O` (kingside), `O-O-O` (queenside)  
- **Promotions**: `e8=Q`, `a1=N`
- **Check/Checkmate**: Add `+` for check, `#` for checkmate

Or use UCI notation (from-to squares):
- `e2e4`, `g1f3`, `e1g1` (castling)

## 🤖 AI Opponent

The AI uses advanced strategy with Stockfish engine fallback. It prioritizes:
- **Checkmate threats** - Always looking for winning combinations
- **Tactical captures** - High-value piece exchanges
- **Positional play** - Center control and piece development
- **Strategic depth** - Multi-move planning

The AI is configured to provide challenging gameplay and will adapt its strategy based on the game phase!

{leaderboard_section}{achievements_section}{game_stats_section}

## 📊 Game Information

- **Current FEN**: `{current_fen}`
- **Game Type**: Human vs Advanced AI
- **Time Control**: Correspondence (no time limit)
- **Engine**: Stockfish + Strategic Analysis
- **Difficulty**: Competitive (Designed to win)

## 🔄 Starting a New Game

If you'd like to start a new game, open an issue with the title: `Move: reset`

## 🏅 Achievement System

Earn achievements by playing:
- **🏃 Century Player** - Play 100+ moves
- **🎯 Regular Player** - Participate in 10+ games  
- **👑 Winner** - Achieve 5+ victories
- **💎 Brilliant Tactician** - Make 5+ brilliant moves
- **⭐ High Performer** - Maintain 70%+ win rate

## 📚 Chess Resources

- [Chess.com Learn](https://www.chess.com/learn)
- [Lichess Practice](https://lichess.org/practice)
- [Chess Rules](https://www.chess.com/learn-how-to-play-chess)

---

*This chess game is powered by GitHub Actions, python-chess, Stockfish engine, and advanced move analysis.*

**🎯 Challenge the AI and make your move!** [Open New Issue →](../../issues/new)
"""

    return readme_content

def append_move_to_pgn(move_san, player="Human"):
    """Append move to PGN file for game history"""
    try:
        pgn_file = 'game_history.pgn'
        
        # Check if file exists and has content
        if not os.path.exists(pgn_file) or os.path.getsize(pgn_file) == 0:
            # Initialize PGN file with headers
            with open(pgn_file, 'w') as f:
                f.write('[Event "GitHub Chess Game"]\n')
                f.write('[Site "GitHub Repository"]\n')
                f.write(f'[Date "{datetime.now().strftime("%Y.%m.%d")}"]\n')
                f.write('[Round "1"]\n')
                f.write('[White "Human Players"]\n')
                f.write('[Black "Stockfish AI"]\n')
                f.write('[Result "*"]\n\n')
                
        # Append move
        with open(pgn_file, 'a') as f:
            f.write(f"{move_san} ")
            
    except Exception as e:
        print(f"Error updating PGN: {e}")

def get_game_statistics():
    """Get basic game statistics"""
    stats = {
        'total_games': 0,
        'total_moves': 0,
        'last_updated': datetime.now().isoformat()
    }
    
    try:
        if os.path.exists('game_state.fen'):
            with open('game_state.fen', 'r') as f:
                fen = f.read().strip()
                if fen:
                    board = chess.Board(fen)
                    stats['total_moves'] = len(board.move_stack)
        
        # Count games from PGN file
        if os.path.exists('game_history.pgn'):
            with open('game_history.pgn', 'r') as f:
                content = f.read()
                stats['total_games'] = content.count('[Event')
                
    except Exception as e:
        print(f"Error getting statistics: {e}")
    
    return stats

def validate_move_format(move_str):
    """Validate move string format"""
    import re
    
    # Common chess move patterns
    patterns = [
        r'^[a-h][1-8][a-h][1-8][qrnb]?$',  # UCI notation (e2e4, a7a8q)
        r'^[KQRNB][a-h1-8]*[a-h][1-8]$',   # Piece moves (Nf3, Bb5)
        r'^[a-h][1-8]$',                    # Pawn moves (e4, d5)  
        r'^[a-h]x[a-h][1-8]$',             # Pawn captures (exd5)
        r'^O-O(-O)?$',                      # Castling
        r'^[a-h][18]=[QRNB]$',             # Promotion (e8=Q)
    ]
    
    move_str = move_str.strip()
    
    for pattern in patterns:
        if re.match(pattern, move_str, re.IGNORECASE):
            return True
            
    return False
