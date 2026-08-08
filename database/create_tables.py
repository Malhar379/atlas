from database.base import Base
from database.connection import engine
from database.models import Experiment, Run

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

print("Tables created successfully!")