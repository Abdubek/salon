from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, REDIRECT_FIELD_NAME, logout as auth_logout

from django.utils.http import is_safe_url
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters

from django.views.generic import FormView, RedirectView, CreateView, TemplateView, UpdateView, View
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages

from users.models import User
from users.forms import SignUpForm


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "users/home.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        if not request.user.salon:
            return redirect(reverse_lazy('salon:add'))

        return self.render_to_response(context)


class UserCreate(CreateView):
    model = User
    form_class = SignUpForm

    def form_valid(self, form):
        instance = form.save(commit=False)

        if self.request.user.is_authenticated:
            instance.manager = self.request.user
            instance.salon = self.request.user.salon
            instance.save()
        else:
            instance.save()
            login(self.request, instance)

            return redirect('/')

        return redirect(instance.get_absolute_url())


class LoginView(FormView):
    """
    Provides the ability to login as a user with a username and password
    """
    success_url = '/'
    form_class = AuthenticationForm
    template_name = "users/login.html"
    redirect_field_name = REDIRECT_FIELD_NAME

    @method_decorator(sensitive_post_parameters('password'))
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        # Sets a test cookie to make sure the user has cookies enabled
        request.session.set_test_cookie()

        return super(LoginView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        login(self.request, form.get_user())

        # If the test cookie worked, go ahead and
        # delete it since its no longer needed
        if self.request.session.test_cookie_worked():
            self.request.session.delete_test_cookie()

        return super(LoginView, self).form_valid(form)

    def get_success_url(self):
        redirect_to = self.request.POST.get(self.redirect_field_name)
        if not is_safe_url(url=redirect_to, host=self.request.get_host()):
            redirect_to = self.success_url
        return redirect_to


class LogoutView(RedirectView):
    """
    Provides users the ability to logout
    """
    url = '/login/'

    def get(self, request, *args, **kwargs):
        auth_logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)


class UserProfile(LoginRequiredMixin, UpdateView):
    model = User
    fields = ('username', 'first_name', 'last_name', 'phone_number', 'avatar', 'email', 'about')
    template_name_suffix = '_update_form'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        password_form = PasswordChangeForm(user=self.request.user)
        context['password_form'] = password_form

        return context


class PasswordChange(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        password_form = PasswordChangeForm(request.user, request.POST)

        if password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)

            return redirect(user.get_absolute_url())
        else:
            messages.error(request, 'Please correct the error below.')

        return redirect(request.user.get_absolute_url())
