from django import forms
from projectapp.models import Post
from projectapp.models import Student


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = "__all__"
        # fields = ["name", "body"]

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ["first_name", "last_name", "phone_number", "description"]