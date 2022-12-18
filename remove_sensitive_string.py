import sys

DB_URL_STARTSWITH = "MySQL_URL ="
DB_USER_STARTSWITH = "MySQL_USER ="
DB_PASSWORD_STARTSWITH = "MySQL_PWD ="
DB_DATABASE_STARTSWITH = "MySQL_DATABASE ="

DB_SENSITIVE_STRINGS = [DB_URL_STARTSWITH, DB_USER_STARTSWITH, DB_PASSWORD_STARTSWITH, DB_DATABASE_STARTSWITH]

for line in sys.stdin:
    for sensitive_string in DB_SENSITIVE_STRINGS:
        if line.startswith(sensitive_string):
            line = line[:len(sensitive_string)] + "\"\"\n"
            break
    sys.stdout.write(line)