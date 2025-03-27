#----------------------------------------------------------------------------
# Connects to a Hex program.
#----------------------------------------------------------------------------

import os, string, sys, subprocess
from random import randrange
from select import select

#----------------------------------------------------------------------------

class Program:
    class CommandDenied(Exception):
        pass

    class Died(Exception):
        pass

    def __init__(self, color, command, logName, verbose):
        command = command.replace("%SRAND", repr(randrange(0, 1000000)))
        self._command = command
        self._color = color
        self._verbose = verbose
        if self._verbose:
            print(("Creating program:", command))
        p = subprocess.Popen(command, shell=True,
                             stdin=subprocess.PIPE, 
                             stdout=subprocess.PIPE, 
                             stderr=subprocess.PIPE)
        (self._stdin, 
         self._stdout, 
         self._stderr) = (p.stdin, p.stdout, p.stderr)
        self._isDead = 0
        self._log = open(logName, "w")
        self._log.write("# " + self._command + "\n")

    def getColor(self):
        return self._color

    def getCommand(self):
        return self._command

    def getDenyReason(self):
        return self._denyReason

    def getName(self):
        name = "?"
        try:
            name = self.sendCommand("name").strip()
            version = self.sendCommand("version").strip()
            name += " " + version
        except Program.CommandDenied:
            pass
        return name

    def getResult(self):
        try:
            l = self.sendCommand("final_score")
            #s = string.split(l)[0]
            #return s
            return l.strip()
        except Program.CommandDenied:
            return "?"

    def getTimeRemaining(self):
        try:
            l = self.sendCommand("time_left");
            return l.strip();
        except Program.CommandDenied:
            return "?"

    def isDead(self):
        return self._isDead

    def sendCommand(self, cmd):
        try:
            self._log.write(">" + cmd + "\n")
            if self._verbose:
                print((self._color + "< " + cmd))

            #print(f"Sending command: {cmd}")  # Debugging output

            self._stdin.write((cmd + "\n" ).encode("utf-8"))
            self._stdin.flush()
            #line = self._stdout.readline()
            #self._stdout.flush()
            #print(f"the output is: {repr(line)}")
            #line = line.decode("utf-8")
            #print(f"the output (deocded) is: {repr(line)}")
            return self._getAnswer()
        except IOError:
            self._programDied()

    def _getAnswer(self):
        self._logStdErr()
        answer = ""
        done = 0
        numberLines = 0
        while not done:
            line = self._stdout.readline().decode("utf-8")
            #print("hi")
            #print(f"the output is: {repr(line)}")
            #self._programDied()
            if line == "":
                self._programDied()
            self._log.write("<" + line)
            if self._verbose:
                sys.stdout.write(self._color + "> " + line)
            numberLines += 1
            done = (line == "\n")
            if not done:
                answer += line
       # if answer.lower().replace(" ","").find("winnerwhite") != -1:
       #     return "resign"
       # if answer.lower().replace(" ","").find("winnerblack") != -1:
       #     return "resign"
        if answer[0] != '=':
            self._denyReason = answer[2:].strip()
            raise Program.CommandDenied
        if numberLines == 1:
            return answer[1:].strip()
        
        return answer[2:]

    def _logStdErr(self):
        list = select([self._stderr], [], [], 0)[0]
        for s in list:
            self._log.write(os.read(s.fileno(), 8192).decode("utf-8"))
        self._log.flush()

    def _programDied(self):
        self._isDead = 1
        self._logStdErr()
        raise Program.Died
    


bcmd = ''
command_suffix = ''
bLogName = "/home/linus/MoHex2.0/benzene-vanilla-cmake-master/benzene-vanilla-cmake-master/tournament/jobs/wawa.log"

wLogName = ''
optimized_settings = [
    "param_mohex max_memory 2000000000",
    "param_mohex max_games 999999",
    "param_mohex max_time  999999",
    "param_mohex use_time_management 1",
    "param_game  game_time 180",
    "param_mohex num_threads 4",
    "param_mohex virtual_loss 1",
    "param_mohex reuse_subtree 1"]

# (fixed) opponent program

# GTP commands sent to the opponent program before starting
opponent_settings = [
    "param_mohex max_memory 2000000000",
    "param_mohex max_games 999999",
    "param_mohex max_time  999999",
    "param_mohex use_time_management 1",
    "param_game  game_time 180",
    "param_mohex num_threads 4",
    "param_mohex virtual_loss 1",
    "param_mohex reuse_subtree 1"]
verbose = True
optimized_program = '/home/linus/MoHex2.0/benzene-vanilla-cmake-master/benzene-vanilla-cmake-master/build/src/mohex/mohex' #this has done something big
opponent_program = '/local/scratch/broderic/hex/benzene-local/benzene/src/mohex/mohex.jun20'
optcmd = optimized_program + " --seed %SRAND --use-logfile=false"
oppcmd = opponent_program  + " --seed %SRAND --use-logfile=false"


bcmd = optcmd

bsettings = optimized_settings
wcmd = oppcmd

wsettings = opponent_settings

if __name__ =="__main__":
    black = Program("B", bcmd, bLogName, verbose)
    size=11
    black.sendCommand("boardsize " + repr(size) + " " + repr(size))
    black.sendCommand("genmove b")



