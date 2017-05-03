from rest_framework import serializers
from blog.models import Blog

class BlogSerializer(serializers.ModelSerializer):
    """
    Serializer class for Blog Model
    """
    class Meta:
        model = Blog
        fields =('id','title','body','publish','created','modified')