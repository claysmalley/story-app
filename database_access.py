# import rethinkdb as r
# import time

class DatabaseConnection:
    def __init__(self):
        self.stories = []
        #self.conn = r.connect(host='ec2-23-23-81-171.compute-1.amazonaws.com', port=5432, auth_key='')

        #if 'storyapp' not in r.db_list().run(self.conn):
        #    r.db_create('storyapp').run(self.conn)
        #if 'stories' not in r.db('storyapp').table_list().run(self.conn):
        #    r.db('storyapp').table_create('stories').run(self.conn)

    def get_stories(self, limit):
        return self.stories[-limit:]
        #return r.db('storyapp').table('stories').order_by(r.desc('time')).limit(limit).run(self.conn)
    
    def get_story(self, story_id):
        return self.stories[story_id]
        #return r.db('storyapp').table('stories').get(story_id).run(self.conn)
    
    def add_story(self, story):
        self.stories.append(story)
        return len(self.stories) - 1
        #return r.db('storyapp').table('stories').insert({ 'story': story, 'time': int(time.time()) }).run(self.conn)
