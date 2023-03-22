create_table_status = '''CREATE TABLE user_status (
                  ID INTEGER PRIMARY KEY AUTOINCREMENT,
                  STATUS INT NOT NULL,
                  DS_STATUS VARCHAR(255) NOT NULL
                  );'''

create_table_users = '''CREATE TABLE users (
                  ID INTEGER PRIMARY KEY AUTOINCREMENT,
                  USER_ID INT NOT NULL,
                  USER_NAME VARCHAR(255),
                  ULTIMA_ATUALIZACAO timestamp,
                  STATUS INT NOT NULL,
                  FOREIGN KEY(STATUS) REFERENCES user_status(STATUS)
                  );'''

index_status = "CREATE INDEX index_status ON users (STATUS);"
index_user_id = "CREATE INDEX index_user_id ON users (USER_ID);"

drop_table_user_status = "drop table user_status;"
drop_table_users = "drop table users;"

status = [
            (1, "WAITING TO FOLLOW"),
            (2, "FOLLOWING"),
            (3, "UNFOLLOWED")
         ]

# list_users = []
# for i in followers:
#     username = bot.get_username_from_user_id(i)
#     user = (i, username, datetime.now(), 2)
#     print(user)
#     list_users.append(user)
# db_followers.insert_many_users(list_users)