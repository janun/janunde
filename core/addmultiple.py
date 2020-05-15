from __future__ import absolute_import, unicode_literals

from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.encoding import force_text
from django.views.decorators.vary import vary_on_headers

from wagtail.admin.auth import PermissionPolicyChecker
from wagtail.images import get_image_model
from wagtail.images.fields import ALLOWED_EXTENSIONS
from wagtail.images.forms import get_image_form
from wagtail.images.permissions import permission_policy
from wagtail.images.views.multiple import get_image_edit_form

permission_checker = PermissionPolicyChecker(permission_policy)


@permission_checker.require("add")
@vary_on_headers("X-Requested-With")
def add(request):
    Image = get_image_model()
    ImageForm = get_image_form(Image)

    collections = permission_policy.collections_user_has_permission_for(
        request.user, "add"
    )
    if len(collections) > 1:
        collections_to_choose = collections
    else:
        # no need to show a collections chooser
        collections_to_choose = None

    if request.method == "POST":
        if not request.is_ajax():
            return HttpResponseBadRequest("Cannot POST to this view without AJAX")

        if not request.FILES:
            return HttpResponseBadRequest("Must upload a file")

        # Build a form for validation
        form = ImageForm(
            {
                "title": request.FILES["files[]"].name,
                "collection": request.POST.get("collection"),
                "attribution": request.POST.get("attribution"),
            },
            {"file": request.FILES["files[]"],},
            user=request.user,
        )

        if form.is_valid():
            # Save it
            image = form.save(commit=False)
            image.uploaded_by_user = request.user
            image.file_size = image.file.size
            image.save()

            # Success! Send back an edit form for this image to the user
            return JsonResponse(
                {
                    "success": True,
                    "image_id": int(image.id),
                    "form": render_to_string(
                        "wagtailimages/multiple/edit_form.html",
                        {
                            "image": image,
                            "form": get_image_edit_form(Image)(
                                instance=image,
                                prefix="image-%d" % image.id,
                                user=request.user,
                            ),
                        },
                        request=request,
                    ),
                }
            )
        else:
            # Validation error
            return JsonResponse(
                {
                    "success": False,
                    # https://github.com/django/django/blob/stable/1.6.x/django/forms/util.py#L45
                    "error_message": "\n".join(
                        [
                            "\n".join([force_text(i) for i in v])
                            for k, v in form.errors.items()
                        ]
                    ),
                }
            )
    else:
        form = ImageForm(user=request.user)

    return render(
        request,
        "wagtailimages/multiple/add.html",
        {
            "max_filesize": form.fields["file"].max_upload_size,
            "help_text": form.fields["file"].help_text,
            "allowed_extensions": ALLOWED_EXTENSIONS,
            "error_max_file_size": form.fields["file"].error_messages[
                "file_too_large_unknown_size"
            ],
            "error_accepted_file_types": form.fields["file"].error_messages[
                "invalid_image"
            ],
            "collections": collections_to_choose,
        },
    )
