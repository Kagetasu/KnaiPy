import asqlite

from typing import Literal

USER_CHECK = """
            INSERT INTO ECONOMY (id, balance) VALUES (?, 0)
            ON CONFLICT(id) DO
            """

class Database:
    def __init__(self, database_file="./databases/economy.db") -> None:
        self.database_file = database_file

    async def create_user(self, user_id: int, bal: int = 0):
        async with asqlite.connect(self.database_file) as conn:
            await conn.execute(
                "INSERT INTO ECONOMY (ID, BALANCE) VALUES (? ,?)", (user_id, bal)
            )
            await conn.commit()

    async def create_tables(self) -> None:
        async with asqlite.connect(self.database_file) as conn:
            await conn.execute(
                """
                CREATE TABLE IF NOT EXISTS ECONOMY (
                    ID INT PRIMARY KEY NOT NULL,
                    BALANCE INT NOT NULL
                );
                """
            )
            await conn.commit()

    async def update(
            self,
            user_id: int,
            mode: Literal["set", "+", "-"],
            amnt: int
    ) -> None:
        async with asqlite.connect(self.database_file) as conn:
            if mode == "set":
                query = "UPDATE set BALANCE = ? where ID = ?;"
            elif mode == "+":
                query = "UPDATE set BALANCE = BALANCE + ? where ID = ?;"
            elif mode == "-":
                query = "UPDATE set BALANCE = BALANCE - ? where ID = ?;"
            else:
                raise RuntimeError(f"Expected `set`, `+` or `-` but received {mode}")
            
            await conn.execute(USER_CHECK+query, (user_id, amnt, user_id))

            await conn.commit()

    async def delete_user(self, user_id: int):
        async with asqlite.connect(self.database_file) as conn:
            await conn.execute("DELETE from ECONOMY where ID = ?;", (user_id,))
            await conn.commit()

    async def get_balance(self, user_id: int) -> int:
        async with asqlite.connect(self.database_file) as conn:
            query = await conn.execute(
                    USER_CHECK+
                        """
                        UPDATE SET balance = balance
                        RETURNING balance
                    """,
                (user_id)
            )
            
            user = await query.fetchone()
            return user[0]
    
    