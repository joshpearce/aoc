from pathlib import Path
import sys
from typing import List, Tuple
import re
import copy

def parse_int_str(val: str) -> int:
    try:
        return int(re.sub("^0+", "", val).replace("#", "0x"), 0)
    except:
        return int(re.sub("[^0-9]", "", val))

def parse_pid_str(val: str) -> int:
    if not re.match("^[0-9]{9}$", val):
        return None
    return parse_int_str(val)

def parse_year_str(val: str, min: int, max: int) -> int:
    v = parse_int_str(val)
    if v and v >= min and v <= max:
        return v
    else:
        return None

def parse_height_str(val) -> Tuple[int, str]:
    ht = (parse_int_str(re.sub("[^0-9]+", "", val)), re.sub("[0-9]+", "", val))
    if ht[1] == "cm":
        if ht[0]:
            if ht[0] < 150 or ht[0] > 193:
                return None
            else:
                return ht
    elif ht[1] == "in":
        if ht[0]:
            if ht[0] < 59 or ht[0] > 76:
                return None
            else:
                return ht
    
    return None

def parse_hair_color(val: str) -> bytearray:
    if re.match("^#[0-9a-f]{6}$", val):
        return bytearray.fromhex(val.replace("#", ""))
    return None

def parse_eye_color(val: str) -> str:
    if val in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]:
        return val
    return None

class Passport:
    ecl: str = None
    pid: int = None
    eyr: int = None
    hcl: bytearray = None
    byr: int = None
    iyr: int = None
    cid: int = None
    hgt: Tuple[int, str] = None
    data: List[str] = None

    def __init__(self, lines: List[str]):
        self.data = copy.deepcopy(lines)
        for line in lines:
            for kvs in line.split():
                k,v = kvs.split(":")
                # TODO: Make a switch statement
                self.ecl = parse_eye_color(v) if k == "ecl" else self.ecl
                self.pid = parse_pid_str(v) if k == "pid" else self.pid
                self.eyr = parse_year_str(v, 2020, 2030) if k == "eyr" else self.eyr
                self.hcl = parse_hair_color(v) if k == "hcl" else self.hcl
                self.byr = parse_year_str(v, 1920, 2002) if k == "byr" else self.byr
                self.iyr = parse_year_str(v, 2010, 2020) if k == "iyr" else self.iyr
                self.cid = parse_int_str(v) if k == "cid" else self.cid
                self.hgt = parse_height_str(v) if k == "hgt" else self.hgt
    
    def is_valid(self):
        valid = (
            self.ecl != None and 
            self.pid != None and 
            self.eyr != None and 
            self.hcl != None and 
            self.byr != None and 
            self.iyr != None and 
            self.hgt != None
        )

        return valid




def run(file_path: Path) -> None:
    passports: List[Passport] = []
    group: List[str] = []
    with file_path.open("r") as file:
        for line in file.readlines():
            if len(line.strip()) == 0:
                passports.append(Passport(group))
                group = []
            else:
                group.append(line)
    print (sum([1 if p.is_valid() else 0 for p in passports]))



if __name__ == "__main__":
    file_path = Path(__file__).parent / "input.txt"
    if len(sys.argv) > 1:
        file_path = Path(sys.argv[1])
    run(file_path)