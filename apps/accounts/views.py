from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from .forms import StudentRegistrationForm, StudentLoginForm, UserProfileUpdateForm, StudentProfileDetailsForm
from .models import User, StudentProfile

class RegisterView(CreateView):
    model = User
    form_class = StudentRegistrationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('dashboard:student_dashboard')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard:student_dashboard')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, f"Welcome to TECHSPIRE Learning, {user.first_name}! Your account has been created successfully.")
        return redirect(self.request.GET.get('next') or self.success_url)

    def form_invalid(self, form):
        messages.error(self.request, "Please fix the errors below to complete your registration.")
        return super().form_invalid(form)


class CustomLoginView(LoginView):
    form_class = StudentLoginForm
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        next_url = self.request.GET.get('next') or self.request.POST.get('next')
        if next_url:
            return next_url
        return reverse_lazy('dashboard:student_dashboard')

    def form_valid(self, form):
        messages.success(self.request, f"Welcome back, {form.get_user().first_name or form.get_user().username}!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Invalid email or password. Please check your credentials.")
        return super().form_invalid(form)


def user_logout(request):
    logout(request)
    messages.info(request, "You have been logged out successfully. Keep learning!")
    return redirect('core:home')


@login_required
def profile_view(request):
    user = request.user
    profile = user.profile

    if request.method == 'POST':
        u_form = UserProfileUpdateForm(request.POST, request.FILES, instance=user)
        p_form = StudentProfileDetailsForm(request.POST, instance=profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "Your profile has been updated successfully!")
            return redirect('accounts:profile')
        else:
            messages.error(request, "Please correct the errors in the profile form.")
    else:
        u_form = UserProfileUpdateForm(instance=user)
        p_form = StudentProfileDetailsForm(instance=profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'title': 'My Profile & Settings',
    }
    return render(request, 'accounts/profile.html', context)
