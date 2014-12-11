import cmd
from eunomia.parser import Parser
from eunomia.engine import Engine
import eunomia.utils
from timer import Timer
import os

class Eis(cmd.Cmd):
    """Eunomia Interactive Shell -- EIS"""

    prompt = "(eis) "
    intro = "Eunomia Interactive Shell - (C) Stijn Heymans, 2014\nType 'help' for an overview of commands. Ctrl-D exits."

    # Store the current Program
    program = None

    # The current engine
    engine = None

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
                self.program = eunomia.utils.load_program(filename)
                if self.program:
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
                    facts = self.engine.get_facts()
                    for f in facts:
                        print f
                    print "==> ", len(facts), "facts currently known."
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

    ## Adding rules or facts
    def do_add(self, what):
        """add [rule or fact]
        \nFor example 'add f(a,b).' for adding a fact or 'add p(?x, ?y) :- q(?y, ?x).' for a rule.
        """
        if what:
            try:
                p = Parser()
                new_program = p.parse(what)
                # Add it to the program and push it to the engine
                self.program.merge(new_program)
                
                # this pushes both facts and rules
                if self.engine:
                    with self.time:
                        self.engine.push_program(new_program)

                print "==> added ", new_program, " and updated known inferences."

            except Exception as e:
                print "I'm not able to add ", what, " Is it a well-formed fact or rule?\nDetails: ",  e
        else:
            print "I don't know what to add. Add a rule or fact."


    ## Doing queries

    def do_query(self, what):
        """query [atom]
        \nFor example 'query f(?x,b).' 
        """
        if what:
            try:
                p = Parser()
                new_program = p.parse(what)
                if len(new_program.facts) > 0:
                    atom = new_program.facts[0].head
                
                # this pushes both facts and rules
                if atom and self.engine:
                    with self.time:
                        facts = self.engine.get_matching_facts(atom)
                        for f in facts:
                            print f
                        print "==> ", len(facts), "facts match query ", atom
                else:
                    print "Do an actual query and do a build first."
 
            except Exception as e:
                print "I'm not able to query ", what, " Is it well-formed? ",  e
        else:
            print "I don't know what to query."


    ## Inferring all you can:

    def do_build(self, line):
        """build
        Given the currently loaded program (rules and facts) infer all facts you can.
        """
        with self.time:
            if not self.program:
                print "No program was loaded. Try 'load' first."
            else:
                print "Building model..."
                self.engine = Engine(self.program)
                print "==> Model built (do 'show inferences' to see all known facts)"

    def do_EOF(self, line):
        return True
    
    def postloop(self):
        print

if __name__ == '__main__':
    Eis().cmdloop()

