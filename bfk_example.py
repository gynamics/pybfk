#!/usr/bin/python
from bfk import Brain, BrainDbgCli

i = Brain()  # create an instance
d = BrainDbgCli()  # create a debugger
d.attach(i)
i.fuck(     # put your code here
        """
        helloworld
        ++++++++++  set (0) to 10
        [           do
        >+++++++    inc (1) by 7
        >++++++++++ inc (2) by 10
        >+++        inc (3) by 3
        >+          inc (4) by 1
        <<<<-]      while dec (0)
        >++.        inc (1) by 2 output 'H'
        >+.         inc (2) by 1 output 'e'
        +++++++.    inc (2) by 7 output 'l'
        .                        output 'l'
        +++.        inc (2) by 3 output 'o'
        >++.        inc (3) by 2 output ' '
        <<+++++++++++++++.
                    inc (1) by 15 output 'W'
        >.              (2)      output 'o'
        +++.        add (2) by 3 output 'r'
        ------.     dec (2) by 6 output 'l'
        --------.   dec (2) by 8 output 'd'
        >+.         add (3) by 1 output '!'
        >.              (4)      output '\\n'
        """
)
