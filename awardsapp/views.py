from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm,ProjectsForm,CommentsForm,VoteForm
from .models import User,Profile,Projects,Comments
from django.http import JsonResponse

from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import ProjectsSerializer,ProfileSerializer

from django.db.models import Max,F


# Create your views here.
@login_required(login_url='/accounts/login/')
def index(request):
    current_user = request.user
    proImages= Projects.objects.all().order_by("posted_date")
    profile= Profile.objects.all()
    
    return render(request,'all-awards/index.html',{"proImages":proImages,"profile":profile})

@login_required(login_url='/accounts/login/')
def viewProject_details(request):
    current_user = request.user
    proImage= Projects.objects.all().order_by("posted_date")
    
    profile= Profile.objects.all()
    
    return render(request,'all-awards/project.html',{"proImages":proImage,"profile":profile})


@login_required(login_url='/accounts/login/')
def project_posts(request, post_id):
    try:
        posts = Projects.objects.all().order_by('posted_date')
       
    except DoesNotExist:
        raise Http404()
    return render(request,"all-awards/project_post.html", {"posts":posts})


@login_required(login_url='/accounts/login/')
def new_post(request):
    current_user = request.user

    if request.method == 'POST':
        form = ProjectsForm(request.POST, request.FILES)
        if form.is_valid():
            projects = form.save(commit=False)
            projects.user = current_user
            projects.save()
            return redirect('index')

    else:
        form = ProjectsForm()
    return render(request, 'all-awards/post_form.html', {"form": form})

@login_required(login_url='/accounts/login/')
def profile(request,user_id  ):

    current_user = request.user.username
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = current_user
            profile.save()
            return redirect('index')

    else:
        form = ProfileForm()

    user=User.objects.all()

    proImage = Projects.objects.filter(user__username=current_user)


    profile = Profile.objects.filter(user__username = current_user)

    return render(request,"all-awards/profile.html",{"user":user,"proImages":proImage,"profile":profile})



@login_required(login_url='/accounts/login/')
def update_profile(request):

    current_user=request.user
    if request.method =='POST':
        if Profile.objects.filter(user_id=current_user).exists():
            form = ProfileForm(request.POST,request.FILES,instance=Profile.objects.get(user_id = current_user))
        else:
            form=ProfileForm(request.POST,request.FILES)
        if form.is_valid():
          profile=form.save(commit=False)
          profile.user=current_user
          profile.save()
          return redirect('profile',current_user.id)
    else:

        if Profile.objects.filter(user_id = current_user).exists():
           form=ProfileForm(instance =Profile.objects.get(user_id=current_user))
        else:
            form=ProfileForm()

    return render(request,'all-awards/profile_form.html',{"form":form}) 


def search_project(request):

    if 'project' in request.GET and request.GET["project"]:
        search_term = request.GET.get("project")
        searched_projects = Projects.search_by_proTitle(search_term)
        message = f"{search_term}"

        return render(request, 'all-awards/search.html',{"message":message,"projects": searched_projects})

    else:
        message = "You haven't searched for any term"
        return render(request, 'all-awards/search.html',{"message":message})

# def add_comment(request,projects_id):
#     current_user=request.user
    
    
#     print(current_user)
#     if request.method=='POST':
#         projects = Projects.objects.filter(id=projects_id).first()
#         form=CommentsForm(request.POST,request.FILES)
#         if form.is_valid():
#             comment=form.save(commit=False)
#             comment.posted_by=current_user
#             comment.project=projects
#             comment.save()
#             return redirect('index')
#     else:
#         form=CommentsForm()
    
#     return render(request,'all-awards/comment_form.html',{"form":form,"projects_id":projects_id})

# def view_comments(request):
#     current_user = request.user
#     projects = Projects.objects.filter(id=projects_id).first()
#     comments=Comments.objects.filter(user__username= current_user)
#     return render(request,'all-awards/comment.html',{"comments":comments,"projects":projects})


@login_required(login_url='/accounts/login/')
def rating(request,id):
  project=Projects.objects.get(id=id)
  rating = round(((project.design + project.usability + project.content)/3),1)
  if request.method == 'POST':
      form = VoteForm(request.POST)
      if form.is_valid:
          project.vote_submissions += 1
          if project.design == 0:
              project.design = int(request.POST['design'])
          else:
              project.design = (project.design + int(request.POST['design']))/2
          if project.usability == 0:
              project.usability = int(request.POST['usability'])
          else:
              project.usability = (project.design + int(request.POST['usability']))/2
          if project.content == 0:
              project.content = int(request.POST['content'])
          else:
              project.content = (project.design + int(request.POST['content']))/2
          project.save()
          return redirect('index')
  else:
      form = VoteForm()
  return render(request,'all-awards/vote.html',{'form':form,'projects':project,'rating':rating})


#......

# def news_today(request):
#     date = dt.date.today()
#     news = Article.todays_news()
#     form = NewsLetterForm()
#     return render(request, 'all-news/today-news.html', {"date": date, "news": news, "letterForm": form})

# #.........

# def newsletter(request):
#     name = request.POST.get('your_name')
#     email = request.POST.get('email')

#     recipient = NewsLetterRecipients(name=name, email=email)
#     recipient.save()
#     send_welcome_email(name, email)
#     data = {'success': 'You have been successfully added to mailing list'}
#     return JsonResponse(data)

class ProjectsList(APIView):
    def get(self, request, format=None):
        all_projects = Projects.objects.all()
        serializers = ProjectsSerializer(all_projects, many=True)
        return Response(serializers.data)


class ProfileList(APIView):
    def get(self, request, format=None):
        all_profile = Profile.objects.all()
        serializers = ProfileSerializer(all_profile, many=True)
        return Response(serializers.data)