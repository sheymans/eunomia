import cmd
from eunomia.parser import Parser
from timer import Timer
import os

class Eis(cmd.Cmd):
    """Eunomia Interactive Shell -- EIS"""

    prompt = "(eis) "
    intro = "Eis Interactive Shell - (C) Stijn Heymans, 2014\nType 'help' for an overview of commands. Ctrl-D exits."

    # Store the current Program
    program = None
    # To time stuff
    time = Timer()

    # Possible options for SHOW command
    show_options = [ 'loaded', 'inferences' ]

    ## Loading files as programs:

    def do_load(self, filename):
        """load [file]
        Load the program that you want to use."""
        with self.time:
            if filename:
                if os.path.isfile(filename):
                    with open(filename, 'rU') as f:
                        text = f.read()
                        parser = Parser()
                        self.program = parser.parse(text) 
                        print "==> program loaded."
                else:
                    print filename, " does not seem to exist."
            else:
                print "What file should I load?"

    ## Showing what Eunomia knows:

    def do_show(self, what):
        """show [option]
        Show what Eunomia currently knows.
        \nFor example, 'show loaded' shows the currently loaded program. """
        if what:
            if what == "loaded":
                print self.program
            elif what == "inferences":
                if not self.engine:
                    print "You did not ask to deduce what I know. Try 'build'."
                else:
                    facts = self.engine.get_all_facts()
                    print facts
                    print "\n"
                    print "==> ", len(facts), " facts currently known."
            else:
                print "I don't know what to show. Use <TAB> to see options."
        else:
            print "Show what? Use <TAB> to see options."

    def complete_show(self, text, line, begidx, endidx):
        if not text:
            completions = self.show_options[:]
        else:
            completions = [ f
                            for f in self.show_options
                            if f.startswith(text)
                            ]
        return completions

    ## Inferring all you can:

    def do_build(self):
        """build
        Given the currently loaded program (rules and facts) infer all facts you can.
        """
        with self.time:
            print "Building model..."
            self.engine = Engine()
            print "==> Model built (do 'show inferences' to see all known facts)"




    def do_EOF(self, line):
        return True
    
    def postloop(self):
        print

if __name__ == '__main__':
    Eis().cmdloop()

