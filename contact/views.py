from django import forms
from django.template import RequestContext
from django.core.mail import EmailMessage
from django.shortcuts import render_to_response

class ContactForm(forms.Form):
    subject = forms.CharField(label='Sujet', max_length=100)
    sender = forms.EmailField(label='Votre E-mail')
    message = forms.CharField(label='Message', widget=forms.Textarea())

def index(request):
    send = None
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            sender = form.cleaned_data['sender']

            email = EmailMessage(subject, message, sender, to=['bob76h@gmail.com'])
            send = email.send()
    else:
        form = ContactForm()

    return render_to_response('contact/contact.html', {
        'form': form,
        'send': send,
        'message': 'Message',
    }, RequestContext(request))
