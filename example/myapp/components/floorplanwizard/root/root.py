from typing import Any, Literal
from django_components import component
from django.forms import ModelForm, RadioSelect, NumberInput, TextInput

from livecomponents import (
    CallContext,
    command,
    ExtraContextRequest,
    InitStateContext,
    LiveComponentsModel,
)
from livecomponents import LiveComponent

from myapp.models import Floorplan
from django.http import QueryDict


class FloorplanForm(ModelForm):
    class Meta:
        model = Floorplan
        exclude = ()
        widgets = {
            "resolution": RadioSelect,
            "furniture_style": RadioSelect,
            "number_of_floorplans": NumberInput(attrs={"min": 1}),
        }


class RootState(LiveComponentsModel):
    step: int = 1
    data: dict = dict(plan_type="2d")
    form: ModelForm | None = None
    saved: any = None
    saved_id: int | None = None


@component.register("floorplanwizard/root")
class RootComponent(LiveComponent[RootState]):
    template_name = "floorplanwizard/root/root.html"
    initial = dict(
        number_of_floorplans=1,
        resolution="1080",
        furniture_style="modern",
    )

    def _build_form(self, state: RootState):
        merged = {**self.initial, **state.data}

        if state.step == 3:
            # bei step 3 unbound form
            return FloorplanForm(initial=merged, data=None)
        else:
            return FloorplanForm(
                initial=self.initial,
                data=merged,
            )

    def init_state(self, context: InitStateContext) -> RootState:
        state = RootState()
        state.form = self._build_form(state)
        return state

    @command
    def nav(self, call_context: CallContext[RootState], dir: str = "next", **fields):
        state = call_context.state
        state.data |= fields
        state.form = FloorplanForm(
            initial=self.initial, data={**self.initial, **state.data}
        )
        if dir == "prev":
            state.step = max(1, state.step - 1)
        elif dir == "next":
            state.step = min(3, state.step + 1)
        state.form = self._build_form(state)

    @command
    def update_data(self, call_context: CallContext[RootState], **fields):
        call_context.state.data = {**call_context.state.data, **fields}
        call_context.state.form = self._build_form(call_context.state)

    @command
    def submit(self, call_context: CallContext[RootState], **fields):
        state = call_context.state
        state.data |= fields

        merged = {**self.initial, **state.data}
        form = FloorplanForm(data=merged, instance=Floorplan())
        state.form = form

        if not form.is_valid():
            return  # root rendert wieder form.errors

        obj = form.save()
        state.saved = obj.__dict__
        state.saved_id = obj.pk
        state.step = 4
