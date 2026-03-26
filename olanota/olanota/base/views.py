from .models import News,Youtube,Ads,Comment,Job,SiteSettings,Author,Tag,User,Comment,NewsVisit
from django.utils import timezone

from .forms import NewsForm,AdsForm,CommentForm,YoutubeForm,JobForm,AuthorRegisterForm,ProfileEditForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.contrib import messages
from django.db.models import Q

from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from django.urls import reverse
from django.contrib.auth import login
from django.db.models import Sum


def register_author(request):
    if request.method == 'POST':
        form = AuthorRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data.get('email')
            user.is_staff = True        

            user.save()

            # Create linked Author profile
            Author.objects.create(
                user=user,
                profile_image=form.cleaned_data.get('profile_image'),
                bio=form.cleaned_data.get('bio'),
                email=form.cleaned_data.get('email'),
                phone=form.cleaned_data.get('phone')
            )

            messages.success(request, 'Registration successful!')
            return redirect('base:dashboard')  # Replace with your dashboard route
    else:
        form = AuthorRegisterForm()

    return render(request, 'dashboard/register_author.html', {'form': form})

class LatestNewsFeed(Feed):
    title = "Olanota News"
    link = "/news/"
    description = "Latest news from olanota News"
    
    # RSS items
    def items(self):
        return News.objects.filter(is_active=True).order_by('-Date')[:20]

    def item_title(self, item):
        return item.Title

    def item_description(self, item):
        author_name = item.author.user.get_full_name() if item.author else "Unknown"
        return f"{item.Sub_heading} - Author: {author_name}"
    
    def item_link(self, item):
        return reverse('base:detail', kwargs={'slug': item.slug, 'pk': item.pk})

    def item_pubdate(self, item):
        return item.Date

    def item_enclosure_url(self, item):
        if item.Image_1:
            return item.Image_1.url
        return None

    def item_enclosure_length(self, item):
        return 0

    def item_enclosure_mime_type(self, item):
        return 'image/jpeg'

def home(request):
  objects5 = News.objects.all().order_by('-id')[:8][4:]  
  objects9 = News.objects.all().order_by('-id')[:12][8:]  
  Politicalc=News.objects.filter(Category="Political").order_by('-pk')[:4]
  Crimec=News.objects.filter(Category="Crime").order_by('-pk')[:4]
  Localc=News.objects.filter(Category="Local").order_by('-pk')[:6]
  Statec=News.objects.filter(Category="State").order_by('-pk')[:6]
  Centralc=News.objects.filter(Category="Central").order_by('-pk')[:4]
  Centralc1=News.objects.filter(Category="Central").order_by('-pk')[:1]
  youtube=Youtube.objects.all().order_by('-id')[:4]

  context= {
            'objects5':objects5,
            'objects9':objects9,
            'Politicalc':Politicalc,
            'Crimec':Crimec,
            'Localc':Localc,
            'Statec':Statec,
            'Centralc':Centralc,
            'Centralc1':Centralc1,
            'youtube':youtube,
            
            }
  return render(request, "home.html",context)

def detail(request,slug, pk):
  pr = News.objects.filter(pk__gt=pk).order_by('pk').first()
  nx = News.objects.filter(pk__lt=pk).order_by('-pk').first()
  news_detail = News.objects.get(pk=pk)
  objects5 = News.objects.all().order_by('-id')[:8][4:]
  objects9 = News.objects.all().order_by('-id')[:12][8:]
  comments = news_detail.comments.filter(is_approved=True)
  ads = Ads.objects.filter(ads_type="Details")
  news_detail.visitor_count += 1
  news_detail.save(update_fields=['visitor_count'])
  related_posts = News.objects.filter(
        Q(Category=news_detail.Category) | Q(tags__in=news_detail.tags.all()),
        is_active=True
    ).exclude(id=news_detail.id).distinct()[:6] 
  
  today = timezone.now().date()
  visit, created = NewsVisit.objects.get_or_create(news=news_detail, date=today)
  visit.count += 1
  visit.save(update_fields=['count'])
  
  if request.method == "POST":
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.news = news_detail
        comment.save()
        return redirect("base:detail",slug=slug, pk=pk)
  else:
    form = CommentForm()

  context = {
    'news_detail': news_detail,
    'related_posts':related_posts,
    'pr': pr,
    'nx': nx,
    'objects9': objects9,
    'objects5': objects5,
    'form':form,
    'comments':comments,
    'ads':ads,
  }
  return render(request, "details.html", context)

def list(request):
  all_post=News.objects.filter(is_active=True)
  cat = request.GET.get('cat')
  loc = request.GET.get('loc')
  query = request.GET.get('q', '').strip()

  if query:
       all_post = all_post.filter(
            Q(Title__icontains=query) |
            Q(Sub_heading__icontains=query) |
            Q(Description__icontains=query) |
            Q(Location__icontains=query) |
            Q(Category__icontains=query) |
            Q(author__user__username__icontains=query) |
            Q(author__user__first_name__icontains=query) |
            Q(author__user__last_name__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct()
  if cat:
    all_post=News.objects.filter(Category=loc).order_by('-id')
  if loc:
    all_post=News.objects.filter(Location=cat).order_by('-id')  
  p = Paginator(all_post, 15)  
  page_number = request.GET.get('page')
  try:
    page_obj = p.get_page(page_number)  
  except PageNotAnInteger:
    page_obj = p.page(1)
  except EmptyPage:
    page_obj = p.page(p.num_pages)
  objects9 = News.objects.all().order_by('-id')[:13][9:]  
  objects5 = News.objects.all().order_by('-id')[:9][5:]
  context= {
    
    
    'objects9':objects9,
    'objects5':objects5,
    'all_post':page_obj,
    }
  return render(request, "list.html",context)

def contact(request):

  return render(request, "contact.html")

def about(request):

  return render(request, "about.html")

def superuser_required(view_func):
  decorated_view_func = user_passes_test(lambda u: u.is_superuser)(view_func)
  return decorated_view_func

def staff_required(view_func):
    decorated_view_func = user_passes_test(lambda u: u.is_staff)(view_func)
    return decorated_view_func

def as_view(request):
    logout(request)
    messages.info(request, "Logout Success")
    return redirect("accounts:login")

@staff_required
def dashboard(request):
    data = (
        NewsVisit.objects.values('date')
        .annotate(total_visitors=Sum('count'))
        .order_by('date')
    )

    # Format data for chart.js
    dates = [entry['date'].strftime('%Y-%m-%d') for entry in data]
    totals = [entry['total_visitors'] for entry in data]

    context = {
        'dates': dates,
        'totals': totals,
         "total_news": News.objects.count(),
        "total_ads": Ads.objects.count(),
        "total_jobs": Job.objects.count(),
        "total_videos": Youtube.objects.count(),
        "total_author": Author.objects.count(),
        
    }
#side bar
    return render(request, "dashboard/dashboard.html", context)

def news_visitor_chart(request, pk):
    news = get_object_or_404(News, pk=pk)

    # Get total visitors of this particular news grouped by date
    data = (
        NewsVisit.objects.filter(news=news)
        .values('date')
        .annotate(total_visitors=Sum('count'))
        .order_by('date')
    )

    # Prepare data for chart.js
    dates = [entry['date'].strftime('%Y-%m-%d') for entry in data]
    totals = [entry['total_visitors'] for entry in data]

    context = {
        'news': news,
        'dates': dates,
        'totals': totals,
    }
    return render(request, 'dashboard/news_visitor_chart.html', context)

@staff_required
def news_list(request):
  if request.user.is_superuser:
   post = News.objects.all().order_by('-id')
  else: 
   post = News.objects.filter(author=Author.objects.get(user=request.user)).order_by('-id')
  context = {
  'post': post,
  }
  return render(request, "dashboard/news_list.html", context)


@staff_required
def add_news(request):
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            news = form.save(commit=False)
            news.author = Author.objects.get(user=request.user)
            news.save()

            # Handle tags (unique + reuse existing)
            tags_text = form.cleaned_data.get('tags', '')
            if tags_text:
                tag_names = [t.strip().lower() for t in tags_text.split(',') if t.strip()]
                unique_names = set(tag_names)  # avoid duplicates in one submission

                for name in unique_names:
                    tag, created = Tag.objects.get_or_create(name__iexact=name, defaults={'name': name})
                    news.tags.add(tag)

            messages.success(request, "✅ News added successfully with unique tags")
            return redirect('base:news_list')
    else:
        form = NewsForm()

    return render(request, "dashboard/add_news.html", {'form': form})




@superuser_required
def delete_news(request, pk):
  current_record = News.objects.get(id=pk)
  current_record.delete()
  messages.success(request, "News Deleted Successfully")
  return redirect('base:news_list')


@staff_required
def add_ads(request):
  if request.method == 'POST':
    form = AdsForm(request.POST, request.FILES)
    if form.is_valid():
      form.save()
      messages.success(request, "Ads Added Successfully")
      return redirect('base:ads_list')
  else:
    form = AdsForm()
  context = {
  'form': form,
  }
  return render(request, "dashboard/add_ads.html", context)

@staff_required
def edit_ads(request, pk):
  current_record = Ads.objects.get(id=pk)
  form = AdsForm( instance=current_record)
  if request.method=="POST":
    form = AdsForm(request.POST or None, request.FILES, instance=current_record)
    if form.is_valid():
      form.save()
      messages.success(request, "Saved Success")
    return redirect('base:ads_list')  
  return render(request, 'dashboard/add_ads.html', {'form': form})

@staff_required
def edit_news(request, pk):
  current_record = News.objects.get(id=pk)
  form = NewsForm( instance=current_record)
  if request.method=="POST":
    form = NewsForm(request.POST or None, request.FILES, instance=current_record)
    if form.is_valid():
      form.save()
      messages.success(request, "News Updated Successfully")
    return redirect('base:dashboard')  
  return render(request, 'dashboard/add_news.html', {'form': form})

@staff_required
def ads_list(request):
  ads = Ads.objects.all()
  context = {
  'ads': ads,
  }
  return render(request, "dashboard/ads_list.html", context)

@staff_required
def slider_ads_list(request):
  ads = Ads.objects.filter(ads_type="Slider")
  context = {
  'ads': ads,
  }
  return render(request, "dashboard/ads_list.html", context)

@staff_required
def left_ads_list(request):
  ads = Ads.objects.filter(ads_type="Left")
  context = {
  'ads': ads,
  }
  return render(request, "dashboard/ads_list.html", context)

@staff_required
def right_ads_list(request):
  ads = Ads.objects.filter(ads_type="Right")
  context = {
  'ads': ads,
  }
  return render(request, "dashboard/ads_list.html", context)

@staff_required
def top_ads_list(request):
  ads = Ads.objects.filter(ads_type="Top")
  context = {
  'ads': ads,
  }
  return render(request, "dashboard/ads_list.html", context)

@staff_required
def details_ads_list(request):
  ads = Ads.objects.filter(ads_type="Details")
  context = {
  'ads': ads,
  }
  return render(request, "dashboard/ads_list.html", context)


@staff_required
def center_ads_list(request):
  ads = Ads.objects.filter(ads_type__in=["Ad1", "Ad2", "Ad3", "Ad4", "Ad5"])
  context = {
  'ads': ads,
  }
  return render(request, "dashboard/ads_list.html", context)  

@staff_required
def youtube_list(request):
  youtube = Youtube.objects.filter(is_active=True).order_by('-id')
  context = {
  'youtube': youtube,
  }
  return render(request, "dashboard/youtube_list.html", context)


@staff_required
def add_youtube(request):
  if request.method == 'POST':
    form = YoutubeForm(request.POST, request.FILES)
    if form.is_valid():
      form.save()
      messages.success(request, "Video Added Successfully")
      return redirect('base:youtube_list')
  else:
    form = YoutubeForm()
  context = {
  'form': form,
  }
  return render(request, "dashboard/add_youtube.html", context)


@staff_required
def edit_youtube(request, pk):
  current_record = Youtube.objects.get(id=pk)
  form = YoutubeForm( instance=current_record)
  if request.method=="POST":
    form = YoutubeForm(request.POST or None, request.FILES, instance=current_record)
    if form.is_valid():
      form.save()
      messages.success(request, "Saved Success")
    return redirect('base:youtube_list')  
  return render(request, 'dashboard/add_youtube.html', {'form': form})

@staff_required
def delete_youtube(request, pk):
  current_record = Youtube.objects.get(id=pk)
  current_record.delete()
  messages.success(request, "News Deleted Successfully")
  return redirect('base:youtube_list')


def youtube(request):
  youtube=Youtube.objects.all().order_by('-id')
  context = {
  'youtube': youtube,
  
  }
  return render(request, "youtube.html", context)


#############

@staff_required
def add_job(request):
    if request.method == 'POST':

        form = JobForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('base:list_job')  
    else:
        form = JobForm()
    return render(request, 'dashboard/add_job.html', {'form': form})


#list of job
@staff_required
def list_job(request):
    post= Job.objects.all().order_by("-id")
    return render(request, 'dashboard/job_list.html', {'post': post})

#delete job
@staff_required
def delete_job(request, pk):
  current_record = Job.objects.get(id=pk)
  current_record.delete()
  messages.success(request, "News Deleted Successfully")
  return redirect('base:list_job')

#edit job

@staff_required
def edit_job(request, pk):
  current_record = Job.objects.get(id=pk)
  form = JobForm( instance=current_record)
  if request.method=="POST":
    form = JobForm(request.POST or None, request.FILES, instance=current_record)
    if form.is_valid():
      form.save()
      messages.success(request, "Saved Success")
    return redirect('base:Job_list')  
  return render(request, 'dashboard/add_job.html', {'form': form})


def job(request):
      post= Job.objects.filter(is_active=True).order_by("-id")
      context = {
      'post': post,
      
      }
      return render(request, 'job.html', context)

def job_details(request, pk):
  post = Job.objects.get(id=pk)
  context = {
      'post': post,
      
      }
  return render(request, 'job_details.html', context)

def tags(request):
  tags=Tag.objects.all().order_by('-id')
  context={
    'tags':tags,
    }
  return render(request, "tags.html",context)

def tc(request):

  return render(request, "tc.html")

def pp(request):

  return render(request, "pp.html")


SOCIAL_FIELDS = [
    'facebook_link', 'instagram_link', 'x_link', 'linkedin_link', 'youtube_link',
    'telegram_link', 'whatsapp_link', 'threads_link', 'snapchat_link', 'pinterest_link',
    'tiktok_link', 'reddit_link', 'discord_link', 'github_link', 'dribbble_link',
    'behance_link', 'arattai_link', 'email', 'phone_number'
]

TOGGLE_FIELDS = ['show_jobs', 'show_youtube']  # example toggles

@superuser_required
def dashboard_settings(request):
    settings, created = SiteSettings.objects.get_or_create(id=1)

    if request.method == 'POST':
        # Update toggle fields
        for toggle in TOGGLE_FIELDS:
            setattr(settings, toggle, toggle in request.POST)

        # Update social media / contact fields
        for field in SOCIAL_FIELDS:
            value = request.POST.get(field, '').strip()
            setattr(settings, field, value if value else None)

        settings.save()
        return redirect('base:dashboard')

    context = {
    'settings': settings,
    'social_fields': SOCIAL_FIELDS,
    'toggle_fields': TOGGLE_FIELDS
    }
    return render(request, 'dashboard/settings.html', context)

def author_details(request,pk):
    author=Author.objects.get(pk=pk)
    post=News.objects.filter(author=author)
    total_news = len(post)
    context={
       'author':author,
       'post':post,
       'total_news':total_news,
    }
    return render(request, 'author-news.html', context)
   



# profile of author
@staff_required
def profile_detail(request,pk):
  if request.user.is_superuser or request.user.pk == pk:  
    author=Author.objects.get(user=pk)
    form = ProfileEditForm( instance=author)
    print(form)
    context={
       'author':author,
       'form':form,
    
    }
    return render(request, 'dashboard/profile.html', context)

  #list

@superuser_required
def author_list(request):
    author=Author.objects.all().order_by("-id")
    context={
       'author':author,
    
    }
    return render(request, 'dashboard/profile-list.html', context)  

@staff_required
def password_reset(request,pk):
    user_obj = get_object_or_404(User, pk=pk)

    if not (request.user.is_superuser or request.user.pk == pk):
        messages.error(request, "You are not authorized to reset this password.")
        return redirect('base:password_reset', pk=pk)

    if request.method == "POST":
        password = request.POST.get('pass')
        confirm_password = request.POST.get('confirm_pass')

        if not password:
            messages.error(request, "Password cannot be empty.")
            return redirect('base:password_reset', pk=pk)

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('base:password_reset', pk=pk)

        user_obj.set_password(password)
        user_obj.save()
        messages.success(request, "Password reset successful.")


        if request.user.is_superuser:
            return redirect('base:profile_detail', pk=pk)
        else:
            
            logout(request)
            return redirect('base:login')
    return redirect('base:profile_detail', pk=pk)

@staff_required
def edit_profile(request,pk):
  if request.method=="POST":
    current_record=Author.objects.get(user=pk)
    form = ProfileEditForm(request.POST or None, request.FILES, instance=current_record)
    if form.is_valid():
      form.save()
      messages.success(request, "Saved Success")
      return redirect('base:profile_detail', pk=pk)
    else:
      print(form.errors)
      messages.warning(request, "Enter Valid Values")
      return redirect('base:profile_detail', pk=pk)

@superuser_required
def delete_user(request, pk):
    user_to_delete = get_object_or_404(User, pk=pk)
    username = user_to_delete.username
    user_to_delete.delete()
    messages.success(request, f"User '{username}' has been deleted successfully.")
    return redirect('base:author_list')
  
@superuser_required
def comment_list(request):
  post=Comment.objects.all().order_by("-id")
  context={
       'post':post,
    
    }
  return render(request, 'dashboard/comment.html', context)  

@superuser_required
def delete_comment(request, pk):
    delete = get_object_or_404(Comment, pk=pk)
    delete.delete()
    messages.success(request, f"Comment been deleted successfully.")
    return redirect('base:comment_list')

# table design

  # news

  # youtube

  # comment
  # job
  # profile

# Details - 20
# Slider - 10
# Left - 5
# Right - 5

# Top - 1
# Ad1 - 1
# Ad2 - 1
# Ad3 - 1
# Ad4 - 1
# Ad5 - 1