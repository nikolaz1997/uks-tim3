from django.shortcuts import render
from django.shortcuts import redirect
from app_models.issue import Issue
from app_models.pull_request import PullRequest
from app_models.label import Label
from app_models.enums import IssueStatus
from app_models.enums import PullRequestStatus
from django.db.models import Value, IntegerField

from user_auth.forms import SignInForm
from .forms import UserForm
from app_models.models import User

from django.contrib.contenttypes.models import ContentType


def index(request):

    if request.user.is_authenticated:
        # Get the currently logged-in user
        user = request.user
        # Render a template with the user information
        return render(request, 'index.html', {'user': user})
    else:
        # Render template for log in
        form = SignInForm()
        return render(request, 'sign_in.html', {'form': form})

def profile(request):
    print(request)
    if request.user.is_authenticated:
        # Get the currently logged-in user
        if request.method == "POST":
            user = User.objects.get(id=request.user.id)
            user.delete()            
            return redirect('logout')
        else:
            user = request.user
            # Render a template with the user information
            profile = User.objects.filter(username=user.username)[0]
            return render(request, 'profile.html', {'user': user, 'profile': profile})
    else:
        # Render template for log in
        form = SignInForm()
        return render(request, 'sign_in.html', {'form': form})
 
def edit_profile(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = UserForm(request.POST)
            if form.is_valid():
                firstName = form.cleaned_data['firstName']
                lastName = form.cleaned_data['lastName']
                bio = form.cleaned_data['bio']
                company = form.cleaned_data['company']
                website = form.cleaned_data['website']
                user = User.objects.update(username=request.user.username,firstName=firstName, lastName=lastName, bio=bio, company=company, website=website)
                return redirect('profile')
        else:
            form = UserForm()
            return render(request, 'edit_profile.html', {'form': form})
    else:
        # Render template for log in
        form = SignInForm()
        return render(request, 'sign_in.html', {'form': form})
    
     
def issues(request):
    user = request.user
    query = request.GET.get('search-issues')
    
    filterMap = getFilterMap(query)
    filters = getObjectFilters(filterMap)

    objects = getFilteredQuerySet(Issue.objects, filters).all()
    opened_issues = list(filter(lambda issue: issue.state.value == 'OPENED', objects))
    closed_issues = list(filter(lambda issue: issue.state.value == 'CLOSED', objects))

    return render(request, 
        'issues.html', 
        {   
            'user': user, 
            'opened_issues': opened_issues, 
            "opened_issues_num": len(opened_issues), 
            "closed_issues": closed_issues, 
            "closed_issues_num": len(closed_issues),
            "is_opened": filterMap.get('is') == 'opened'
        })

def pulls(request):
    user = request.user
    query = request.GET.get('search-issues')
    
    filterMap = getFilterMap(query)
    filters = getObjectFilters(filterMap)

    objects = getFilteredQuerySet(PullRequest.objects, filters).all()
    opened_pulls = list(filter(lambda issue: issue.state.value == 'OPENED', objects))
    closed_pulls = list(filter(lambda issue: issue.state.value == 'CLOSED', objects))
    
    return render(request, 
        'pull_requests.html', 
        {   
            'user': user, 
            'opened_pulls': opened_pulls, 
            "opened_pulls_num": len(opened_pulls), 
            "closed_pulls": closed_pulls, 
            "closed_pulls_num": len(closed_pulls),
            "is_opened": filterMap.get('is') == 'opened'
        })


def getFilterMap(query):
    filterMap = {}
    if query != None:
        query_array = query.split(' ')

        for item in query_array:
            params = item.split(':')
            if params[0] == "is":
                if params[1] == 'pr' or params[1] == 'issue':
                    filterMap['type'] = params[1]
            if params[0] == 'author':
                filterMap['creator__username'] = params[1]
            if params[0] == 'assignee':
                filterMap['asignee__username'] = params[1]
    
    return filterMap

def getObjectFilters(filterMap):
    filters = []
    for key in filterMap:
        filters.append({ 'key': key, 'value': filterMap.get(key)})
    return filters
        

def getFilteredQuerySet(objectType, filters):
    querySet = objectType
    for filter in filters:
        filtered_by = filter['key']
        filter_value = filter['value']
        querySet = querySet.filter(**{filtered_by: filter_value})

    return querySet

    
def getLabels(issues):
    for issue in issues:
        content_type = ContentType.objects.get_for_model(Label)
        model_class = content_type.model_class()

        labels = model_class.objects.filter(pk=issue.id).all()
        issue.labels = labels
