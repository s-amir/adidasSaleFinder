from django.shortcuts import render
from .find_items import run_driver
def start(request):
    run_driver()

