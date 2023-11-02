import sqlite3

class UserStoryDB:
    
    def __init__(self) -> None:
        self.__con = sqlite3.connect('userstories.db')
        self.__cur = self.__con.cursor()
        self.__create_table()

    def __create_table(self) -> None:
        self.__cur.execute('''CREATE TABLE IF NOT EXISTS userstories(
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            from_user STRING  NOT NULL,
            title STRING  NOT NULL,
            decs STRING  NOT NULL
        )''')

        self.__con.commit()

    def drop_table(self) -> None:
        self.__cur.execute('DROP TABLE userstories')
        self.__con.commit()

    def add_userstory(self, from_user, title, decs) -> None:
        self.__cur.execute('INSERT INTO userstories (from_user, title, decs) VALUES (?, ?, ?)', (from_user, title, decs))
        self.__con.commit()

    def get_userstory(self) -> str:
        self.__cur.execute('SELECT * from userstories')

        text_res = ''
        for res in self.__cur.fetchall():
            text_res += res[2] + '\n' + res[3] + '\n\n'

        return text_res
        
    def __del__(self) -> None:
        self.__cur.close()
        self.__con.close()