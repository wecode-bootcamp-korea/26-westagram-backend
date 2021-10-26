from django.db    import models
class Posting(models.Model):
    user         = models.ForeignKey('users.User', on_delete=models.CASCADE)
    content      = models.CharField(max_length=2000)
    url          = models.URLField()
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'postings'

class Comment(models.Model):
    user         = models.ForeignKey('users.User', on_delete=models.CASCADE)
    posting      = models.ForeignKey('Posting', on_delete=models.CASCADE)
    content      = models.CharField(max_length=2000)
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'comments'