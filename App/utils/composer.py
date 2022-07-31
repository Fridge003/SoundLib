from django.shortcuts import render
from App.models import Composer

def render_composer_info(OriginalRequest, SelectedComposers) :

    context                 = {}
    context["AllComposers"] = [SelectedComposers]

    return render(OriginalRequest, "composer.html", context)

def render_composer_change(
    OriginalRequest,
    SelectedComposer: Composer,
    ChangeFailed=False,
    MultipleNames=False) :

    context                     = {}
    context["Composer"]         = SelectedComposer
    context["ChangeFailed"]     = ChangeFailed
    context["MultipleNames"]    = MultipleNames

    return render(OriginalRequest, "composer_change.html", context)

def process_composer_change(
    SelectedComposer: Composer,
    Name,
    Introduction
    ) :

    if Name != SelectedComposer.get_name() :
        SameName = Composer.objects.filter(Name=Name).all()
        if len(SameName) :
            return {"ChangeFailed": True, "MultipleNames": True}

    SelectedComposer.Name = Name
    SelectedComposer.Introduction = Introduction

    SelectedComposer.save()

    return {"ChangeFailed": False, "MultipleNames": False}