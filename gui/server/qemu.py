import subprocess
import yaml
import argparse
import os
import glob
from flask_sqlalchemy import SQLAlchemy
from QemuModel import System, Processor, QemuRun, ProcessorType

class qemu:
    def __init__(self , db):
        self.database = db
      
    
    
    def run(self , options ):
        print("Running an instance of qemu")
        parse_inputs(self)
        build_command(self)
    def getCommand():
        return command
    def terminate():
        pass
    
    def database_to_qemu(self , run ):
        
        command = []
        # exe
        processor_exe = "qemu.exe" #qemu.deduce_processor( run.processor.processor )
        # memory
        #command.append("-M")
        #command.append( run.processor.memoryBytes)
        # dtb 
        dtb = "lol" #self.build_dtb( run.processor.dts )
        command.append("-hw-dtb")
        command.append(dtb)
        # elf / bin
        command.append("-kernel")
        command.append( run.binary )
        # other 
        opts_array =[]
        if( run.options != None ):
            opts_array =[]# run.options.split(" ")
        for opt in opts_array:
            command.append( opts_array )
        command = ["hi", "its", "me"]
            
        
        return command
def find_elf( folder ):
    searchPath = os.path.join( folder , "**/*.elf") 
    fileList = glob.glob(searchPath, recursive=True)

    return fileList
def find_dts( folder ):
    searchPath = os.path.join(folder ,"**/*.dts")
    fileList = glob.glob(searchPath, recursive=True)
    return fileList
def find_yamls(folder):
    searchPath = os.path.join(folder ,"**/*.yaml")
    fileList = glob.glob(searchPath, recursive=True)
    return fileList
def generate_qemu_dict( path ):
    out = dict()
    for file in os.listdir(path):
        f = open( os.path.join(path,file),'rt')
        lines = f.readlines()
        arr = []
        for line in lines:
           pair = line.split(",")
           item = ( pair[0] , pair[1].strip("\n"))
           arr.append( item)
        out[file] = arr
    print("dictionary:\n {}".format(out))
    return out

    