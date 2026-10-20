"""COBOL program templates for parametrized synthetic generation.

Templates are Python format strings. Each produces a complete, compilable
COBOL-85 program with a single expected output line.
"""

# Simple display-only template (e.g. for testing)
DISPLAY_ONLY = """\
       IDENTIFICATION DIVISION.
       PROGRAM-ID. {program_id}.
       DATA DIVISION.
       WORKING-STORAGE SECTION.
       01 WS-MSG PIC X(80) VALUE '{message}'.
       PROCEDURE DIVISION.
           DISPLAY WS-MSG.
           STOP RUN.
"""

# Arithmetic template: computes A + B and displays the result.
ADDITION = """\
       IDENTIFICATION DIVISION.
       PROGRAM-ID. {program_id}.
       DATA DIVISION.
       WORKING-STORAGE SECTION.
       01 WS-A    PIC 9(5)V99 VALUE {a}.
       01 WS-B    PIC 9(5)V99 VALUE {b}.
       01 WS-SUM  PIC 9(6)V99 VALUE 0.
       01 WS-OUT  PIC X(80) VALUE SPACES.
       PROCEDURE DIVISION.
           COMPUTE WS-SUM = WS-A + WS-B.
           STRING
               '{label}'
               WS-SUM
               DELIMITED BY SIZE
               INTO WS-OUT
           END-STRING.
           DISPLAY FUNCTION TRIM(WS-OUT).
           STOP RUN.
"""

# Conditional template: displays one of two messages based on a comparison.
CONDITIONAL = """\
       IDENTIFICATION DIVISION.
       PROGRAM-ID. {program_id}.
       DATA DIVISION.
       WORKING-STORAGE SECTION.
       01 WS-VALUE PIC 9(5) VALUE {value}.
       01 WS-THRESH PIC 9(5) VALUE {threshold}.
       PROCEDURE DIVISION.
           IF WS-VALUE > WS-THRESH
               DISPLAY '{high_msg}'
           ELSE
               DISPLAY '{low_msg}'
           END-IF.
           STOP RUN.
"""

# Enterprise DB2 / EXEC SQL query template
EXEC_SQL = """\
       IDENTIFICATION DIVISION.
       PROGRAM-ID. {program_id}.
       DATA DIVISION.
       WORKING-STORAGE SECTION.
       01 WS-CUST-ID   PIC 9(8) VALUE {cust_id}.
       01 WS-BALANCE   PIC 9(7)V99 VALUE {balance}.
       01 SQLCODE      PIC S9(9) COMP VALUE 0.
       01 WS-OUT      PIC X(80) VALUE SPACES.
       PROCEDURE DIVISION.
      * EXEC SQL
      *     SELECT BALANCE INTO :WS-BALANCE
      *     FROM ACCOUNT_TABLE
      *     WHERE CUST_ID = :WS-CUST-ID
      * END-EXEC.
           COMPUTE WS-BALANCE = {balance}.
           STRING
               '{label}'
               WS-BALANCE
               DELIMITED BY SIZE
               INTO WS-OUT
           END-STRING.
           IF SQLCODE = 0
               DISPLAY FUNCTION TRIM(WS-OUT)
           ELSE
               DISPLAY 'SQL ERROR CODE: ' SQLCODE
           END-IF.
           STOP RUN.
"""

# Enterprise CICS Transaction template
EXEC_CICS = """\
       IDENTIFICATION DIVISION.
       PROGRAM-ID. {program_id}.
       DATA DIVISION.
       WORKING-STORAGE SECTION.
       01 WS-TRANS PIC X(4) VALUE '{trans_id}'.
       01 WS-USER  PIC X(8) VALUE '{user_id}'.
       01 WS-RESP  PIC S9(8) COMP VALUE 0.
       PROCEDURE DIVISION.
      * EXEC CICS
      *     SEND TEXT FROM(WS-TRANS)
      *     LENGTH(4)
      *     ERASE
      *     RESP(WS-RESP)
      * END-EXEC.
           DISPLAY '{label}' WS-TRANS ' U:' WS-USER.
           STOP RUN.
"""

# Enterprise VSAM KSDS File handling template
VSAM_FILE = """\
       IDENTIFICATION DIVISION.
       PROGRAM-ID. {program_id}.
       ENVIRONMENT DIVISION.
       INPUT-OUTPUT SECTION.
       FILE-CONTROL.
           SELECT VSAM-FILE ASSIGN TO {file_name}
           ORGANIZATION IS INDEXED
           ACCESS MODE IS DYNAMIC
           RECORD KEY IS VSAM-KEY
           FILE STATUS IS WS-FILE-STATUS.
       DATA DIVISION.
       FILE SECTION.
       FD  VSAM-FILE.
       01  VSAM-REC.
           05 VSAM-KEY   PIC X(10).
           05 VSAM-DATA  PIC X(70).
       WORKING-STORAGE SECTION.
       01 WS-FILE-STATUS PIC X(2) VALUE '00'.
       PROCEDURE DIVISION.
           DISPLAY '{label} VSAM STATUS: ' WS-FILE-STATUS.
           STOP RUN.
"""

# Copybook inclusion template
COPYBOOK_INCLUSION = """\
       IDENTIFICATION DIVISION.
       PROGRAM-ID. {program_id}.
       DATA DIVISION.
       WORKING-STORAGE SECTION.
           COPY {copybook_name}.
       01 WS-STATUS PIC X(10) VALUE '{status_val}'.
       PROCEDURE DIVISION.
           DISPLAY '{label}' WS-STATUS.
           STOP RUN.
"""