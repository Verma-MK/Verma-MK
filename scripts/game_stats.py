#!/usr/bin/env python3
"""
Game statistics and leaderboard management for GitHub Chess
"""

import json
import os
from datetime import datetime
from collections import defaultdict
import chess

class GameStats:
    def __init__(self):
        """Initialize game statistics manager"""
        self.stats_file = 'game_stats.json'
        self.load_stats()
    
    def load_stats(self):
        """Load game statistics from file"""
        try:
            if os.path.exists(self.stats_file):
                with open(self.stats_file, 'r') as f:
                    self.stats = json.load(f)
            else:
                self.stats = {
                    'players': {},
                    'games': [],
                    'total_moves': 0,
                    'total_games': 0,
                    'ai_wins': 0,
                    'player_wins': 0,
                    'draws': 0,
                    'last_updated': datetime.now().isoformat()
                }
        except Exception as e:
            print(f"Error loading stats: {e}")
            self.stats = self._get_default_stats()
    
    def _get_default_stats(self):
        """Get default stats structure"""
        return {
            'players': {},
            'games': [],
            'total_moves': 0,
            'total_games': 0,
            'ai_wins': 0,
            'player_wins': 0,
            'draws': 0,
            'last_updated': datetime.now().isoformat()
        }
    
    def save_stats(self):
        """Save statistics to file"""
        try:
            self.stats['last_updated'] = datetime.now().isoformat()
            with open(self.stats_file, 'w') as f:
                json.dump(self.stats, f, indent=2)
        except Exception as e:
            print(f"Error saving stats: {e}")
    
    def record_move(self, player, move, move_quality="normal"):
        """Record a player move"""
        if player not in self.stats['players']:
            self.stats['players'][player] = {
                'moves_played': 0,
                'games_participated': 0,
                'wins': 0,
                'losses': 0,
                'draws': 0,
                'brilliant_moves': 0,
                'blunders': 0,
                'first_game': datetime.now().isoformat(),
                'last_active': datetime.now().isoformat(),
                'favorite_openings': {},
                'total_score': 0
            }
        
        player_stats = self.stats['players'][player]
        player_stats['moves_played'] += 1
        player_stats['last_active'] = datetime.now().isoformat()
        
        # Track move quality
        if move_quality == "brilliant":
            player_stats['brilliant_moves'] += 1
            player_stats['total_score'] += 10
        elif move_quality == "blunder":
            player_stats['blunders'] += 1
            player_stats['total_score'] -= 5
        else:
            player_stats['total_score'] += 1
        
        self.stats['total_moves'] += 1
        self.save_stats()
    
    def record_game_start(self, player):
        """Record when a player starts/joins a game"""
        if player not in self.stats['players']:
            self.record_move(player, "", "normal")  # Initialize player
        
        self.stats['players'][player]['games_participated'] += 1
        self.save_stats()
    
    def record_game_end(self, winner, players_involved):
        """Record game completion"""
        self.stats['total_games'] += 1
        
        if winner == "AI":
            self.stats['ai_wins'] += 1
            for player in players_involved:
                if player in self.stats['players']:
                    self.stats['players'][player]['losses'] += 1
        elif winner == "Draw":
            self.stats['draws'] += 1
            for player in players_involved:
                if player in self.stats['players']:
                    self.stats['players'][player]['draws'] += 1
        else:
            self.stats['player_wins'] += 1
            for player in players_involved:
                if player in self.stats['players']:
                    if player == winner:
                        self.stats['players'][player]['wins'] += 1
                        self.stats['players'][player]['total_score'] += 100
                    else:
                        self.stats['players'][player]['losses'] += 1
        
        # Record game in history
        game_record = {
            'date': datetime.now().isoformat(),
            'players': players_involved,
            'winner': winner,
            'total_moves': self.stats['total_moves']
        }
        self.stats['games'].append(game_record)
        
        self.save_stats()
    
    def get_leaderboard(self, limit=10):
        """Get top players leaderboard"""
        players = []
        for username, stats in self.stats['players'].items():
            win_rate = 0
            if stats['games_participated'] > 0:
                win_rate = (stats['wins'] + 0.5 * stats['draws']) / stats['games_participated']
            
            player_data = {
                'username': username,
                'score': stats['total_score'],
                'wins': stats['wins'],
                'losses': stats['losses'],
                'draws': stats['draws'],
                'games': stats['games_participated'],
                'moves': stats['moves_played'],
                'win_rate': win_rate,
                'brilliant_moves': stats['brilliant_moves'],
                'blunders': stats['blunders'],
                'last_active': stats['last_active']
            }
            players.append(player_data)
        
        # Sort by score, then by win rate
        players.sort(key=lambda x: (x['score'], x['win_rate']), reverse=True)
        return players[:limit]



    # def get_leaderboard(self, limit=10):
    #     """Get top players leaderboard sorted by score and win rate"""
    #     players = []

    #     for username, stats in self.stats['players'].items():
    #         win_rate = 0
    #         if stats['games_participated'] > 0:
    #             win_rate = (stats['wins'] + 0.5 * stats['draws']) / stats['games_participated']

    #         player_data = {
    #             'username': username,
    #             'score': stats['total_score'],
    #             'wins': stats['wins'],
    #             'losses': stats['losses'],
    #             'draws': stats['draws'],
    #             'games': stats['games_participated'],
    #             'moves': stats['moves_played'],
    #             'win_rate': win_rate,
    #             'brilliant_moves': stats['brilliant_moves'],
    #             'blunders': stats['blunders'],
    #             'last_active': stats['last_active']
    #         }
    #         players.append(player_data)

    #     # ✅ Sort and limit (this was missing!)
    #     players.sort(key=lambda p: (p['score'], p['win_rate']), reverse=True)
    #     return players[:limit]




    
    def get_player_achievements(self, player):
        """Get achievements for a specific player"""
        if player not in self.stats['players']:
            return []
        
        stats = self.stats['players'][player]
        achievements = []
        
        # Move-based achievements
        if stats['moves_played'] >= 100:
            achievements.append("🏃 Century Player - 100+ moves")
        if stats['moves_played'] >= 500:
            achievements.append("⚡ Speed Demon - 500+ moves")
        if stats['moves_played'] >= 1000:
            achievements.append("🚀 Chess Master - 1000+ moves")
        
        # Game-based achievements
        if stats['games_participated'] >= 10:
            achievements.append("🎯 Regular Player - 10+ games")
        if stats['games_participated'] >= 50:
            achievements.append("🏆 Chess Veteran - 50+ games")
        
        # Skill-based achievements
        if stats['brilliant_moves'] >= 5:
            achievements.append("💎 Brilliant Tactician - 5+ brilliant moves")
        if stats['wins'] >= 5:
            achievements.append("👑 Winner - 5+ victories")
        if stats['wins'] >= 10:
            achievements.append("🏅 Champion - 10+ victories")
        
        # Special achievements
        win_rate = 0
        if stats['games_participated'] > 0:
            win_rate = (stats['wins'] + 0.5 * stats['draws']) / stats['games_participated']
        
        if win_rate >= 0.7 and stats['games_participated'] >= 5:
            achievements.append("⭐ High Performer - 70%+ win rate")
        if win_rate >= 0.9 and stats['games_participated'] >= 10:
            achievements.append("🌟 Chess Prodigy - 90%+ win rate")
        
        return achievements
    
    def analyze_move_quality(self, board, move_san):
        """Analyze move quality (basic implementation)"""
        # This is a simplified analysis - in production you'd use an engine
        try:
            move = board.parse_san(move_san)
            
            # Check if it's a capture of high-value piece
            if board.is_capture(move):
                captured = board.piece_at(move.to_square)
                if captured and captured.symbol().lower() in ['q', 'r']:
                    return "brilliant"
            
            # Check if it gives check
            board.push(move)
            is_check = board.is_check()
            is_checkmate = board.is_checkmate()
            board.pop()
            
            if is_checkmate:
                return "brilliant"
            elif is_check:
                return "good"
            
            return "normal"
            
        except Exception:
            return "normal"
    
    def get_opening_stats(self, player):
        """Get opening statistics for a player"""
        if player not in self.stats['players']:
            return {}
        
        return self.stats['players'][player].get('favorite_openings', {})
    
    def record_opening(self, player, opening_name):
        """Record opening played by player"""
        if player not in self.stats['players']:
            self.record_move(player, "", "normal")
        
        openings = self.stats['players'][player].setdefault('favorite_openings', {})
        openings[opening_name] = openings.get(opening_name, 0) + 1
        self.save_stats()