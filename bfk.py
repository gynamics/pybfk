#!/usr/bin/python
'''bfk: 
A naive implementation of brainfu*k, go:

    brain.fuck(",>[.>,]")

'''


class brain:
    def __init__(self):
        self.array_p = [0] # non negative array
        self.array_n = [0] # negative array
        self.array = self.array_p
        self.addrs = []
        self.ptr = 0
        self.pch = 0
        self.bplist = [] # breakpoint list
        self.trap = -1   # trap counter

    def err(self, msg):
    # report an error
        print(msg)

    def rsh(self):
    # right shift
        self.ptr += 1
        if self.ptr == 0:
            self.array = self.array_p
        if(self.ptr >= len(self.array)):
            self.array.append(0)

    def lsh(self):
    # left shift
        self.ptr -= 1
        if self.ptr == -1 :
            self.array = self.array_n
        if(abs(self.ptr) >= len(self.array)):
            self.array.append(0)

    def inc(self):
    # increment byte
        self.array[abs(self.ptr)] = (self.array[abs(self.ptr)]+1) % 256

    def dec(self):
    # decrement byte
        self.array[abs(self.ptr)] = (self.array[abs(self.ptr)]+255) % 256

    def ldt(self):
    # load to
        flag = True
        while flag:
            try:
                self.array[abs(self.ptr)] = input()
            except ValueError:
                print("Invalid, please try again")
            else:
                flag = False

    def ott(self):
    # output to
        print('%c' % (self.array[abs(self.ptr)]), end='')

    def jnz(self):
    # jump if not zero
        if self.array[abs(self.ptr)] != 0:
            self.pch = self.addrs[-1]
        else:
            self.addrs.pop()

    def lab(self):
    # load address back
        self.addrs.append(self.pch)

    def ign(self):
    # ignore
        pass

    def dbg(self, code):
    # for debug and trap
        for b in self.bplist: # check breakpoints
            if b == self.pch:
                print("fu*k break")
                break
        else: # check trap
            self.trap -= 1
            if self.trap != 0:
                return
            print("fu*k trapped")
        while True:
            # print code
            start, end = 0, 0
            while start >= -16:
                if code[self.pch + start - 1] == '\n':
                    break
                start -= 1
            while end <= 32 + start:
                if code[self.pch + end ] == '\n':
                    break
                end += 1
            print('fu*k code:', self.pch, end='')
            print( '(', code[(self.pch + start ):self.pch], '\033[31m*', end='')
            if code[self.pch] != '\n':
                print(code[self.pch], end='')
            else:
                print('\\n', end='')
            print( '*\033[0m', code[(self.pch + 1):(self.pch + end)], ')')
            # print array
            print('fu*k mem*:', self.ptr, end='')
            print( '[', self.array[self.ptr-16:self.ptr],
                  '\033[33m', self.array[self.ptr], '\033[0m',
                   self.array[self.ptr+1:self.ptr+16], ']')
            # interaction
            ins = input("fu*k ins.> ")
            if ins == "":
                print("fu*k you didn't say anything!")
                continue
            if ins == "ba": # breakpoint add
                bpaddr = self.pch
                for b in self.bplist:
                    if b == bpaddr:
                        print("fu*k breakpoint already exist")
                        break
                else:
                    self.bplist.append(bpaddr)
                    print("fu*k breakpoint added at ", self.pch)
            elif ins == "bc": # breakpoint clear
                try:
                    self.bplist.remove(self.pch)
                except ValueError:
                    print("which breakpoint fu*k you want to remove?")
                else:
                    print("fu*k breakpoint clear at ", self.pch)
            elif ins == "bl": # breakpoint list
                print("fu*k breakpoint list:")
                for b in self.bplist:
                    print("byte ", b, " : ", repr(code[b]))
            elif ins[0] == 'b': # breakpoint at line l
                try:
                    l = int(ins[1:])
                except ValueError:
                    print("what fu*k did you say?")
                else:
                    for b in self.bplist:
                        if b == l:
                            print("fu*k breakpoint already exist")
                            break
                    else:
                        self.bplist.append(l)
                        print("fu*k breakpoint added at ", l)
            elif ins == "c": # continue
                self.trap = -1
                print("fu*k continue")
                break
            elif ins[0] == 'd': # dump memory
                try:
                    l = int(ins[1:])
                except ValueError:
                    print("what fu*k did you say?")
                else:
                    try:
                        v = self.array[l]
                    except IndexError:
                        print("where fu*k you want to see?")
                    else:
                        print("fu*k mem* dump: from ", l-16, " to ", l+16)
                        print('\033[34m#\033[0m', self.array[l-16:l],
                          '\033[34m', self.array[l], '\033[0m',
                          self.array[l+1:l+16], '\033[34m#\033[0m')
            elif ins[0] == 'e': # edition
                code[self.pch] = ins[1]
                print("modify current code to ", ins[1], ":{:#x}".format(ins[1]))
            elif ins == "h": # help
                print("""fu*k helpstr:
                ==========brainfu*k debugger instructions========
                ba      :add a breakpoint at current position
                bc      :clear breakpoint at current position
                bl      :list breakpoints
                b num   :add a breakpoint at code[num]
                c       :continue
                d num   :dump memory at array[num-16:num+16]
                e$      :edit character at current position to $
                h       :show this fu*king help
                i       :show brainfu*k information
                j num   :jump to code[num]
                l num   :list code at code[num-16:num+16]
                s       :step
                s num   :step forward for num
                sc      :step forward to <>+-,.[]
                q       :quit
                ========================================*.#=&*===
                """)
            elif ins == "i": # information
                print("self.array: ", self.array)
                print("self.array_p: ", self.array_p)
                print("self.array_n: ", self.array_n)
                print("self.ptr: ", self.ptr)
                print("self.pch: ", self.pch)
                print("self.addrs: ", self.addrs)
            elif ins[0] == 'j':
                try:
                    l = int(ins[1:])
                except ValueError:
                    print("what fu*k did you say?")
                else:
                    try:
                        v = code[l]
                    except IndexError:
                        print("where fu*k you want to go?")
                    else:
                        self.pch = l
                        print("fu*k jump to position ", l)

            elif ins[0] == 'l': # list code
                try:
                    l = int(ins[1:])
                except ValueError:
                    print("what fu*k did you say?")
                else:
                    try:
                        v = code[l]
                    except IndexError:
                        print("where fu*k you want to see?")
                    else:
                        print("fu*k list code: from ", l-16, " to ", l+16)
                        print('\033[36m&\033[0m', repr(code[l-16:l]),
                              '\033[36m',repr(code[l]),'\033[0m',
                              repr(code[l+1:l+16]), '\033[36m&\033[0m')
            elif ins == "s":
                print("fu*k step")
                self.trap = 1
                return
            elif ins == "sc": # step to code
                while self.pch < len(code):
                    if code[self.pch] in "<>+-,.[]":
                        break
                    self.pch += 1
            elif ins[0] == 's': # step multiple instructions 
                try:
                    s = int(ins[1:])
                except ValueError:
                    print("what fu*k did you say?")
                else:
                    print("fu*k ", s, " steps")
                    self.trap = s
                    return
            elif ins == "q": # quit
                print("fu*k quit")
                quit()
            else:
                print("what fu*k did you say?")
            # extend debug functions here

    def fuck(self, code):
        while self.pch < len(code):
            ch = code[self.pch]
            self.dbg(code) # for debug uses
            if ch == '>':
                self.rsh()
            elif ch == '<':
                self.lsh()
            elif ch == '+':
                self.inc()
            elif ch == '-':
                self.dec()
            elif ch == ',':
                self.ldt()
            elif ch == '.':
                self.ott()
            elif ch == ']':
                self.jnz()
            elif ch == '[':
                self.lab()
            else:
                self.ign()
            self.pch += 1

def main():
    i = brain()
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
