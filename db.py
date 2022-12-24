import sqlite3


class DB:
    def __init__(self, database_name: str):
        self.connection = sqlite3.connect(database_name)
        self.cursor = self.connection.cursor()

    def get_user_password_by_username(self, username: str):
        with self.connection:
            try:
                return self.cursor.execute(
                    "SELECT * FROM user WHERE username=?",
                    (username,)
                ).fetchone()
            except TypeError:
                print("TypeError")
            except Exception as e:
                print(e)

    def get_information_about_players(self):
        with self.connection:
            try:
                return self.cursor.execute(
                    "SELECT p.name_player, p.birthday_date, s.game_played,"
                    "       s.goal, s.assist, s.goal + s.assist AS point,"
                    "       s.penalty_minutes "
                    " FROM player AS p INNER JOIN statistic AS s ON p.player_id = s.player_id",
                ).fetchall()
            except TypeError:
                print("TypeError")
            except Exception as e:
                print(e)

    def get_top_fife_players(self):
        with self.connection:
            try:
                return self.cursor.execute(
                    "SELECT p.name_player, p.birthday_date, s.game_played,"
                    "       s.goal, s.assist, s.goal + s.assist AS point,"
                    "       s.penalty_minutes "
                    "FROM player AS p INNER JOIN statistic AS s ON p.player_id = s.player_id ORDER BY point DESC",
                ).fetchall()
            except TypeError:
                print("TypeError")
            except Exception as e:
                print(e)

    def add_new_player(self, player_name, player_birthday):
        with self.connection:
            try:
                return self.cursor.execute("INSERT INTO player(name_player, birthday_date) VALUES(?, ?);",
                                           (str(player_name), str(player_birthday)),
                                           )
            except TypeError:
                print("TypeError")
            except Exception as e:
                print(e)
            finally:
                self.connection.commit()

    def add_player_statistic(self, player_id, game, goal,
                             assist, penalty_minutes):
        with self.connection:
            try:
                return self.cursor.execute(
                    "INSERT INTO statistic(player_id, game_played, goal, assist, penalty_minutes)"
                    "     VALUES(?, ?, ?, ?, ?);",
                    (player_id, game, goal, assist, penalty_minutes),
                    )
            except TypeError:
                print("TypeError")
            except Exception as e:
                print(e)
            finally:
                self.connection.commit()

    def add_new_user(self, username, password, is_superuser):
        with self.connection:
            try:
                return self.cursor.execute("INSERT INTO user(username, password, is_superuser)"
                                           "     VALUES(?, ?, ?);",
                                           (username, password, bool(is_superuser)),
                                           )
            except TypeError:
                print("TypeError")
            except Exception as e:
                print(e)
            finally:
                self.connection.commit()

    def update_player(self, player_name, change_field, change_information):
        with self.connection:
            try:
                if change_field == 'name_player' or change_field == 'birthday_date':
                    query = f'''
                    UPDATE player 
                    SET {change_field} = ? 
                    WHERE name_player = ?'''
                else:
                    query = f'''
                        UPDATE statistic 
                        SET {change_field} = ? 
                        WHERE statistic.player_id = 
                        (SELECT player.player_id FROM player WHERE player.name_player = ?)'''
                return self.cursor.execute(query, (change_information, player_name)
                                           )
            except TypeError:
                print("TypeError")
            except Exception as e:
                print(e)
            finally:
                self.connection.commit()

    def delete_player(self, player_name):
        with self.connection:
            try:
                query = '''
                DELETE FROM player
                WHERE name_player = ?
                '''
                return self.cursor.execute(query, (str(player_name),)
                                           )
            except TypeError:
                print("TypeError")
            except Exception as e:
                print(e)
            finally:
                self.connection.commit()

    def get_sorting_player_list(self, params):
        connection = sqlite3.connect("ice-hockey_player.db")
        cursor = self.connection.cursor()
        with connection:
            try:
                if params == "Player Name":
                    return cursor.execute(
                        "SELECT p.name_player, p.birthday_date, s.game_played,"
                        "       s.goal, s.assist, s.goal + s.assist AS point,"
                        "       s.penalty_minutes "
                        "FROM player AS p INNER JOIN statistic AS s ON p.player_id = s.player_id ORDER BY name_player ",
                    ).fetchall()
                elif params == "Goals":
                    return cursor.execute(
                        "SELECT p.name_player, p.birthday_date, s.game_played,"
                        "       s.goal, s.assist, s.goal + s.assist AS point,"
                        "       s.penalty_minutes "
                        "FROM player AS p INNER JOIN statistic AS s ON p.player_id = s.player_id ORDER BY goal DESC",
                    ).fetchall()
                else:
                    return cursor.execute(
                        "SELECT p.name_player, p.birthday_date, s.game_played,"
                        "       s.goal, s.assist, s.goal + s.assist AS point,"
                        "       s.penalty_minutes "
                        "FROM player AS p INNER JOIN statistic AS s ON p.player_id = s.player_id ORDER BY game_played DESC",
                    ).fetchall()

            except TypeError:
                print("TypeError")
            except Exception as e:
                print(e)

    def get_player_by_name(self, player_name):
        with self.connection:
            try:
                return self.cursor.execute(
                    "SELECT p.name_player, p.birthday_date, s.game_played,"
                    "       s.goal, s.assist, s.goal + s.assist AS point,"
                    "       s.penalty_minutes "
                    "FROM player AS p INNER JOIN statistic AS s ON p.player_id = s.player_id WHERE p.name_player=?",
                    (player_name,)
                ).fetchone()

            except TypeError:
                print("TypeError")
            except Exception as e:
                print(e)

    def get_information_about_users(self):
        with self.connection:
            try:
                return self.cursor.execute(
                    "SELECT user_id, username, is_superuser"
                    " FROM user",
                ).fetchall()
            except TypeError:
                print("TypeError")
            except Exception as e:
                print(e)

    def delete_user(self, user_id):
        with self.connection:
            try:
                query = '''
                DELETE FROM user
                WHERE user_id = ?
                '''
                return self.cursor.execute(query, (str(user_id),)
                                           )
            except TypeError:
                print("TypeError")
            except Exception as e:
                print(e)
            finally:
                self.connection.commit()
