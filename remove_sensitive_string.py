import sys

DB_URL_STARTSWITH = "localhost"
DB_USER_STARTSWITH = "root"
DB_PASSWORD_STARTSWITH = "123456"
DB_DATABASE_STARTSWITH = "week"

DB_SENSITIVE_STRINGS = [DB_URL_STARTSWITH, DB_USER_STARTSWITH, DB_PASSWORD_STARTSWITH, DB_DATABASE_STARTSWITH]

for line in sys.stdin:
    for sensitive_string in DB_SENSITIVE_STRINGS:
        if line.startswith(sensitive_string):
            line = line[:len(sensitive_string)] + "\"\"\n"
            break
    sys.stdout.write(line)