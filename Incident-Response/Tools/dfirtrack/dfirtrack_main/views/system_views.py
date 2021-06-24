from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView
from dfirtrack_artifacts.models import Artifact
from dfirtrack_config.models import MainConfigModel
from dfirtrack_main.forms import SystemForm, SystemNameForm
from dfirtrack_main.logger.default_logger import debug_logger, warning_logger
from dfirtrack_main.models import Analysisstatus, Ip, System, Systemstatus
from dfirtrack.settings import INSTALLED_APPS as installed_apps
from django.http import  JsonResponse, HttpResponseForbidden
from django.templatetags.static import static
from django.template.loader import render_to_string
from django.core.exceptions import FieldError
import ipaddress

class SystemList(LoginRequiredMixin, ListView):
    login_url = '/login'
    model = System
    template_name = 'dfirtrack_main/system/system_list.html'
    context_object_name = 'system_list'

    def get_queryset(self):
        # call logger
        debug_logger(str(self.request.user), " SYSTEM_LIST_ENTERED")
        return System.objects.order_by('system_name')

    def get_context_data(self, **kwargs):

        # returns context dictionary
        context = super(SystemList, self).get_context_data()

        # set dfirtrack_api for template
        if 'dfirtrack_api' in installed_apps:
            context['dfirtrack_api'] = True
        else:
            context['dfirtrack_api'] = False

        # return dictionary with additional values for template
        return context

class SystemDetail(LoginRequiredMixin, DetailView):
    login_url = '/login'
    model = System
    template_name = 'dfirtrack_main/system/system_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        system = self.object

        # set dfirtrack_artifacts for template
        if 'dfirtrack_artifacts' in installed_apps:
            context['dfirtrack_artifacts'] = True
            context['artifacts'] = Artifact.objects.filter(system=system)
        else:
            context['dfirtrack_artifacts'] = False

        # set dfirtrack_api for template
        if 'dfirtrack_api' in installed_apps:
            context['dfirtrack_api'] = True
        else:
            context['dfirtrack_api'] = False

        # call logger
        system.logger(str(self.request.user), " SYSTEM_DETAIL_ENTERED")
        return context

class SystemCreate(LoginRequiredMixin, CreateView):
    login_url = '/login'
    model = System
    form_class = SystemNameForm
    template_name = 'dfirtrack_main/system/system_add.html'

    def get(self, request, *args, **kwargs):

        # get id of first status objects sorted by name
        systemstatus = Systemstatus.objects.order_by('systemstatus_name')[0].systemstatus_id
        analysisstatus = Analysisstatus.objects.order_by('analysisstatus_name')[0].analysisstatus_id

        # show empty form with default values for convenience and speed reasons
        form = self.form_class(initial={
            'systemstatus': systemstatus,
            'analysisstatus': analysisstatus,
        })
        # call logger
        debug_logger(str(request.user), " SYSTEM_ADD_ENTERED")
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            system = form.save(commit=False)
            system.system_created_by_user_id = request.user
            system.system_modified_by_user_id = request.user
            system.system_modify_time = timezone.now()
            system.save()
            form.save_m2m()

            # extract lines from ip list
            lines = request.POST.get('iplist').splitlines()
            # call function to save ips
            ips_save(request, system, lines)

            # call logger
            system.logger(str(request.user), ' SYSTEM_ADD_EXECUTED')
            messages.success(request, 'System added')
            return redirect(reverse('system_detail', args=(system.system_id,)))
        else:
            return render(request, self.template_name, {'form': form})

class SystemUpdate(LoginRequiredMixin, UpdateView):
    login_url = '/login'
    model = System
    template_name = 'dfirtrack_main/system/system_edit.html'

    # get config model (without try statement 'manage.py migrate' fails (but not in tests))
    try:
        system_name_editable = MainConfigModel.objects.get(main_config_name = 'MainConfig').system_name_editable
    except:
        system_name_editable  = False

    # choose form class depending on variable
    if system_name_editable is False:
        form_class = SystemForm
    elif system_name_editable is True:
        form_class = SystemNameForm
    else:
        # enforce default value False
        form_class = SystemForm

    def get(self, request, *args, **kwargs):
        system = self.get_object()

        # get config model (without try statement 'manage.py migrate' fails (but not in tests))
        try:
            system_name_editable = MainConfigModel.objects.get(main_config_name = 'MainConfig').system_name_editable
        except:
            system_name_editable  = False

        # set system_name_editable for template
        if system_name_editable is False:
            system_name_edit = False
        elif system_name_editable is True:
            system_name_edit = True

        """ get all existing ip addresses """

        # get objects
        ips = system.ip.all()
        # count objects
        iplen = len(ips)
        # set counter
        i = 0
        # set default string if there is no object at all
        ipstring = ''
        for ip in ips:
            # add ip to string
            ipstring = ipstring + str(ip.ip_ip)
            # increment counter
            i += 1
            # add newline but not for last occurence
            if i < iplen:
                ipstring = ipstring + '\n'

        # show form for system with all ip addresses
        form = self.form_class(
            instance=system,
            initial={
                'iplist': ipstring,
            },
        )
        # call logger
        system.logger(str(request.user), " SYSTEM_EDIT_ENTERED")
        return render(
            request,
            self.template_name,
            {
                'form': form,
                # boolean variable is used in template
                'system_name_edit': system_name_edit,
                # return system object in context for use in template
                'system': system,
            }
        )

    def post(self, request, *args, **kwargs):
        system = self.get_object()
        form = self.form_class(request.POST, instance=system)
        if form.is_valid():
            system = form.save(commit=False)
            system.system_modified_by_user_id = request.user
            system.system_modify_time = timezone.now()
            system.save()
            form.save_m2m()

            # remove all ips to avoid double assignment of beforehand assigned ips
            system.ip.clear()
            # extract lines from ip list
            lines = request.POST.get('iplist').splitlines()
            # call function to save ips
            ips_save(request, system, lines)

            # call logger
            system.logger(str(request.user), ' SYSTEM_EDIT_EXECUTED')
            messages.success(request, 'System edited')
            return redirect(reverse('system_detail', args=(system.system_id,)))
        else:
            return render(request, self.template_name, {'form': form})

def ips_save(request, system, lines):
    # iterate over lines
    for line in lines:
        # skip empty lines
        if line == '':
            # call logger
            warning_logger(str(request.user), ' SYSTEM_ADD_IP_EMPTY_LINE')
            messages.error(request, 'Empty line instead of IP was provided')
            continue
        # check line for ip
        try:
            ipaddress.ip_address(line)
        except ValueError:
            # call logger
            warning_logger(str(request.user), ' SYSTEM_ADD_IP_NO_IP')
            messages.error(request, 'Provided string was no IP')
            continue

        # create ip
        ip, created = Ip.objects.get_or_create(ip_ip=line)
        # call logger
        if created == True:
            ip.logger(str(request.user), ' SYSTEM_ADD_IP_CREATED')
            messages.success(request, 'IP created')
        else:
            messages.warning(request, 'IP already exists in database')

        # save ip for system
        system.ip.add(ip)

def get_systems_json(request):
    if request.user.is_authenticated:
        # get parameters from GET request and parse them accordingly
        get_params = request.GET
        referer = request.headers['Referer']
        order_column_number = get_params['order[0][column]']
        order_column_name = get_params['columns['+order_column_number+'][data]']
        order_dir = '' if (get_params['order[0][dir]']=='asc') else '-'
        search_value = get_params['search[value]']
        # check that string contains only alphanumerical chars or spaces (or '_','-',':')
        if not all((x.isalnum() or x.isspace() or x == '_' or x == '-' or x == ':') for x in search_value):
            search_value = ''

        # if no search value is given, get all objects and order them according to user setting, if the table is not generated on the general system overview page, only show the systems with the relevant id 
        if search_value == '':
            if referer.endswith('/system/'):
                system_values = System.objects.all().order_by(order_dir+order_column_name)
            elif '/analysisstatus/' in referer:
                analysisstatus_id = referer.split("/")[-2]
                system_values = System.objects.filter(analysisstatus__analysisstatus_id=analysisstatus_id)
            elif '/systemstatus/' in referer:
                systemstatus_id = referer.split("/")[-2]
                system_values = System.objects.filter(systemstatus__systemstatus_id=systemstatus_id)
            elif '/case/' in referer:
                case_id = referer.split("/")[-2]
                system_values = System.objects.filter(case__case_id=case_id)
            elif '/tag/' in referer:
                tag_id = referer.split("/")[-2]
                system_values = System.objects.filter(tag__tag_id=tag_id)


        # if search value is given, go through all cloumn-raw-data and search for it
        else:
            system_values = System.objects.none()
            # to keep the search dynamic and not hardcode the fields, we go through all columns as they are found in the request here
            for entry in get_params:
                # this matches on these lines: ''' columns[0][data]': ['system_id/system_name/...'] '''
                if '][data]' in entry:
                    tmp_column_name = get_params[entry]
                    # we start with an empty queryset and add all systems that have a match in one of their relevant fields
                    try:
                        # filter_kwargs is necessary for dynamic filter design
                        filter_kwargs = {tmp_column_name+'__icontains': search_value}
                        if '/analysisstatus/' in referer:
                            analysisstatus_id = referer.split("/")[-2]
                            filter_kwargs["analysisstatus__analysisstatus_id"] = analysisstatus_id
                        elif '/systemstatus/' in referer:
                            systemstatus_id = referer.split("/")[-2]
                            filter_kwargs["systemstatus__systemstatus_id"] = systemstatus_id
                        elif '/case/' in referer:
                            case_id = referer.split("/")[-2]
                            filter_kwargs["case__case_id"] = case_id
                        elif '/tag/' in referer:
                            tag_id = referer.split("/")[-2]
                            filter_kwargs["tag__tag_id"] = tag_id
                        system_values = system_values | System.objects.filter(**filter_kwargs)
                    # for foreign keys, an exception is thrown, need to modify filter_kwargs accordingly
                    except FieldError:
                        filter_kwargs = {tmp_column_name+'__'+tmp_column_name+'_name'+'__icontains': search_value}
                        if '/analysisstatus/' in referer:
                            analysisstatus_id = referer.split("/")[-2]
                            filter_kwargs["analysisstatus__analysisstatus_id"] = analysisstatus_id
                        elif '/systemstatus/' in referer:
                            systemstatus_id = referer.split("/")[-2]
                            filter_kwargs["systemstatus__systemstatus_id"] = systemstatus_id
                        elif '/case/' in referer:
                            case_id = referer.split("/")[-2]
                            filter_kwargs["case__case_id"] = case_id
                        elif '/tag/' in referer:
                            tag_id = referer.split("/")[-2]
                            filter_kwargs["tag__tag_id"] = tag_id
                        system_values = system_values | System.objects.filter(**filter_kwargs)
            # make the resulting queryset unique and sort it according to user settings
            system_values = system_values.distinct().order_by(order_dir+order_column_name)

        # starting point for records in table
        start = int(get_params['start'])
        # how many records are to be shown? if all records are to be shown, length is set to -1
        length = int(get_params['length']) if int(get_params['length'])!=-1 else len(system_values)

        # if there is a search value check that the search value really occurs in one of the visible fields in the table (it is possible that the value only occurs e.g. only in the milliseconds of the data field)
        if search_value != '':
            for i in system_values:
                # extract values from system object
                system_id = i.system_id
                system_name = i.system_name
                systemstatus = i.systemstatus
                analysisstatus = i.analysisstatus
                system_create_time = i.system_create_time.strftime("%Y-%m-%d %H:%M")
                system_modify_time = i.system_modify_time.strftime("%Y-%m-%d %H:%M")

                search_relevant_strings = [str(system_id), str(system_name), str(systemstatus), str(analysisstatus), str(system_create_time), str(system_modify_time)]
                really_contains_search_string = False
                # go through visible fields and check if search string is contained
                for field in search_relevant_strings:
                    if search_value in field:
                        really_contains_search_string = True
                # if the searched string was not found, exclude system from queryset
                if not really_contains_search_string:
                    system_values = system_values.exclude(system_id=system_id)

        # all matching systems
        system_count = len(system_values)
        # construct the final list with systems that are presented to user
        visible_system_list = []
        for i in system_values[start:(start+length)]:
            # construct the data to be presented in the system table, important: if you add something here, make sure you also add it above in the cleaned_system_values generation to stay consistent
            visible_system_list.append(
                {
                "system_id": i.system_id,
                "system_name": "<a href='"+i.get_absolute_url()+"' type='button' class='btn btn-primary btn-sm top-distance copy-true'><img src='"+static("dfirtrack_main/icons/monitor-light.svg")+"' class='icon right-distance copy-false' alt='icon'>"+i.system_name+"</a>",
                "systemstatus": render_to_string('dfirtrack_main/includes/button_systemstatus.html', {'systemstatus': i.systemstatus}),
                "analysisstatus": "<span data-toggle='tooltip' data-placement='auto' title='"+str(i.analysisstatus.analysisstatus_note or "")+"'><a href='"+i.analysisstatus.get_absolute_url()+"'>"+str(i.analysisstatus)+"</a></span>" if i.analysisstatus is not None else "---",
                "system_create_time": i.system_create_time.strftime("%Y-%m-%d %H:%M"),
                "system_modify_time": i.system_modify_time.strftime("%Y-%m-%d %H:%M")
                }
                )

        # prepare dictionary with relevant data to convert to json
        json_dict = {}
        json_dict['draw'] = int(get_params['draw'])
        json_dict['recordsTotal'] = len(System.objects.all())
        json_dict['recordsFiltered'] = system_count
        json_dict['data'] = visible_system_list

        # convert dict with data to jsonresponse
        response = JsonResponse(json_dict, safe=False)
    # user is not logged in - possible TODO: should this be logged somewhere?
    else:
        response = HttpResponseForbidden()
    return response
