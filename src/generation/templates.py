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