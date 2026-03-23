from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse

# ------------------------------
# Choices for News Category
# ------------------------------
category_choices = (
  ("Political", "Political"),
    ("Crime", "Crime"),
    ("Local", "Local"),
    ("State", "State"),
    ("Central", "Central"),
    ("World", "World"),
    ("Business", "Business"),
    ("Technology", "Technology"),
    ("Sports", "Sports"),
    ("Entertainment", "Entertainment"),
    ("Education", "Education"),
    ("Health", "Health"),
    ("Environment", "Environment"),
    ("Science", "Science"),
    ("Travel", "Travel"),
    ("Lifestyle", "Lifestyle"),
    ("Culture", "Culture"),
    ("Weather", "Weather"),
    ("Opinion", "Opinion"),
    ("Others", "Others"),
)



Location_choices=(
("India" , "India"),
("Andhra Pradesh" , "Andhra Pradesh"),
("Arunachal Pradesh" , "Arunachal Pradesh"),
("Assam" , "Assam"),
("Bihar", "Bihar"),
("Chhattisgarh", "Chhattisgarh"),
("Goa", "Goa"),
("Gujarat","Gujarat"),
("Haryana","Haryana"),
("Himachal Pradesh","Himachal Pradesh"),
("Jharkhand","Jharkhand"),
("Karnataka","Karnataka"),
("Kerala","Kerala"),
("Madhya Pradesh","Madhya Pradesh"),
("Maharashtra","Maharashtra"),
("Manipur","Manipur"),
("Meghalaya","Meghalaya"),
("Mizoram","Mizoram"),
("Nagaland","Nagaland"),
("Odisha","Odisha"),
("Punjab","Punjab"),
("Rajasthan","Rajasthan"),
("Sikkim","Sikkim"),
("Tamil Nadu","Tamil Nadu"),
("Telangana","Telangana"),
("Tripura","Tripura"),
("Uttar Pradesh","Uttar Pradesh"),
("Uttarakhand","Uttarakhand"),
("West Bengal","West Bengal"),
("Kerala" ,"Kerala"),
("Alappuzha","Alappuzha"),
("Ernakulam","Ernakulam"),
("Idukki","Idukki"),
("Kannur","Kannur"),
("Kasaragod","Kasaragod"),
("Kollam","Kollam"),
("Kottayam","Kottayam"),
("Kozhikode","Kozhikode"),
("Malappuram","Malappuram"),
("Palakkad","Palakkad"),
("Pathanamthitta","Pathanamthitta"),
("Thiruvananthapuram","Thiruvananthapuram"),
("Thrissur","Thrissur"),
("Wayanad","Wayanad"),
("Karnataka","Karnataka"),
("Bagalkote","Bagalkote"),
("Ballari","Ballari"),
("Belagavi","Belagavi"),
("Bengaluru Rural","Bengaluru Rural"),
("Bengaluru Urban","Bengaluru Urban"),
("Bidar","Bidar"),
("Chamarajanagara","Chamarajanagara"),
("Chikkaballapura","Chikkaballapura"),
("Chikkamagaluru","Chikkamagaluru"),
("Chitradurga","Chitradurga"),
("Dakshina Kannada","Dakshina Kannada"),
("Davanagere","Davanagere"),
("Dharwad","Dharwad"),
("Gadag","Gadag"),
("Hassan","Hassan"),
("Haveri","Haveri"),
("Kalaburagi","Kalaburagi"),
("Kodagu","Kodagu"),
("Kolar","Kolar"),
("Koppal","Koppal"),
("Mandya","Mandya"),
("Mysuru","Mysuru"),
("Raichur","Raichur"),
("Ramanagara","Ramanagara"),
("Shivamogga","Shivamogga"),
("Tumakuru","Tumakuru"),
("Udupi","Udupi"),
("Uttara Kannada","Uttara Kannada"),
("Vijayanagara","Vijayanagara"),
("Vijayapura","Vijayapura"),
("Yadgiri","Yadgiri"),
)


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='authors/', blank=True, null=True)
    bio = models.TextField(blank=True)
    email=models.EmailField( max_length=254, blank=True, null=True)
    phone=models.CharField( max_length=254, blank=True, null=True)
    # social_links = models.JSONField(blank=True, null=True)  # optional: {"facebook": "...", "twitter": "..."}

    def __str__(self):
        return self.user.get_full_name() or self.user.username
    
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=60, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

# ------------------------------
# News Model
# ------------------------------
class News(models.Model):
    Title = models.CharField(max_length=255)
    Sub_heading = models.TextField(blank=True, default="")
    Description = models.TextField()
    Location = models.CharField(max_length=255, blank=True, default="",choices=Location_choices)
    Date = models.DateTimeField(auto_now_add=True, blank=True)
    Category = models.CharField(max_length=20, choices=category_choices, default="Political")

    Image_1 = models.ImageField(upload_to='upload/')
    Image_2 = models.ImageField(upload_to='upload/', blank=True, null=True)
    Image_3 = models.ImageField(upload_to='upload/', blank=True, null=True)
    Image_4 = models.ImageField(upload_to='upload/', blank=True, null=True)
    Image_5 = models.ImageField(upload_to='upload/', blank=True, null=True)
    Image_6 = models.ImageField(upload_to='upload/', blank=True, null=True)
    display_author=models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True,blank=True, related_name='articles')
    tags = models.ManyToManyField(Tag,blank=True)
    slug = models.SlugField(max_length=255, blank=True, null=True)
    
    visitor_count = models.PositiveIntegerField(default=0)

 
    class Meta:
        verbose_name = "News"
        verbose_name_plural = "News"

    def _str_(self):
        return self.Title


class NewsVisit(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='visits')
    date = models.DateField(auto_now_add=True)
    count = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('news', 'date')

    def __str__(self):
        return f"{self.news.Title} - {self.date} ({self.count})"
    
# ------------------------------
# Youtube Model
# ------------------------------
class Youtube(models.Model):
    youtube_url = models.TextField()
    title = models.CharField(max_length=200, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    class Meta:
        verbose_name = "Youtube"
        verbose_name_plural = "Youtube"

    def _str_(self):
        return self.youtube_url

# ------------------------------
# Add Model
# ------------------------------
ADS_TYPES = (
    ('Details', 'Details'),
    ('Left', 'Left'),
    ('Right', 'Right'),
    ('Slider', 'Slider'),
    ('Top', 'Top'),
    ('Ad1', 'Ad1'),
    ('Ad2', 'Ad2'),
    ('Ad3', 'Ad3'),
    ('Ad4', 'Ad4'),
    ('Ad5', 'Ad5'),
)
class Ads(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True)
    link = models.URLField(max_length=500, blank=True, null=True)
    image = models.ImageField(upload_to='uploads/ads', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    ads_type = models.CharField(max_length=50, choices=ADS_TYPES, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



    def __str__(self):
        return str(f'{self.title} - {self.ads_type}')
    

class Comment(models.Model):
    news = models.ForeignKey(News, related_name="comments", on_delete=models.CASCADE)
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    name=models.CharField(max_length=50,blank=True)
    email=models.CharField(max_length=50,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_approved = models.BooleanField(default=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.news.Title}"
    

EMPLOYMENT_TYPES = [
    ('Full-time', 'Full-time'),
    ('Part-time', 'Part-time'),
    ('Internship', 'Internship'),
    ('Contract', 'Contract'),
]

class Job(models.Model):
    title = models.CharField(max_length=255)
    location = models.CharField(max_length=100)
    experience = models.CharField(max_length=50)
    employment_type = models.CharField(max_length=50, choices=EMPLOYMENT_TYPES)
    about_role = models.TextField()
    responsibilities = models.TextField(help_text="Use line breaks for each responsibility.")
    skills = models.TextField(help_text="Use line breaks for each skill.")
    qualifications = models.TextField(help_text="Use line breaks for each qualification.")
    benefits = models.TextField(help_text="Use line breaks for each benefit.")
    email = models.EmailField()
    apply_link = models.URLField(blank=True, null=True)
    deadline = models.DateField()
    is_active=models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_responsibilities_list(self):
        return [r.strip() for r in self.responsibilities.split('\n') if r.strip()]

    def get_skills_list(self):
        return [s.strip() for s in self.skills.split('\n') if s.strip()]

    def get_qualifications_list(self):
        return [q.strip() for q in self.qualifications.split('\n') if q.strip()]

    def get_benefits_list(self):
        return [b.strip() for b in self.benefits.split('\n') if b.strip()]

    def __str__(self):
        return self.title    
    


class SiteSettings(models.Model):
    show_jobs = models.BooleanField(default=True)
    show_youtube = models.BooleanField(default=True)
    facebook_link = models.URLField(blank=True, null=True)
    instagram_link = models.URLField(blank=True, null=True)
    x_link = models.URLField(blank=True, null=True) 
    linkedin_link = models.URLField(blank=True, null=True)
    youtube_link = models.URLField(blank=True, null=True)
    telegram_link = models.URLField(blank=True, null=True)
    whatsapp_link = models.URLField(blank=True, null=True)
    threads_link = models.URLField(blank=True, null=True)
    snapchat_link = models.URLField(blank=True, null=True)
    pinterest_link = models.URLField(blank=True, null=True)
    # tiktok_link = models.URLField(blank=True, null=True)
    reddit_link = models.URLField(blank=True, null=True)
    discord_link = models.URLField(blank=True, null=True)
    github_link = models.URLField(blank=True, null=True)
    dribbble_link = models.URLField(blank=True, null=True)
    behance_link = models.URLField(blank=True, null=True)
    arattai_link = models.URLField(blank=True, null=True) 
    email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return "Website Settings"

    class Meta:
        verbose_name_plural = "Site Settings"





