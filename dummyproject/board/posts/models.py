from django.db import models


class Board(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(max_length=800)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    owner = models.ForeignKey(to='members.Member', on_delete=models.CASCADE)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    body = models.TextField(max_length=800)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body
