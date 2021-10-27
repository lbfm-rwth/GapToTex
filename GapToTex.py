import sys
import os
from subprocess import Popen, PIPE, STDOUT
import errno
import signal
import functools
import time

# ----------------- #
# Global Parameters #
# ----------------- #

# https://stackoverflow.com/questions/287871/how-to-print-colored-text-to-the-terminal
class bcolors:
    FAIL = '\033[91m'
    ENDC = '\033[0m'

# optional argument GAP path
GAP = '/bin/gap.sh'
if sys.argv[1:]:
    GAP = sys.argv[1]

# Delay after starting GAP, in sec
DELAY = 10
# Timeout for trying to read a line after a successful read, in sec
TIMEOUT = 0.2
# Memory for GAP session
MEMORY = '3G'
# Input directory
IN = 'in'
# Output directory
OUT = 'out'
# Temporary files
TMPFILE = '%s/%s' % (OUT, 'tmp.txt')
DUMPFILE = '%s/%s' % (OUT, 'dump.txt')

if not os.path.exists(OUT):
    os.mkdir(OUT)

# -------------- #
# Timeout Helper #
# -------------- #

class TimeoutError(Exception):
    pass

# https://stackoverflow.com/questions/2281850/timeout-function-if-it-takes-too-long-to-finish?noredirect=1&lq=1
def timeout(time=10, error_message=os.strerror(errno.ETIME)):
    def decorator(func):
        def _handle_timeout(signum, frame):
            raise TimeoutError(error_message)

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.setitimer(signal.ITIMER_REAL, time)
            try:
                result = func(*args, **kwargs)
            finally:
                signal.setitimer(signal.ITIMER_REAL, 0)
            return result

        return wrapper

    return decorator

# ---------------------- #
# Write and Read Helpers #
# ---------------------- #

def writeline(stdin, line):
    stdin.write(line)
    stdin.flush()

# Try to read new lines until TIMEOUT is detected for a single line.
# Blocks all subsequent code while running.
def readlines(stdout, outfile):
    # read first line definitely
    readline(stdout, outfile)
    # try to read more lines
    try:
        while True:
            readlineWithTimeout(stdout, outfile)
    except TimeoutError as exc:
        pass

def readline(stdout, outfile):
    outfile.write(stdout.readline())

@timeout(TIMEOUT)
def readlineWithTimeout(stdout, outfile):
    return readline(stdout, outfile)

###################
 # ------------- #
 # Main Function #
 # ------------- #
###################

for FILE in [f for f in os.listdir(IN) if os.path.isfile(os.path.join(IN, f))] :

    # Declare input and output files
    GAPFILE = '%s/%s' % (IN, FILE)
    LATEXFILE = '%s/%s' % (OUT, FILE.split('.')[0]+'.tex')

    # Start GAP
    proc = Popen([GAP, '-q', '-o', MEMORY], stdin=PIPE, stdout=PIPE, stderr=STDOUT,encoding='utf8')

    # For some reason, the first command outputs an additional empty line at the beginning
    with open(DUMPFILE, mode='w') as dumpfile:
        writeline(proc.stdin, '"Run GAP file";\n')
        # Some people might configure GAP to load additional packages etc.
        # which might produce additional output on startup.
        time.sleep(DELAY)
        readlines(proc.stdout, dumpfile)

    # Main communication with GAP
    with open(GAPFILE, mode='r') as infile, open(TMPFILE, mode='a') as outfile:
        inline = ''
        for line in infile:
            # Last line may not contain a linebreak
            if line[-1] != '\n':
                line += '\n'
            inline += line
            # Empty or Comment
            if inline[0] == '\n' or inline[0] == '#':
                outfile.write(inline)
                inline = ''
            # Command
            elif inline[-2] == ';':
                # Split line into chunks
                inchunks = [chunk+'\n' for chunk in inline.split('\n') if chunk]
                # Write GAP input
                outfile.write('gap> %s' % inchunks[0])
                for i in range(1, len(inchunks)):
                    outfile.write('> %s' % inchunks[i])

                # Execute GAP input
                writeline(proc.stdin, inline)
                # Write GAP output
                if inline[-3] != ';':
                    readlines(proc.stdout, outfile)

                inline = ''

    # Start GAP with large terminal
    proc = Popen([GAP, '-q', '-o', MEMORY, '-x', '120'], stdin=PIPE, stdout=PIPE, stderr=STDOUT,encoding='utf8')

    # Create LaTeX file with GAPDoc
    writeline(proc.stdin, 'r := rec(content := ReadAll(InputTextFile("%s")), name := "Example");;\n' % TMPFILE)
    writeline(proc.stdin, 'str := "";;\n')
    writeline(proc.stdin, 'GAPDoc2LaTeXProcs.Example(r, str);;\n')
    writeline(proc.stdin, 'PrintTo("%s", str);;\n' % LATEXFILE)

    # Wait for GAP to finish before proceeding
    with open(DUMPFILE, mode='w') as dumpfile:
        writeline(proc.stdin, '"Close GAP file";\n')
        # Some people might configure GAP to load additional packages etc.
        # which might produce additional output on startup.
        time.sleep(DELAY)
        readline(proc.stdout, dumpfile)

# -------- #
# Clean Up #
# -------- #

if os.path.exists(TMPFILE):
    os.remove(TMPFILE)

if os.path.exists(DUMPFILE):
    os.remove(DUMPFILE)
