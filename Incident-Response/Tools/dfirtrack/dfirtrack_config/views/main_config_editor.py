from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from dfirtrack_config.forms import MainConfigForm
from dfirtrack_config.models import MainConfigModel
from dfirtrack_main.logger.default_logger import info_logger

@login_required(login_url="/login")
def main_config_view(request):

    # form was valid to post
    if request.method == "POST":

        # get config model
        model = MainConfigModel.objects.get(main_config_name = 'MainConfig')
        # get form
        form = MainConfigForm(request.POST, instance = model)

        if form.is_valid():

            # save settings
            model = form.save(commit=False)
            model.save()
            form.save_m2m()

            # create message
            messages.success(request, 'Main config changed')

            # call logger
            info_logger(str(request.user), " MAIN_CONFIG_CHANGED")

            # close popup
            return HttpResponse('<script type="text/javascript">window.close();</script>')

        else:
            # show form page again
            return render(
                request,
                'dfirtrack_config/main_config_popup.html',
                {
                    'form': form,
                }
            )

    else:

        # get config model
        model = MainConfigModel.objects.get(main_config_name = 'MainConfig')
        # get form
        form = MainConfigForm(instance = model)

    # show form page
    return render(
        request,
        'dfirtrack_config/main_config_popup.html',
        {
            'form': form,
        }
    )
