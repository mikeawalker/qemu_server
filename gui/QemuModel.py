from flask_sqlalchemy import SQLAlchemy
import enum
import uuid

db = SQLAlchemy()

class ProcessorType( enum.Enum ):
    CORTEX_A9 = "Cortex A9"
    CORTEX_A53 = "Cortex A53"
    CORTEX_R5  = "Cortex R5"

class System( db.Model ):
    __tablename__ = 'systems'
    id = db.Column( db.String,primary_key=True)

class Processor(db.Model):
    """Stores an setup instance a specific processor"""
    __tablename__ = 'processors'

    id = db.Column(db.String(256), primary_key=True )
    name = db.Column(db.String(256) , default="")
    exe = db.Column(db.String(256) , default="")
    #processor   = db.Column(db.Enum(ProcessorType))
    memoryBytes = db.Column(db.Integer)
    machine     = db.Column(db.String(50))
    used_by     = db.relationship( "QemuRun" , back_populates="processor"  )
class QemuRun(db.Model):
    """Stores additional data to simulate a single processor with QEMU"""
    __tablename__ = 'qemus'
    id = db.Column(db.String(256), primary_key=True )

    #system_id = db.Column(db.String, db.ForeignKey('systems.id'))
    #qemu_exe = db.Column(db.String(128))
    binary = db.Column(db.String(256))
    options = db.Column(db.String(1024), default = "" )
    archived = db.Column( db.Boolean , default = False )
    processor_id =  db.Column(db.String(256), db.ForeignKey('processors.id'))
    processor = db.relationship("Processor", back_populates="used_by")

