from multiprocessing.pool import Pool
from multiprocessing import cpu_count
import subprocess
import sys
from config import PIN, MAX_NUM, MIN_NUM


def call_proc(cmd):
    """ This runs in a separate thread. """
    # subprocess.call(shlex.split(cmd))  # This will block until cmd finishes
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    return (out, err)


class Pin(object):
    def __init__(self, INSCOUNT, filename, target_addr):
        self.filename = filename
        self.result = ''
        self.INSCOUNT = INSCOUNT
        self.target_addr = str(int(target_addr, 16))

    def run_pin(self, args):
        pool = Pool(cpu_count()) #获取cpu个数
        results = []
        for each_args in args:
            command = 'echo {} | {} -t {} -a {} -- {}'.format(each_args[1], PIN, self.INSCOUNT, self.target_addr,
                                                              self.filename)
            result = pool.apply_async(call_proc, (command,))
            results.append((each_args[0], each_args[1], result))
        deal_result = []
        # io流最后处理
        for each in results:
            out, err = each[2].get()
            count = int(out.decode().split("Count:")[1], 10)
            deal_result.append([each[0], each[1], count])
        pool.close()
        pool.join()
        diff = deal_result[0][2]
        for i in deal_result:
            i.append(i[2] - diff)
        self.result = deal_result

    def get_all_result(self):
        return self.result

    def get_equal(self, diff):
        for each in self.result:
            if each[3] == diff:
                return each[0]
        print("Not found equal")
        sys.exit(0)

    def get_unequal(self, diff):
        for each in self.result:
            if each[3] != diff:
                return each[0]
        print("Not found unequal")
        sys.exit(0)

    def get_below(self, diff):
        for each in self.result:
            if each[3] <= diff:
                return each[0]
        print("Not found below")
        sys.exit(0)

    def get_after(self, diff):
        for each in self.result:
            if each[3] >= diff:
                return each[0]
        print("Not found after")
        sys.exit(0)

    def get_min(self):
        min_num = MAX_NUM
        index = self.result[0][0]
        for each in self.result:
            if each[3] <= min_num:
                min_num = each[3]
                index = each[0]
        return index

    def get_max(self):
        max_num = MIN_NUM
        index = self.result[0][0]
        for each in self.result:
            if each[3] >= max_num:
                max_num = each[3]
                index = each[0]
        return index

    def get_diff(self):
        num = []
        charset = []
        for i in self.result:
            num.append(i[3])
            charset.append(i[0])
        temp = [elem for elem in num if num.count(elem) == 1]
        return charset[num.index(temp[0])]
