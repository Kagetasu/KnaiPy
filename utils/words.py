import asqlite

import aiofiles

class Words:
    def __init__(self, database_file="./databases/words.db") -> None:
        self.database_file = database_file

    async def create_tables(self) -> None:
        async with asqlite.connect(self.database_file) as conn:
            await conn.execute(
                """
                CREATE TABLE IF NOT EXISTS words(
                    word TEXT PRIMARY KEY
                );
                """
            )
            await conn.commit()

    async def filter_words(self) -> None:
        parsed = []
        
        async with aiofiles.open('WORD.LST', mode='r') as f:
            async for line in f:
                line = line.strip()
                if len(line) == 5:
                    parsed.append(line)

        async with asqlite.connect(self.database_file) as conn:
            await conn.executemany("INSERT INTO words VALUES (?)", [(word,) for word in parsed])
            await conn.commit()

    async def get_random(self) -> None:
        async with asqlite.connect(self.database_file) as conn:
            word = await conn.execute("SELECT word FROM words ORDER BY RANDOM() LIMIT 1;")
            word = await word.fetchone()
        return word[0]