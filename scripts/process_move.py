#!/usr/bin/env python3
"""
Main script to process chess moves from GitHub Issues
"""

import os
import sys
import re
from github import Github
from chess_engine import ChessEngine
from board_generator import BoardGenerator
from utils import update_readme, log_move
from game_stats import GameStats

def extract_move_from_title(title):
    """Extract chess move from issue title"""
    # Check for reset command first
    if re.search(r'Move:\s*reset', title, re.IGNORECASE):
        return "reset"
    
    # Match patterns like "Move: e2e4", "Move: Nf3", "Move: O-O", etc.
    match = re.search(r'Move:\s*([a-h][1-8][a-h][1-8][qrnb]?|[KQRNB][a-h1-8]*[a-h][1-8]|O-O-O|O-O|[a-h]x[a-h][1-8])', title, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return None

def comment_on_issue(github_client, repo_name, issue_number, comment):
    """Add a comment to the GitHub issue"""
    try:
        repo = github_client.get_repo(repo_name)
        issue = repo.get_issue(issue_number)
        issue.create_comment(comment)
        return True
    except Exception as e:
        print(f"Error commenting on issue: {e}")
        return False

def close_issue(github_client, repo_name, issue_number):
    """Close the GitHub issue"""
    try:
        repo = github_client.get_repo(repo_name)
        issue = repo.get_issue(issue_number)
        issue.edit(state='closed')
        return True
    except Exception as e:
        print(f"Error closing issue: {e}")
        return False

def main():
    # Get environment variables
    github_token = os.getenv('GITHUB_TOKEN')
    issue_number_str = os.getenv('ISSUE_NUMBER')
    issue_title = os.getenv('ISSUE_TITLE')
    issue_author = os.getenv('ISSUE_AUTHOR')
    repository = os.getenv('REPOSITORY')
    
    if not all([github_token, issue_number_str, issue_title, repository]):
        print("Missing required environment variables")
        sys.exit(1)
    
    if issue_number_str is None:
        print("Missing issue number")
        sys.exit(1)
    
    try:
        issue_number = int(issue_number_str)
    except ValueError:
        print("Invalid issue number")
        sys.exit(1)
    
    # Initialize GitHub client
    github_client = Github(github_token)
    
    # Extract move from issue title
    player_move = extract_move_from_title(issue_title)
    if not player_move:
        comment = f"❌ **Invalid move format!**\n\nPlease use the format: `Move: e2e4` (standard algebraic notation)\n\nExamples:\n- `Move: e2e4` (pawn move)\n- `Move: Nf3` (knight move)\n- `Move: O-O` (castling)\n- `Move: Qxd7+` (queen captures with check)\n- `Move: reset` (start new game)"
        comment_on_issue(github_client, repository, issue_number, comment)
        close_issue(github_client, repository, issue_number)
        return
    
    print(f"Processing move: {player_move} by {issue_author}")
    
    # Initialize chess engine
    engine = ChessEngine()
    
    # Handle reset command
    if player_move.lower() == "reset":
        try:
            engine.reset_game()
            
            # Generate new board
            board_gen = BoardGenerator()
            board_gen.generate_board_svg(engine.board)
            
            # Update README
            update_readme(engine)
            
            comment = f"🔄 **Game Reset!**\n\n{issue_author} has started a new chess game!\n\nThe board has been reset to the starting position. White to move first!\n\nCheck the updated board in the README and make your opening move!"
            comment_on_issue(github_client, repository, issue_number, comment)
            close_issue(github_client, repository, issue_number)
            
            log_move(f"{issue_author}: Game reset")
            print("Game reset successfully")
            return
            
        except Exception as e:
            error_comment = f"❌ **Error resetting game**\n\nThere was an unexpected error: {str(e)}\n\nPlease try again or report this issue."
            comment_on_issue(github_client, repository, issue_number, error_comment)
            close_issue(github_client, repository, issue_number)
            print(f"Error resetting game: {e}")
            return
    
    # Try to make the player's move
    try:
        success, message = engine.make_player_move(player_move)
        
        if not success:
            comment = f"❌ **Invalid move: {player_move}**\n\n{message}\n\nCurrent position: `{engine.get_fen()}`\n\nPlease check the current board state in the README and try again with a legal move."
            comment_on_issue(github_client, repository, issue_number, comment)
            close_issue(github_client, repository, issue_number)
            return
            
        # Initialize statistics tracker
        stats = GameStats()
        
        # Analyze move quality and record player move
        move_quality = stats.analyze_move_quality(engine.board, player_move)
        stats.record_move(issue_author, player_move, move_quality)
        
        # Log the player move
        log_move(f"{issue_author}: {player_move}")
        
        # Generate AI response
        ai_move, ai_message = engine.get_ai_move()
        
        if ai_move:
            engine.make_ai_move(ai_move)
            # Record AI move
            stats.record_move("AI", ai_move, "normal")
            log_move(f"AI: {ai_move}")
            
        # Check for game over and record results
        if engine.board.is_game_over():
            if engine.board.is_checkmate():
                winner = "AI" if engine.board.turn else issue_author
            else:
                winner = "Draw"
            stats.record_game_end(winner, [issue_author])
            
        # Save game state
        engine.save_game_state()
        
        # Generate new board
        board_gen = BoardGenerator()
        board_gen.generate_board_svg(engine.board)
        
        # Update README with stats
        update_readme(engine, stats)
        
        # Create success comment
        game_status = ""
        if engine.board.is_checkmate():
            if engine.board.turn:  # White to move, so black won
                game_status = "\n🎉 **Checkmate! AI (Black) wins!**"
            else:  # Black to move, so white won  
                game_status = "\n🎉 **Checkmate! You (White) win!**"
        elif engine.board.is_stalemate():
            game_status = "\n🤝 **Stalemate! It's a draw!**"
        elif engine.board.is_check():
            game_status = "\n⚠️ **Check!**"
            
        comment = f"✅ **Move accepted: {player_move}**\n\nAI responds with: **{ai_move}**\n{ai_message}{game_status}\n\nCheck the updated board in the README!"
        
        comment_on_issue(github_client, repository, issue_number, comment)
        close_issue(github_client, repository, issue_number)
        
        print(f"Successfully processed move: {player_move}, AI responded: {ai_move}")
        
    except Exception as e:
        error_comment = f"❌ **Error processing move**\n\nThere was an unexpected error: {str(e)}\n\nPlease try again or report this issue."
        comment_on_issue(github_client, repository, issue_number, error_comment)
        close_issue(github_client, repository, issue_number)
        print(f"Error processing move: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
