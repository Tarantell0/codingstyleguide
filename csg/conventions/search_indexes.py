import datetime
from haystack import indexes
from conventions.models import Convention
from tags.models import Tag

class ConventionIndex(indexes.SearchIndex, indexes.Indexable): 
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title')
    description = indexes.CharField(model_attr='description',null=True)
    creation_date = indexes.DateTimeField(model_attr='creation_date')

    #tag = indexes.EdgeNgramField(model_attr='tag')
    """EdgeNgramField will pay attention for example to spaces, etc. 
    The content_auto create a table while typing"""
    #content_auto = indexes.EdgeNgramField(model_attr='title') 

    tag_name = indexes.CharField()
    def get_model(self):
        return Convention
   
    def prepare_tag_name(self, obj):
        return obj.tag.name
   

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all() #.select_related(tag.convention_set.name)


class TagIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr='name')

    def get_model(self):
        return Tag

    def index_queryset(self, using=None):
        return self.get_model().objects.all()


