from typing import Any
from django_components import component
from livecomponents import StatelessLiveComponent


@component.register("floorplanwizard/step3")
class Step3Component(StatelessLiveComponent):
    template_name = "floorplanwizard/step3/step3.html"
