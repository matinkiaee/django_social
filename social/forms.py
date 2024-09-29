from django import forms
from .models import *
from django.contrib.auth.forms import AuthenticationForm


class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=250, required=True, label="نام کاربری یا تلفن",
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(max_length=250, required=True, label="رمز عبور",
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    



class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(max_length=20, widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                               label='پسورد')
    password2 = forms.CharField(max_length=20, widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                                label='تکرار پسورد')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'phone']



    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('پسورد ها مطابقت ندارند!')
        return cd['password2']
    

    def clean_phone(self):
        phone=self.cleaned_data["phone"]
        if User.objects.filter(phone=phone).exists():
            raise forms.ValidationError("phone already exists")
        return phone
    


class UserEditForm(forms.ModelForm):



    class Meta:
        model=User
        fields=["first_name","last_name","phone","date_of_birth","job","bio","email","photo"]




    def clean_phone(self):
        phone=self.cleaned_data["phone"]
        if User.objects.exclude(id=self.instance.id).filter(phone=phone).exists():
            raise forms.ValidationError("phone already exists")
        return phone
    
    

    def clean_username(self):
        username=self.cleaned_data["username"] 
                                    #یوزر نیمی که کاربر وارد میکنه      یوزر نیمی که از  قبل هست
        if User.objects.exclude(id=self.instance.id).filter(username=username).exists():
            raise forms.ValidationError("username already exists")
        return username
   



class TicketForm(forms.Form):
    SUBJECT_CHOICES = (
        ('پیشنهاد', 'پیشنهاد'),
        ('انتقاد', 'انتقاد'),
        ('گزارش', 'گزارش'),
    )
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': "3"}), required=True, label='پیام')
    name = forms.CharField(max_length=250,widget=forms.TextInput(attrs={'class': 'form-control'}), required=True, label='نام')
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control'}),label='ایمیل')
    phone = forms.CharField(max_length=11,widget=forms.TextInput(attrs={'class': 'form-control'}), required=True, label='شماره تماس')
    subject = forms.ChoiceField(choices=SUBJECT_CHOICES, label='موضوع')

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if phone:
            if not phone.isnumeric():
                raise forms.ValidationError("شماره تلفن عددی نیست!")
            else:
                return phone


class CreatePostForm(forms.ModelForm):
    image1 = forms.ImageField(label="تصویر اول", required=False, widget=forms.FileInput(attrs={'class': 'form-control'}))
    image2 = forms.ImageField(label="تصویر دوم", required=False, widget=forms.FileInput(attrs={'class': 'form-control'}))
    class Meta:
        model = Post
        fields = ['description', 'tags']




class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        widgets={
            'body': forms.TextInput(attrs={
                'placeholder': 'کامنت بزارید...',
                'class':'form-control input-sm'
            }),
        }