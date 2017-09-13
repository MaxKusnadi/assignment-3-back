# from sqlalchemy import create_engine
# from sqlalchemy.orm import scoped_session, sessionmaker
# from sqlalchemy.ext.declarative import declarative_base
#
# db_username = 'root'
# db_password = 'pass'
# db_name = 'app_db'
# # db_url = 'mysql://{0}:{1}@localhost/{2}'.format(db_username, db_password, db_name)
# db_url = 'sqlite:///test.db'
#
# engine = create_engine(db_url, convert_unicode=True)
# db_session = scoped_session(sessionmaker(autocommit=False,
#                                          autoflush=False,
#                                          bind=engine))
# Base = declarative_base()
# Base.query = db_session.query_property()
#
# def init_db():
#     Base.metadata.drop_all(bind=engine)
#     import a3.models
#     Base.metadata.create_all(bind=engine)
