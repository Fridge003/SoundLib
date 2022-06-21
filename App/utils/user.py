from django.shortcuts import render
from django.db.utils import IntegrityError
from App.models import User
from django.contrib.auth import logout as logout_user

# Render the "user" page,
# Parameters include error messages when user tries to change info
def render_user(Request,
                ChangeFailed=False,
                Inconsistency=False,
                UsedName=False,) :
    Context          = {}
    Context["ChangeFailed"] = ChangeFailed
    Context["Inconsistency"] = Inconsistency
    Context["UsedName"] = UsedName
    return render(Request, 'user.html', Context)

# Process a submitted change-user-info form
def process_change_form(Request, UserName, Email, Password, Password2, Introduction="Empty") :

    OldUserName = Request.user.username
    print('changing', OldUserName, 'to', UserName, Email, Password, Password2, Introduction)

    CurUser = User.objects.get(username=OldUserName)

    if Password and Password2 : # change password
        if Password != Password2 : # different password
            return {"change_failed": True, "inconsistent_password": True, "conflict_username": False}
        else :
            CurUser.set_password(Password)
    
    if UserName != OldUserName : # change user name
        CurUser.username=UserName

    if Introduction :
        CurUser.Introduction = Introduction

    try:
        CurUser.save()
    except IntegrityError as e: # Possibly conflicting username
        return {"change_failed": True, "inconsistent_password": False, "conflict_username": True}

    CurUser.save()
    Request.user = CurUser
    
    return True