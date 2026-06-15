import pymysql

class BoardDAO:
    def __init__(self):

        self.host = "localhost"
        self.user = "board_user"
        self.password = "board1234"
        self.database = "board_db"

    def get_connection(self):

        return pymysql.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
            charset="utf8mb4"
        )

    def select_all(self):
        """1. 목록 보기: 번호, 제목, 작성자, 작성일 추출 (num 기준으로 정렬)"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
       
        sql = "SELECT num, title, writer, DATE_FORMAT(created_at, '%%Y-%%m-%%d') FROM board ORDER BY num DESC"
        cursor.execute(sql)
        rows = cursor.fetchall()
        
        cursor.close()
        conn.close()
        return rows

    def insert_board(self, title, content, writer, password):
        """2. 글 등록: 비밀번호를 포함하여 저장 (총 4개 인자받음)"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
       
        sql = "INSERT INTO board (title, content, writer, password) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (title, content, writer, password))
        
        conn.commit()
        cursor.close()
        conn.close()

    def select_one(self, num):
        """3. 내용 보기: 특정 게시글 상세 조회"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        
        sql = """
            SELECT num, title, content, writer, 
                   DATE_FORMAT(created_at, '%%Y-%%m-%%d %%H:%%i'), likes 
            FROM board 
            WHERE num = %s
        """
        cursor.execute(sql, (num,))
        row = cursor.fetchone()
        
        cursor.close()
        conn.close()
        return row

    def delete_board(self, num, password):
        """4. 글 삭제: 비밀번호 검증 후 삭제 성공 여부(True/False) 반환"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        
        sql_check = "SELECT password FROM board WHERE num = %s"
        cursor.execute(sql_check, (num,))
        row = cursor.fetchone()
        
        success = False
        if row and row[0] == password:
            sql_delete = "DELETE FROM board WHERE num = %s"
            cursor.execute(sql_delete, (num,))
            conn.commit()
            success = True
            
        cursor.close()
        conn.close()
        return success

    def increase_like(self, num):
        """5. 좋아요 증가: 해당 번호의 좋아요 수 1 올림"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        
        sql = "UPDATE board SET likes = likes + 1 WHERE num = %s"
        cursor.execute(sql, (num,))
        
        conn.commit()
        cursor.close()
        conn.close()