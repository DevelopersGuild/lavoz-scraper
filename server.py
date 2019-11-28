from flask import Flask
from flask_graphql import GraphQLView
from scrapes import get_page_length, get_link_data, get_story_data
import graphene

app = Flask(__name__)

class Link(graphene.ObjectType):
    href = graphene.String()
    content = graphene.String()
    
class Story(graphene.ObjectType):
    headline = graphene.String()
    by = graphene.String()
    date = graphene.Date()
    tags = graphene.List(graphene.String)
    content = graphene.List(graphene.String)
    href = graphene.String()

class Query(graphene.ObjectType):
    pages = graphene.Int()
    links = graphene.List(Link, index=graphene.Int(default_value=2))
    story = graphene.Field(Story, url=graphene.String(required=True))
    
    def resolve_pages(self, info):
        return get_page_length()
    
    def resolve_links(self, info, index: int):
        return get_link_data(index)

    def resolve_story(self, info, url: str):
        return get_story_data(url)
    


schema = graphene.Schema(query=Query)



app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True))

if __name__ == "__main__":
    app.run(debug=True)