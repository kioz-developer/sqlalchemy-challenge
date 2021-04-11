import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine, func

class Connection:

    def __init__(self):
        # create engine to hawaii.sqlite
        print("Create engine ...")
        engine = create_engine("sqlite:///../Resources/hawaii.sqlite")

        # reflect an existing database into a new model
        print("Automap base ...")
        Base = automap_base()

        # reflect the tables
        print("Reflect tables ...")
        Base.prepare(engine, reflect=True)

        # Save references to each table
        print(f"Measurement: {Base.classes.measurement}")
        print(f"Station: {Base.classes.station}")
        
        self.Measurement = Base.classes.measurement
        self.Station = Base.classes.station
        self.engine = engine