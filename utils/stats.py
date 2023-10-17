import asqlite

from typing import Literal, TypedDict, Optional

GAMBLING_CHECK = """
                INSERT INTO GAMBLING (id, games_played, games_won, games_lost, amnt_played, amnt_won, amnt_lost) VALUES (?, 0, 0, 0, 0, 0, 0)
                ON CONFLICT(id) DO NOTHING;
                """

class UserStats(TypedDict):
    games_played: int
    games_won: int
    games_lost: int
    amnt_played: int
    amnt_won: int
    amnt_lost: int

class Stats:
    def __init__(self, database_file="./databases/stats.db") -> None:
        self.database_file = database_file

    async def create_tables(self) -> None:
        async with asqlite.connect(self.database_file) as conn:
            await conn.execute(
                """
                CREATE TABLE IF NOT EXISTS GAMBLING (
                    ID INT PRIMARY KEY,
                    GAMES_PLAYED INT,
                    GAMES_WON INT,
                    GAMES_LOST INT,
                    AMNT_PLAYED INT,
                    AMNT_WON INT,
                    AMNT_LOST INT
                )"""
            )
            await conn.commit()
        
    async def update_gambling(
            self,
            user_id: int,
            amnt: int,
            change: int,
            result: Literal["win", "loss"]
    ) -> None:
        async with asqlite.connect(self.database_file) as conn:
            if result == "win":
                query = """
                        GAMES_WON = GAMES_WON + 1,
                        AMNT_WON = AMNT_WON + ?
                        """
            else:
                query = """
                        GAMES_LOST = GAMES_LOST + 1,
                        AMNT_LOST = AMNT_LOST + ?
                        """
            await conn.execute(GAMBLING_CHECK, (user_id,))
            await conn.execute(
                f"""
                UPDATE GAMBLING
                SET GAMES_PLAYED = GAMES_PLAYED + 1,
                    AMNT_PLAYED = AMNT_PLAYED + ?,
                    {query}
                WHERE id = ?;
                """,
                (amnt, change, user_id)
            )
            
            await conn.commit()

    async def get_stats(
            self,
            user_id: int,
    ) -> Optional[UserStats]:
        async with asqlite.connect(self.database_file) as conn:
            await conn.execute(GAMBLING_CHECK, (user_id,))
            query = await conn.execute("SELECT * FROM GAMBLING WHERE id = ?", (user_id,))
            stats = await query.fetchone()
            if stats[1] == 0:
                return None
            return {
                "games_played": stats[1],
                "games_won": stats[2],
                "games_lost": stats[3],
                "amnt_played": stats[4],
                "amnt_won": stats[5],
                "amnt_lost": stats[6]
                }
            