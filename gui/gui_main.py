from flask import Flask, render_template, redirect, url_for, request, jsonify
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, FormField, TextAreaField, BooleanField,FileField, FieldList, FormField, IntegerField
from wtforms.validators import DataRequired# App config.
import os
import server.qemu as QEMU
import yaml
from flask_sqlalchemy import SQLAlchemy
from QemuModel import System, Processor, QemuRun, ProcessorType, db
import uuid

DEBUG = True

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mydb.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SECRET_KEY'] = 'C2HWGVoMGfNTBsrYQg8EcMrdTimkZfAb'

machine_dict = QEMU.generate_qemu_dict("qemu")

qemu_object = QEMU.qemu()
def getProcessors( database ):
    names = []
    for p in database.session.query(Processor).all():
        names.append(p.name)
    
    return names
class QemuForm(FlaskForm):
    processor_config = SelectField(label="Processor config", choices=[] )
    binary = SelectField(label='Binary selection', choices=QEMU.find_elf("work"))
    hardware = SelectField(label="Hardware selection" , choices=[])
    additional = StringField('Additional QEMU options')
    save = SubmitField(label="Save")
    cmd  = "abc"
    def setId(self, id ):
        self.id = id 
    def getId(self):
        return self.id


class NewProcessorForm(FlaskForm):
    processors_available = QEMU.find_dts("work")

    name = StringField("Name",validators=[DataRequired()])
    executable = SelectField(label="select_exe" , choices=machine_dict.keys(), id='select_exe')
    memory = IntegerField(label="Memory", default=64,validators=[DataRequired()])
    machine = SelectField(label="Machine Type" , choices=[] ,validators=[DataRequired()], id='select_machine')
    processor = SelectField(label='Processor selection', choices=ProcessorType,validators=[DataRequired()])
    dts = SelectField(label='DTS File', choices=QEMU.find_dts("work"),validators=[DataRequired()])
    add = SubmitField(label="Save")


        

class ControlForm(FlaskForm):
    add =  SubmitField("Add")
    control = SubmitField("Run")

@app.context_processor
def utility( ):
    def get_command(entry ):
        commands = QEMU.database_to_qemu( entry )
        print( "Hey: {}".format(commands) )
        out = " ".join( commands )
        #out = " ".join(q.database_to_qemu( entry ))
        #out = "hey im a command"
        return out
    return dict(get_command=get_command)

@app.route('/_get_choices' , methods=["GET","POST"])
def get_choices():
    exe = request.args.get('executable')

    selection = exe

    machines = machine_dict[exe]
    print( "Exe is {}".format(exe))
    return jsonify( machines )
@app.route('/_get_status', methods=["GET","POST"])
def get_status():
    out = qemu_object.get_status()
    print( " number of statuseses {}".format( len(out)) )
    return jsonify( out )
    
@app.route('/qemu_config', methods=['GET', 'POST'])
def qemu_config():

    return render_template('run.html')


@app.route('/runs', methods=['GET', 'POST'])
def runs():

    # Find all the QEMU runs in the database
    qemuRuns = db.session.query(QemuRun).all()
    print("Runs")
    if( request.method == "POST"):
        print("POST")
        if( "RunAll" in request.form ):
            print("Running")
            qemu_object.run(db)
    print("Number of runs {}".format( len(qemuRuns)))
    
    return render_template('run.html', databases = qemuRuns , type="run")
@app.route('/build' , methods=['GET', 'POST'])
def build():
    form = NewProcessorForm()

    if request.method == 'POST':
        #print("Dealng wiht a post {}".format(request.form))
        if( "remove_button" in request.form ):
            # lets remove stuff
            deleteId = request.form["remove_button"]
            deleteME =db.session.query(Processor).filter(Processor.id == deleteId).first()
            db.session.delete(deleteME)
            db.session.commit()
        if (form.add.data == True):
            newProcessor = Processor()
            newProcessor.id = str(uuid.uuid4())
            newProcessor.exe = str( form.executable.data)
            newProcessor.name = str(form.name.data)
            newProcessor.machine = str(form.machine.data)
            newProcessor.memoryBytes  = int(form.memory.data)
            newProcessor.dts = str( form.dts.data )
            #newProcessor.processor = ProcessorType["CORTEX_A53"]
            db.session.add( newProcessor )
            db.session.commit()
    # Do stuff to the form as needed
    #newProcessor.machine.choices = machine_dict[ ]
    # get processor list from db
    processors = db.session.query(Processor).all()
    return render_template('index.html', type="Processor", title="Processors" ,form=form, database=processors , copyable="LOL" )
@app.route('/', methods=['GET', 'POST'])
def index():

    # you must tell the variable 'form' what you named the class, above
    # 'form' is the variable name used in this template: index.html
    #qemuObj = QEMU.qemu(  systemDB )

    form = QemuForm()
    
    ## See if we need to add a new form
    if request.method == 'POST':
        #print("Dealng wiht a post {}".format(request.form))
        if( "remove_button" in request.form ):
            # lets remove stuff
            deleteId = request.form["remove_button"]
            print("Trying to delete {}".format(deleteId))
            deleteME =db.session.query(QemuRun).filter(QemuRun.id == deleteId).first()
            db.session.delete(deleteME)
            db.session.commit()
        if( form.save.data == True):
            newQemu = QemuRun()
            newQemu.id=  str(uuid.uuid4())
            newQemu.binary = form.binary.data
            newQemu.options = form.additional.data
            processorName = form.processor_config.data

            # find the processor name we care about 
            processorModel =  db.session.query(Processor).filter( Processor.name == processorName ).first()
            newQemu.processor = processorModel 

            db.session.add( newQemu )
            db.session.commit()
            print("Commited to DB {}".format(db))
 
    # do things to the form as needed
    form.processor_config.choices = getProcessors(db)
    
    qemusToList = db.session.query(QemuRun).all()

    return render_template('index.html', type="QEMU Instance",title="QEMU Configuration", form=form, database=qemusToList , copyable="LOL" )
    
# Flask-Bootstrap requires this line
if __name__ == "__main__":
    with app.app_context():
        db.init_app(app=app)
        db.create_all()


        Bootstrap(app)
        app.run(debug=True , host='0.0.0.0')
