from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.db import transaction
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_encode

from ..forms.register_form import RegistrationForm


@transaction.atomic
def register(request):
    try:
        form = RegistrationForm()
        if request.method == "POST":
            form = RegistrationForm(request.POST)
            if form.is_valid():
                with transaction.atomic():
                    new_form = form.save(commit=False)

                    # data
                    email = form.cleaned_data.get("email")
                    username = email.split("@")[0]  # get username from email
                    new_form.username = username
                    password = form.cleaned_data.get("password")
                    new_form.set_password(password)
                    new_form.save()

                    # send email to user
                    email = form.cleaned_data.get("email")
                    username = form.cleaned_data.get("username")
                    first_name = form.cleaned_data.get("first_name")
                    last_name = form.cleaned_data.get("last_name")

                    current_site = get_current_site(request)
                    subject = "Welcome to the site"
                    domain = f"http://{current_site.domain}/activate/{urlsafe_base64_encode(force_bytes(new_form))}/"
                    message = f"Hi {first_name} {last_name}, welcome to the site"
                    body = render_to_string(
                        "accounts/verification.html",
                        {
                            "subject": subject,
                            "body": message,
                            "domain": domain,
                        },
                    )
                    html_body = strip_tags(body)
                    sendmail = EmailMessage(
                        subject=subject,
                        body=html_body,
                        to=[email],
                    )
                    sendmail.send()

                messages.success(request, f"Account created for {username}!")
                return redirect("accounts:sign_in")
        return render(request, "accounts/register.html", {"form": form})
    except Exception as e:
        messages.error(request, f"Error: {e}")
        return redirect("accounts:register")
