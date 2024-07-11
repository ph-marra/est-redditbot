from structure import RedditStructure
import copy
import json

class Post:
    def __init__(self, url, title, post_itself):
        self.url = url
        self.json_name = RedditStructure.get_json_name_from_url(url)
        self.title = title
        self.post_itself = post_itself
        self.comments = []
        self.retrieved_at = None
        
    def __str__(self):        
        return "(" + str(self.json_name) + ", " + str(self.title) + ")"

    def to_json(self):        
        obj_dict = copy.deepcopy(self.__dict__)
        
        if self.comments:
            obj_dict['comments'] = list(self.comments)
        
        with open(self.json_name + ".json", "w", encoding="utf-8") as out:
            out.write(json.dumps(obj_dict))