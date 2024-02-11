# Models

## Relationships

Notation key

- \<Class>
- \[list of objects]
- $foreignkey
- #backref assigned

One-to-many

```txt
<Tournament> [games]
├─ <Game> $tournament_id, #tournament
<User> [games_officiated]
├─ <Game> $referee_id, #referee
<User> [games_entered]
├─ <Game> $entered_by_id
<Tournament> [awards]
├─ <Award> $tournament_id
```

player1_id, player2_id, and [games_played] are unlinked.

Many-to-many

```txt
<Tournament> [players], [referees]
├─ <User> #[tournaments_played]
├─ <User> #[tournaments_officiated]
<User> [awards]
│  ├─ <Award> #[awardees]
<User> [games_played]
│  ├─ <Game> #[players]
```

### User

- List of games they played in
- List of games they officiated

### Game

- Player 1
- Player 2
- Referee
- Who entered
- Tournament

### Tournament

- List of players
- List of referees
- List of games
- List of awards given

### Award

- Awardee
- Tournament
