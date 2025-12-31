from typing import Any
from django_components import component
from livecomponents import StatelessLiveComponent


@component.register("floorplanwizard/step2_3d")
class Step2_3dComponent(StatelessLiveComponent):
    template_name = "floorplanwizard/step2_3d/step2_3d.html"
