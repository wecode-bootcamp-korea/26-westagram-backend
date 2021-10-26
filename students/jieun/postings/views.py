import json

from django.http        import JsonResponse
from django.views       import View

from core.utils         import login_required, posting_existed
from postings.models    import Posting, Comment

class PostingListView(View):
    def get(self, request):
        results = [
            {
                'user'    : posting.user.name,
                'content' : posting.content,
                'url'     : posting.url,
                'date'    : posting.created_at
            }
            for posting in Posting.objects.all()
        ]
        return JsonResponse({'results' : results}, status=200)
    
    @login_required
    def post(self, request):
        data = json.loads(request.body)

        try:
            Posting.objects.create(
                user_id  = request.user.id,
                content  = data['content'], 
                url      = data['url']
            )
            return JsonResponse({'message' : 'SUCCESS'}, status=201)
       
        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)


class CommentListView(View):
    @posting_existed
    def get(self, request, id):
        results = [
            {
                'posting_id' : id,
                'content'    : comment.content,
                'date'       : comment.updated_at,
            }
            for comment in Comment.objects.filter(posting_id=id)
        ]
        return JsonResponse({'results' : results}, status=200)

    @login_required
    @posting_existed
    def post(self, request, id):
        data = json.loads(request.body)

        try:
            Comment.objects.create(
                posting_id   = id,
                user_id      = request.user.id,
                content      = data['content'],
            )
            return JsonResponse({'message': 'SUCCESS'}, status=201)
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)