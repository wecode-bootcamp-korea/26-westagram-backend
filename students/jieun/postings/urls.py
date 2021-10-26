from django.urls    import path
from postings.views import PostingListView, CommentListView

app_name = 'postings'
urlpatterns = [
    path('', PostingListView.as_view()),
    path('/<int:id>/comments', CommentListView.as_view()),
]