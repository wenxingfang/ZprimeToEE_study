import os
import ROOT



class out_object:
    def __init__(self, name, input_path, output_name):
        self.name = name
        self.input_path = input_path
        self.output_name = output_name
        self.filenames = os.listdir(self.input_path)
    def print_err(self):
        f1 = open(self.output_name,'w')
        N=0
        for ifile in  self.filenames:
            N=N+1
            if N%1000==0:
                print N
            file_name=self.input_path+ifile
            #print file_name
            if "sh.e" not in file_name:continue
            f2 = open(file_name,'r') 
            lines = f2.readlines()
            #last_line=lines[-1]
            #if "Done" not in last_line:
            for li in lines:
                if "bus" in li or "Error" in li:
                    f1.write(ifile)
                    f1.write('\n')
                    break
            f2.close()
        f1.close() 


obj_list=[]
obj_list.append(out_object("1","./","err_1.txt"))

for i in obj_list:
    i.print_err()
    print "%s is done"%(i.name)
