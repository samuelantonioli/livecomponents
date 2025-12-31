from typing import Any
from django_components import component
from livecomponents import StatelessLiveComponent


@component.register("floorplanwizard/step1")
class Step1Component(StatelessLiveComponent):
    template_name = "floorplanwizard/step1/step1.html"
