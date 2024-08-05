from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import ImageCreateForm
from .models import Image
from actions.utils import create_action

# Create your views here.

@login_required
def image_create(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = ImageCreateForm(data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            new_image = form.save(commit=False)
            
            # assign the current user to the form.
            new_image.user = request.user
            new_image.save()
            
            # Add an action using bookmarked image as a verb.
            create_action(user=request.user,
                          verb='bookmarked image',
                          target=new_image)
            
            # Show success message.
            messages.success(request,
                         "Image added successfully")
            
            return redirect(new_image.get_absolute_url())
    
    else:
        form = ImageCreateForm(data=request.GET)
    return render(request,
                  "images/image/create.html",
                  {"section": "images", "form": form})

def image_detail(request: HttpRequest, id: int, slug: str) -> HttpResponse:

    image = get_object_or_404(Image, id=id, slug=slug)
    return render(request,
                  "images/image/detail.html",
                  {"section": "images", "image": image})

@login_required
@require_POST
def image_like(request: HttpRequest) -> HttpResponse:
    image_id = request.POST.get("id")
    action = request.POST.get("action")
    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            if action == "like":
                image.user_likes.add(request.user)

                # Add an action using likes as a verb.
                create_action(user=request.user,
                              verb="likes",
                              target=image)
                
            else:
                image.user_likes.remove(request.user)
            return JsonResponse({"status": "ok"})
        except Image.DoesNotExist:
            pass
    return JsonResponse({"status": "error"})

@login_required
def image_list(request: HttpRequest) -> HttpResponse:
    images = Image.objects.all()
    paginator = Paginator(images, 8)
    page = request.GET.get('page') # When requested by the browser.
    images_only = request.GET.get('images_only') # When requested by JS.
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page.
        images = paginator.page(1)
    except EmptyPage:
        if images_only:
            # If AJAX request and page out of range
            # return an empty page
            return HttpResponse("")
        # If page out of range retrun last page of results
        images = paginator.page(paginator.num_pages)
    
    if images_only:
        return render(request,
                      'images/image/list_images.html',
                      {'section': 'images',
                       'images': images})
    return render(request,
                  'images/image/list.html',
                  {'section': 'images',
                   'images': images})