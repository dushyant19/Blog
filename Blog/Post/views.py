from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect,Http404
from .models import Post
from django.urls import reverse
from .forms import CreatePost
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models.signals import pre_save
from django.utils.text import slugify
from urllib.parse import quote_plus
# Create your views here.

def Create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    form=CreatePost(request.POST or None,request.FILES or None)
    context={'form':form}
    if form.is_valid():
        form.save(commit=False)
        form.save()
        messages.success(request,'Post Created Successfully')
        return HttpResponseRedirect(reverse('Post:list'))
    return render(request,'create_form.html',context)

def List(request):
    queryset=Post.objects.all().order_by("-timestamp")
    context_dict={'title':'List','object_list':queryset}
    #if request.user.is_authenticated:
    #    context_dict={'title':'List'}
    #else:
    #   context_dict={'title':'My List'}
    return render(request,'list.htm',context_dict)

def Retrieve(request,slug=None):
    instance=get_object_or_404(Post,slug=slug)
    share_string=quote_plus(instance.content)
    context_dict={'title':'Retrieve','instance':instance,'share_string':share_string}
    return render(request,'detail.html',context_dict)

def Update(request,slug=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance=get_object_or_404(Post,slug=slug)
    form=CreatePost(request.POST or None,request.FILES or None,instance=instance)
    context={'form':form}
    if form.is_valid():
        form.save(commit=False)
        instance.user=request.user
        form.save()
        messages.success(request,'Post Updated Successfully')
        return HttpResponseRedirect(reverse('Post:retrieve',kwargs={"slug":slug}))
    return render(request,'create_form.html',context)

def Delete(request,pk=None):
    instance=get_object_or_404(Post,id=pk)
    instance.delete()
    messages.success(request,'Post deleted successfully')
    return HttpResponseRedirect(reverse('Post:list'))

def listing(request):
    Post_list = Post.objects.all().order_by("-timestamp")
    paginator = Paginator(Post_list, 3) # Show 3 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'list.htm', {'page_obj': page_obj,'title':'List'})

def pre_save_post_reciever(sender,instance,*args,**kwargs):
    slug=slugify(instance.title)
    exists=Post.objects.filter(slug=slug).exists()
    if exists:
        slug="%s-%s"%(slugify(instance.title),instance.id)

    instance.slug=slug


pre_save.connect(pre_save_post_reciever,sender=Post)