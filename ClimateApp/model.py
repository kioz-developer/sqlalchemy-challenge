import sqlalchemy
import pandas as pd
import datetime as dt
import matplotlib.dates as mdates
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from connection import Connection

class Model(Connection):

    def __init__(self):
        Connection.__init__(self)

    def precipitation(self):
        # Create our session (link) from Python to the DB
        session = Session(self.engine)
        Measurement = self.Measurement
        
        # Create an sqlalchemy query
        results = session.query( 
            Measurement.date, 
            Measurement.prcp
        ).order_by(
            Measurement.date.desc()
        ).all()

        # Convert query results to dataframe
        df = pd.DataFrame(results, columns=['date','prcp'])
        df.set_index('date', inplace=True)

        # Close Session
        session.close()

        # Convert dataframe to dictionary
        return df.to_dict()

    def stations(self):
        # Create our session (link) from Python to the DB
        session = Session(self.engine)
        Station = self.Station

        # Create an sqlalchemy query
        results = session.query( 
            Station.id, 
            Station.station, 
            Station.name, 
            Station.latitude, 
            Station.longitude, 
            Station.elevation 
        ).order_by(
            Station.id.desc()
        ).all()

        # Convert query results to dataframe
        columns = ['id','station','name','latitude','longitude','elevation']
        df = pd.DataFrame(results, columns=columns)
        df.set_index('id', inplace=True)

        # Close Session
        session.close()

        # Convert dataframe to dictionary
        return df.to_dict(orient='records')

    def last_year_tobs(self):
        # Create our session (link) from Python to the DB
        session = Session(self.engine)
        Measurement = self.Measurement

        # Find the most recent date in the data set.
        results = session.query(
            Measurement.date
        ).order_by(
            Measurement.date.desc()
        ).limit(1).all()

        most_recent_date_str = results[0][0]
        most_recent_date = dt.datetime.strptime(most_recent_date_str, '%Y-%m-%d')
        start_date = most_recent_date - dt.timedelta(days=+365)

        # Create an sqlalchemy query
        results = session.query( 
            Measurement.date, 
            Measurement.prcp 
        ).filter(
            Measurement.date >= start_date
        ).all()

        # Convert query results to dataframe
        df = pd.DataFrame(results, columns=['date','prcp'])

        # Close Session
        session.close()

        # Convert dataframe to dictionary
        return df.to_dict(orient='records')

    def tobs_by_start(self, start_date):
        # Create our session (link) from Python to the DB
        session = Session(self.engine)
        Measurement = self.Measurement

        # Create an sqlalchemy query
        results = session.query( 
            Measurement.date, 
            Measurement.prcp 
        ).filter(
            Measurement.date >= start_date
        ).all()

        # Convert query results to dataframe
        df = pd.DataFrame(results, columns=['date','prcp'])
        df = df.groupby('date')['prcp'].agg(['min', 'mean', 'max']).reset_index()

        # Close Session
        session.close()

        # Convert dataframe to dictionary
        return df.to_dict(orient='records')

    def tobs_by_start_end(self, start_date, end_date):
        # Create our session (link) from Python to the DB
        session = Session(self.engine)
        Measurement = self.Measurement

        # Create an sqlalchemy query
        results = session.query( 
            Measurement.date, 
            Measurement.prcp 
        ).filter(
            Measurement.date >= start_date,  
            Measurement.date <= end_date
        ).all()

        # Convert query results to dataframe
        df = pd.DataFrame(results, columns=['date','prcp'])
        df = df.groupby('date')['prcp'].agg(['min', 'mean', 'max']).reset_index()

        # Close Session
        session.close()

        # Convert dataframe to dictionary
        return df.to_dict(orient='records')