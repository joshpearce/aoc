#!/usr/bin/env python3

from bitarray import *
import binascii
from bitarray.util import ba2int
from math import prod

def add_version_nums(packet):
    count = 0
    queue = [packet]
    while any(queue):
        p = queue.pop()
        count += p.version
        queue += p.packets
    return count

class Packet:
    def __init__(self, bits):
        self.version = ba2int(bits[0:3])
        self.typeid = ba2int(bits[3:6])
        self.packets = []
        self.length = 6

        if  self.typeid == 4: # parse literal value
            temp = bitarray()
            chunk = bitarray('1')
            i = 1
            while chunk[0] == 1:
                i += 5
                self.length += 5
                chunk = bits[i:i+5]
                temp += chunk[1:]
            
            self.litval = ba2int(temp)
        else: #parse operator
            self.length_type_id = bits[6]
            self.length += 1
            # Just doing the same non-dry logic for each scenario, but I think that's okay for now
            if not self.length_type_id:
                self.subpackets_total_len = ba2int(bits[7:22])
                self.length += 15
                j = 22
                children_length = 0
                while children_length < self.subpackets_total_len:
                    np = Packet(bits[j:])
                    self.length += np.length
                    children_length += np.length
                    j += np.length
                    self.packets.append(np)
            else:
                self.subpackets_num = ba2int(bits[7:18])
                self.length += 11
                j = 18
                
                while len(self.packets) < self.subpackets_num:
                    np = Packet(bits[j:])
                    self.length += np.length
                    j += np.length
                    self.packets.append(np)
    
    def get_value(self):
        rtn = None
        match self.typeid:
            case 0:
                rtn =  sum(p.get_value() for p in self.packets)
            case 1:
                rtn =  prod(p.get_value() for p in self.packets)
            case 2:
                rtn =  min(p.get_value() for p in self.packets)
            case 3:
                rtn =  max(p.get_value() for p in self.packets)
            case 4:
                rtn =  self.litval
            case 5:
                rtn =  1 if self.packets[0].get_value() > self.packets[1].get_value() else 0
            case 6:
                rtn =  1 if self.packets[0].get_value() < self.packets[1].get_value() else 0
            case 7:
                rtn =  1 if self.packets[0].get_value() == self.packets[1].get_value() else 0
        return rtn

def part_one(bits):
    
    p = Packet(bits)
    vc = add_version_nums(p)
    return vc
        
def part_two(bits):

    p = Packet(bits)
    return p.get_value()

if __name__ == "__main__":
    from pathlib import Path

    f = "test.txt"
    f = "input.txt"
    lines = (Path(__file__).parent / f).open().read().split("\n")
    bin = binascii.unhexlify(lines[0]) # 0 - lit value, 1 - operator with 2 sub packets, 2 - operator with 3 sub packets,
    bits = bitarray()
    bits.frombytes(bin)
    
    print("\nPart one:")
    print(f"{part_one(bits)}")

    print("Part two:")
    print(f"{part_two(bits)}")
    