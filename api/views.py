from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from blog.models import Blog
from api.serializers import BlogSerializer
import logging
logger = logging.getLogger("django")

#used Function based views

@api_view(['GET','POST'])
def blog_list(request):
    """
    Lists all blogs, or create a new blog
    """
    if request.method == 'GET':
        logger.info("GET method called")
        blogs = Blog.objects.all()
        serializer = BlogSerializer(blogs,many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        logger.info("POST method called")
        logger.info("Data passed : %s"%str(request.data))
        serializer = BlogSerializer(data=request.data)
        if serializer.is_valid():
            logger.info("Valid data passed and created the record")
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            logger.error("%s"%str(serializer.errors))
            logger.error("HTTP_400_BAD_REQUEST")
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PUT','DELETE'])
def blog_detail(request,pk):
    """
    Get,Update, or delete a specific blog
    """
    #If a blog with the specified key not present, it is handled by catching the exception "DOesNotExist"
    try:
        blog=Blog.objects.get(pk=pk)
    except Blog.DoesNotExist:
        logger.error("ID [%s] does not exist"%str(pk))
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        #Get a blog
        serializer = BlogSerializer(blog)
        logger.info("Getting info for [%s]"%str(pk))
        return Response(serializer.data)
    elif request.method == 'PUT':
        #Update a blog
        serializer=BlogSerializer(blog,data=request.data)
        if serializer.is_valid():
            logger.info("Updating info for [%s]"%str(pk))
            serializer.save()
            return Response(serializer.data)
        logger.error("PUT error : %s"%str(serializer.errors))
        logger.error("HTTP_400_BAD_REQUEST")
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        #delete a blog
        blog.delete()
        logger.info("Deleting info [%s]"%str(pk))
        return Response(status=status.HTTP_204_NO_CONTENT)

