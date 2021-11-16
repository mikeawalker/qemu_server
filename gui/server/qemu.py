import subprocess
import yaml
import argparse
import os
import glob
from flask_sqlalchemy import SQLAlchemy
from QemuModel import System, Processor, QemuRun, ProcessorType
import subprocess
class qemu:
    def __init__(self ):
        self.threads = []
    def run( self , db ):
        # cleanup 
        self.kill_processes()        
        # get all qemu instances
        qemuRuns = db.session.query(QemuRun).all()

        # loop over all qemu instances and get commands
        commandGroup = []
        for run in qemuRuns:
            command = database_to_qemu( run )
            command = ["timeout" , "20"]
            print( "Starting")
            p = subprocess.Popen( command , stdout=subprocess.PIPE, shell=True)
            print( "Ending")
            td = dict()
            td["process"] = p
            td["id"] = run.id
            self.threads.append( td )

        pass
    def kill_processes(self):
        for process in self.threads:
            process["process"].terminate()
        self.threads = []
    def get_status( self ):
        out = []
        for t in self.threads:
            poll = t["process"].poll()
            if poll is None:
                pair = ( t["id"], 1)
            else:
                pair = ( t["id"], 0)
            out.append( pair )
        return out
def database_to_qemu( qemu  ):
    processor  = qemu.processor
    command = []
    # exe
    
    command.append( processor.exe)
    # memory
    command.append("-m")
    command.append( str(processor.memoryBytes) ) 
    # dtb 
    dtb = "lol" #self.build_dtb( run.processor.dts )
    command.append("-hw-dtb")
    command.append(dtb)
    # machine 
    command.append("-M")
    command.append(processor.machine)
    # elf / bin
    command.append("-kernel")
    command.append( qemu.binary )
    # connect serial to stdio
    command.append("-serial")
    command.append("stdio")
    # other 
    opts_array =[]
    if( qemu.options != None ):
        opts_array = qemu.options.split(" ")
    
    #for opt in opts_array:
    #    command.append( opts_array )
    # Turn off the display
    command.append("-display")
    command.append("none")
        
    
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
def machine_command_from_name( name  , tupleList ):
    out = list( filter( lambda x:name in x , tupleList ))
    print( out )
    return out
    