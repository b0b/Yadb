# -*- coding: utf-8 -*-

from django import forms

class SearchForm(forms.Form):
    search_terms = forms.CharField()
