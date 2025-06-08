# ♟️ Interactive Chess Game

Welcome to my GitHub profile chess game! Challenge a competitive AI opponent by opening a GitHub Issue.

## 🏁 Current Game Status

⚪ **White to move**

**Game Status:** White to move  
**Total Moves:** 2  
**Last Moves:** 1. d3 d5

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


## 🏆 Leaderboard

| Rank | Player | Score | W/L/D | Win Rate | Moves |
|------|--------|-------|-------|----------|-------|
| 1 | AI | 16 | 0/0/0 | 0% | 16 |
| 2 | Player1 | 10 | 0/0/0 | 0% | 10 |
| 3 | TestPlayer1 | 4 | 0/2/0 | 0% | 4 |
| 4 | TestPlayer2 | 4 | 0/2/0 | 0% | 4 |
| 5 | Verma-MK | 1 | 0/0/0 | 0% | 1 |

## 🎖️ Recent Achievements


## 📈 Game Statistics

- **Total Games Played**: 2
- **AI Win Rate**: 100.0% (2 wins)
- **Player Victories**: 0
- **Draws**: 0
- **Total Moves**: 36


## 📊 Game Information

- **Current FEN**: `rnbqkbnr/ppp2ppp/8/3pp3/4P3/3P4/PPP2PPP/RNBQKBNR w KQkq - 0 3`
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
