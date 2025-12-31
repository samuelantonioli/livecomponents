from typing import Any
from django_components import component
from livecomponents import StatelessLiveComponent


@component.register("floorplanwizard/step2_2d")
class Step2_2dComponent(StatelessLiveComponent):
    template_name = "floorplanwizard/step2_2d/step2_2d.html"
