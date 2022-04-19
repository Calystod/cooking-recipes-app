class Recipe():

    def __init__(self, recipe_json):
        #uuid = UUIDField()
        self.url = recipe_json['url']
        self.name = recipe_json['name']
        self.picture = recipe_json['picture']
        self.description = recipe_json['description']
        self.recipe_json = recipe_json

    def __str__(self):
        recipe = """
        'url': %s, 
        'name': %s, 
        'picture': %s,
        'description': %s
        """ % (self.url, self.name, self.picture, self.description)

        return recipe
