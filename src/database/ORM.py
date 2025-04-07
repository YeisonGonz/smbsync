from src.database.DatabaseConnection import DatabaseConnection

class ORM:
    def __init__(self):
        self.conn = DatabaseConnection().get_connection()
        self.cursor = self.conn.cursor()

    def add_user(self, name: str, password: str, host_connection: str) -> int:
        """Agrega un nuevo usuario samba a la base de datos.

        Returns:
            int: ID del nuevo usuario insertado.
        """
        self.cursor.execute(
            """
            INSERT INTO samba_user (name, password, host_connection)
            VALUES (?, ?, ?)
            """,
            (name, password, host_connection)
        )
        self.conn.commit()
        return 0

    def prune_users(self):
        try:
            self.cursor.execute("DELETE FROM samba_user")
            self.conn.commit()
            print("Todos los usuarios han sido eliminados.")
        except Exception as e:
            print(f"Error al eliminar usuarios: {e}")

    def get_all_users(self) -> list[dict]:
        self.cursor.execute("SELECT * FROM samba_user")
        rows = self.cursor.fetchall()
        return [dict(row) for row in rows]

    def get_first_user(self) -> dict:
        self.cursor.execute("SELECT * FROM samba_user LIMIT 1")
        rows = self.cursor.fetchall()
        return [dict(row) for row in rows]