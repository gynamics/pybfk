#!/usr/bin/python
'''bfk:
A naive implementation of brainfu*k, go:

    brain.fuck(",>[.>,]")

'''


class Brain:
    '''
    a minimal brainfu*k interpreter
    '''
    def __init__(self):
        self.array_p = [0]  # non-negative direction
        self.array_n = [0]  # negative direction
        self.array = self.array_p  # current array
        self.addrs = []  # stack
        self.code = ''  # code ptr
        self.ptr = 0  # pointer to array
        self.pch = 0  # pointer to character
        self.symtbl = {
            # call table for this interpreter
            '>': self.rsh,
            '<': self.lsh,
            '+': self.inc,
            '-': self.dec,
            ',': self.ldt,
            '.': self.ott,
            ']': self.jnz,
            '[': self.lab
        }

    def rsh(self):
        "brainfu*k primitive: right shift"
        self.ptr += 1
        if self.ptr == 0:
            self.array = self.array_p
        if self.ptr >= len(self.array):
            self.array.append(0)

    def lsh(self):
        "brainfu*k primitive: left shift"
        self.ptr -= 1
        if self.ptr == -1:
            self.array = self.array_n
        if abs(self.ptr) >= len(self.array):
            self.array.append(0)

    def inc(self):
        "brainfu*k primitive: increment byte"
        self.array[abs(self.ptr)] = (self.array[abs(self.ptr)]+1) % 256

    def dec(self):
        "brainfu*k primitive: decrement byte"
        self.array[abs(self.ptr)] = (self.array[abs(self.ptr)]+255) % 256

    def ldt(self):
        "brainfu*k primitive: load to"
        flag = True
        while flag:
            try:
                self.array[abs(self.ptr)] = input()
            except ValueError:
                print("Invalid, please try again")
            else:
                flag = False

    def ott(self):
        "brainfu*k primitive: output to"
        print(f'{self.array[abs(self.ptr)]:c}', end='')

    def jnz(self):
        "brainfu*k primitive: jump if not zero"
        if self.array[abs(self.ptr)] != 0:
            self.pch = self.addrs[-1]
        else:
            self.addrs.pop()

    def lab(self):
        "brainfu*k primitive: load address back"
        self.addrs.append(self.pch)

    def ign(self):
        "ignore that symbol and pass, this function is useful in debugging"

    def fuck(self, code):
        "interpret a string @code"
        self.code = code
        while self.pch < len(self.code):
            sym = self.code[self.pch]
            if sym in self.symtbl:
                self.symtbl[sym]()
            else:
                self.ign()
            self.pch += 1


class BrainDbgCore:
    '''
    debugger for class brain
    '''
    def __init__(self, brain=None):
        self.attached = False
        self.symtbl = {}
        self.brain = brain  # a bfk interpreter
        self.bplist = []  # breakpoint list
        self.trapcnt = -1   # trap counter
        self.trapflag = True  # trap flag

    def attach(self, brain):
        "attach to a brain instance"
        if brain is not None and isinstance(brain, Brain):
            self.brain = brain
            self.symtbl = self.brain.symtbl
            self.brain.symtbl = {}
            # function override out of class
            self.brain.ign = self.debug
            self.attached = True
        else:
            print('fu*k, that is not a brain!')

    def detach(self):
        "detach from a brain instance"
        if self.attached is True:
            self.brain.ign = self.debug
            self.brain.symtbl = self.symtbl
            self.attached = False

    def bpadd(self, ins):
        "add a breakpoint at ins[0]"
        try:
            pos = int(ins[0])
        except IndexError:
            pos = self.brain.pch
        except ValueError:
            print("what fu*k did you say?")
            return
        # add without repeating
        if pos in self.bplist:
            print("fu*k breakpoint already exist")
        else:
            self.bplist.append(pos)
            print("fu*k breakpoint added at ", pos)

    def bprmv(self, ins):
        "remove a breakpoint at ins[0]"
        try:
            pos = int(ins[0])
        except IndexError:
            pos = self.brain.pch
        except ValueError:
            print("what fu*k did you say?")
            return
        # remove must exist
        try:
            self.bplist.remove(self.brain.pch)
        except ValueError:
            print("fu*k breakpoint does not exist!")
        else:
            print("fu*k breakpoint clear at ", pos)

    def edit(self, ins):
        "edit the code. set the code at ins[0] to ins[1]"
        try:
            pos = int(ins[0])
        except IndexError or ValueError:
            print("what fu*k did you say?")
            return
        else:
            try:
                val = int(ins[1])
            except IndexError:
                val = pos
                pos = self.brain.pch
            except ValueError:
                print("what fu*k did you say?")
                return
        # modify code
        try:
            self.brain.code[pos] = val
        except IndexError:
            print("where fu*k did you write?")
        else:
            print("modify code at ", pos, "to {:#x}".format(val))

    def jump(self, ins):
        "jump in code, ins[0] is the target address"
        try:
            pos = int(ins[0])
        except ValueError:
            print("what fu*k did you say?")
            return
        # check & change pch
        if 0 <= pos < len(self.brain.code):
            self.brain.pch = pos
            print("fu*k jump to position ", pos)
        else:
            print("where fu*k you want to go?")

    def step(self, ins):
        "step forward for ins[0] steps"
        try:
            cnt = int(ins[0])
        except ValueError:
            print("what fu*k did you say?")
            return
        except IndexError:
            cnt = 1
        # set trapcnt
        if cnt >= 1:
            self.trapcnt = cnt
            self.trapflag = False
        else:
            print("where fu*k you want to go?")

    def trap(self):
        "a dummy trap for subclasses to implement"

    def debug(self):
        "The debugger function"
        for bkp in self.bplist:
            if bkp == self.brain.pch:
                self.trapflag = True
                break
        else:  # check trap
            if self.trapcnt > 0:
                self.trapcnt -= 1
            if self.trapcnt == 0:
                self.trapflag = True
            # trap before execution
        self.trap()
        # do normal work
        sym = self.brain.code[self.brain.pch]
        if sym in self.symtbl:
            self.symtbl[sym]()


class BrainDbgCli(BrainDbgCore):
    '''
    cmd interface of braindbg
    '''
    def __init__(self):
        super().__init__(self)
        self.instructions = {
            'a': self.bpadd,
            'b': self.ptraps,
            'c': self.untrap,
            'd': self.parray,
            'e': self.edit,
            'h': self.phelp,
            'i': self.pinfo,
            'j': self.jump,
            'l': self.pcode,
            'q': self.quit,
            'r': self.bprmv,
            's': self.step,
        }

    def phelp(self, ins):
        "print instruction table"
        print('==========brainfu*k debugger instructions========')
        for key, val in self.instructions.items():
            print(key, '\t:', val.__name__, '\n\t', val.__doc__)
        print('========================================*.#=&*===')

    def pinfo(self, ins):
        "print brain information"
        print("brain.array: ", self.brain.array)
        print("brain.array_p: ", self.brain.array_p)
        print("brain.array_n: ", self.brain.array_n)
        print("brain.ptr: ", self.brain.ptr)
        print("brain.pch: ", self.brain.pch)
        print("brain.addrs: ", self.brain.addrs)

    def pcode(self, ins):
        "list code"
        # unpack arguments
        try:
            start = int(ins[1])
        except IndexError:
            start, end = -16, 16
        except ValueError:
            print("what fu*k did you say?")
            return
        else:
            try:
                end = int(ins[2])
            except IndexError:
                end = 16
            except ValueError:
                print("what fu*k did you say?")
                return
        # print code
        print('fu*k code:', self.brain.pch, '(',
              repr(self.brain.code[(self.brain.pch + start):
                                   min(self.brain.pch - 1,
                                       self.brain.pch + end)]), end='')
        if end >= 0:
            print('\033[31m*',
                  repr(self.brain.code[self.brain.pch]),
                  '*\033[0m', end='')
            if end >= 1:
                print(repr(self.brain.code[(self.brain.pch + 1):
                                           (self.brain.pch + end)]), ')')

    def parray(self, ins):
        "print array"
        # unpack arguments
        try:
            start = int(ins[1])
        except IndexError:
            start, end = -16, 16
        except ValueError:
            print("what fu*k did you say?")
            return
        else:
            try:
                end = int(ins[2])
            except IndexError:
                end = 16
            except ValueError:
                print("what fu*k did you say?")
                return
        # combine array, if we do not do this, the code will be annoying
        array = self.brain.array_n[:0:-1] + self.brain.array_p
        offset = self.brain.ptr+len(self.brain.array_n)-1
        # print array
        print('fu*k mem*:', offset, '[',
              self.brain.array[offset + start:min(offset - 1, offset + end)],
              end='')
        if end >= 0:
            print('\033[33m', array[offset], '\033[0m', end='')
            if end >= 1:
                print(self.brain.array[offset + 1:offset + end], ']')

    def ptraps(self):
        "print breakpoints"
        print("fu*k breakpoint list:")
        for b in self.bplist:
            print("byte ", b, " : ", repr(self.brain.code[b]))

    def trap(self):
        "interactions on cmdline, override the dummy one"
        while self.trapflag is True:
            ins = input("fu*k ins.> ").strip().split()
            if ins is not None:
                if ins[0] not in self.instructions:
                    print("what fu*k did you say?")
                else:
                    self.instructions[ins[0]](ins[1:])

    def untrap(self, ins):
        "unset the trap, only used in instruction table"
        self.trapcnt = -1
        self.trapflag = False

    def quit(self, ins):
        "quit process, only used in instruction table"
        quit()


def main():
    "main function, use for test"
    i = Brain()
    i.fuck(
        """WELCOME TO BRAIN FUCK!
        ++++++++++++++++[>+++++>++++>++>+<<<<-]>+++++++.
        >+++++.+++++++.---------.++++++++++++.--.--------.
        >.<<---.-----.>>.<---.<+++.>-.++++++++.<----.
        >---.<+++++++.>---.++++++++.>+.>---.---.
        """
    )


if __name__ == '__main__':
    main()
