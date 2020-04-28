from django.db import models

class Post(models.Model):

    title = models.CharField(max_length=100)
    body = models.TextField()
    genre = models.TextField()
    imgLink = models.TextField()
    author = models.ForeignKey('auth.User',on_delete=models.CASCADE,)
    status = models.CharField(max_length=20)

    # def __str__(self):
    #     return self.title

class Links(models.Model):
    animeKaizoku=models.TextField()
    anidl=models.TextField()
    postId = models.ForeignKey(Post,on_delete=models.CASCADE)

class AnimeInfo(models.Model):
    episode_list = models.CharField(max_length=10)
    op_list = models.TextField()
    ed_list = models.TextField()
    postId = models.ForeignKey(Post,on_delete=models.CASCADE)

