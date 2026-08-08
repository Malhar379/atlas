from database.base import Base
from database.connection import engine
from database.models import Experiment, Run
from database.base import Base
from database.connection import engine

# Import all models
from database.models import Experiment

Base.metadata.create_all(bind=engine)

print("Tables created successfully!")