-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

\c tournament

create table players(	player_id serial, 
			player_name text, 
			wins integer,
			games_played integer);

create view rank as select player_id,player_name, wins, games_played from players order by wins DESC; 
			