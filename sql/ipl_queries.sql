-- 1. Total matches and seasons
SELECT season, COUNT(*) AS matches_played
FROM matches_clean
GROUP BY season
ORDER BY season;

-- 2. Team-wise total wins across all seasons
SELECT winner AS team, COUNT(*) AS wins
FROM matches_clean
WHERE winner IS NOT NULL
GROUP BY winner
ORDER BY wins DESC;

-- 3. Win rate after winning toss
WITH toss_summary AS (
    SELECT toss_winner,
           COUNT(*) AS tosses_won,
           SUM(CASE WHEN toss_winner = winner THEN 1 ELSE 0 END) AS matches_won_after_toss
    FROM matches_clean
    WHERE toss_winner IS NOT NULL
    GROUP BY toss_winner
)
SELECT toss_winner AS team,
       tosses_won,
       matches_won_after_toss,
       ROUND((matches_won_after_toss * 100.0) / tosses_won, 2) AS toss_to_match_win_pct
FROM toss_summary
ORDER BY toss_to_match_win_pct DESC;

-- 4. Top players of the match award winners
SELECT player_of_match, COUNT(*) AS awards
FROM matches_clean
WHERE player_of_match IS NOT NULL
GROUP BY player_of_match
ORDER BY awards DESC
LIMIT 10;

-- 5. Stadiums with the highest average first-innings totals
WITH first_innings AS (
    SELECT m.venue, d.match_id, SUM(d.total_runs) AS total_runs
    FROM deliveries_clean d
    JOIN matches_clean m ON m.id = d.match_id
    WHERE d.inning = 1
    GROUP BY m.venue, d.match_id
)
SELECT venue, ROUND(AVG(total_runs), 2) AS avg_first_innings_score
FROM first_innings
GROUP BY venue
ORDER BY avg_first_innings_score DESC
LIMIT 10;

-- 6. Most common dismissal kind in IPL
SELECT dismissal_kind, COUNT(*) AS dismissals
FROM deliveries_clean
WHERE dismissal_kind IS NOT NULL AND dismissal_kind <> 'NA'
GROUP BY dismissal_kind
ORDER BY dismissals DESC;

-- 7. Top teams by average runs scored per match
WITH team_scores AS (
    SELECT batting_team, match_id, SUM(total_runs) AS team_total_runs
    FROM deliveries_clean
    GROUP BY batting_team, match_id
)
SELECT batting_team AS team,
       ROUND(AVG(team_total_runs), 2) AS avg_runs_per_match
FROM team_scores
GROUP BY batting_team
ORDER BY avg_runs_per_match DESC;

-- 8. Match result breakdown by type
SELECT result, COUNT(*) AS matches
FROM matches_clean
GROUP BY result
ORDER BY matches DESC;
