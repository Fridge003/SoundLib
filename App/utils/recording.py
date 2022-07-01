from django.shortcuts import render
from django.db.utils import IntegrityError
from App.models import Recording, Composer

def render_recording_info(Request, Recordings) :
    Context                  = {}
    Context["RecordingList"] = Recordings
    return render(Request, 'recording.html', Context)

def render_recording_change(Request, Recordings) :

    Context                  = {}
    Context["RecordingList"] = Recordings
    return render(Request, 'recording_change.html', Context)

# Save a uploaded file to disk and maintain databases
def process_recording_change(
    CurRecording: Recording,
    MyFile,
    RecordingName,
    ComposerName,
    Description,
    ChangeTime,
    ChangeUser
    ) :

    # FileStorage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, "Uploaded"))
    # Filename = FileStorage.save(MyFile.name, MyFile)
    # UploadedFileUrl = FileStorage.url(Filename)

    CurComposer, _created = Composer.objects.get_or_create(Name=ComposerName, defaults={"Introduction": "Empty"})

    if _created :

        print("Created New Composer: ", CurComposer.Name)
    
    if ChangeUser != CurRecording.UploadUser :

        print("Trying to edit other's recording!")

        return
    
    if MyFile != None :
        CurRecording.File = MyFile
    
    CurRecording.Name = RecordingName
    CurRecording.Composer = CurComposer
    CurRecording.Description = Description
    CurRecording.LastEditTime = ChangeTime
    
    CurRecording.save()

    return