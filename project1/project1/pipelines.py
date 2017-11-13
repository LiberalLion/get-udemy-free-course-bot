# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from project1.items import Course

class UdemyCoursePipeline(object):
    """Livingsocial pipeline for storing scraped items in the database"""
    def __init__(self):
        """
        Initializes database connection and sessionmaker.
        Creates deals table.
        """
        #engine = db_connect()
        #create_deals_table(engine)
        #self.Session = sessionmaker(bind=engine)
        engine = create_engine('sqlite:///courses.db')
        self.Session = sessionmaker(bind=engine)
        #session = Session()


    def process_item(self, item, spider):
        """Save deals in the database.

        This method is called for every item pipeline component.

        """
        session = self.Session()


        try:
            course=session.query(Course).filter(Course.udemy_url == item['udemy_url']).limit(1).with_for_update().one_or_none()
            if course is not None:
                print("course already inside")
                item_dict=dict(item)
                for key, value in item_dict.items():
                    print(key,value)
                    setattr(course,key,value)
                session.add(course)
                session.commit()
            else:
                course = Course(**item)
                session.add(course)
                session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

        return item
