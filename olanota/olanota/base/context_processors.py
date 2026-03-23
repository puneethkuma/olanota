from .models import Ads,SiteSettings,Tag,News
from django.db.models import Sum

def ads_context(request):
    left_ads=Ads.objects.filter(is_active=True,ads_type="Left")
    right_ads=Ads.objects.filter(is_active=True,ads_type="Right")
    slider_ads=Ads.objects.filter(is_active=True,ads_type="Slider")
    top_ads=Ads.objects.filter(is_active=True,ads_type="Top").last()
    ad1=Ads.objects.filter(is_active=True,ads_type="Ad1").last()
    ad2=Ads.objects.filter(is_active=True,ads_type="Ad2").last()
    ad3=Ads.objects.filter(is_active=True,ads_type="Ad3").last()
    ad4=Ads.objects.filter(is_active=True,ads_type="Ad4").last()
    ad5=Ads.objects.filter(is_active=True,ads_type="Ad5").last()
    tags=Tag.objects.all().order_by("-id")[:20]
    settings = SiteSettings.objects.first()
    last_four=News.objects.all().order_by('-id')[:4]
    total_visitors = News.objects.aggregate(total=Sum('visitor_count'))['total'] or 0

    return {
        'total_visitors':total_visitors,
        'last_four':last_four,
        'left_ads':left_ads,
        'right_ads':right_ads,
        'slider_ads':slider_ads,
        'top_ads':top_ads,
        'ads1':ad1,
        'ads2':ad2,
        'ads3':ad3,
        'ads4':ad4,
        'ads5':ad5,
        'tags':tags,
        'settings':settings,
     
    }
