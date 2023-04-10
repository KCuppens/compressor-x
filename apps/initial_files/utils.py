import datetime

from apps.base.utils import upload_file_to_media
from apps.compression.models import Compression

from .models import InitialFile


def uploading_initial_file(file, action_obj):
    """
    Creating the InitialFile
    Assign InitialFile to Action
    """
    # Creating Compression
    compression_obj = Compression.objects.create()
    filename = get_unique_file_name(file)
    path = get_initial_file_path(action_obj, compression_obj, filename)
    # Save in S3 MediaStorage
    upload_file_to_media(path, file)
    # Creating InitialFile
    initial_file = InitialFile.objects.create(file=path)
    compression_obj.initial_file = initial_file
    compression_obj.save(update_fields=["initial_file"])
    # Assign Convert to Action
    action_obj.compressions.add(compression_obj)
    return initial_file


def get_unique_file_name(file):
    file_name = file.name.split("/")[-1]
    extension = file_name.split(".")[1]
    file_name = file_name.split(".")[0]
    date_now = str(datetime.datetime.now().strftime("%m%d%Y%H%M%S"))
    return f"{file_name}-{date_now}.{extension}"


def get_initial_file_path(action_obj, compression_obj, filename):
    """
    Get the path of the initial file
    """
    return f"{action_obj}/{compression_obj.id}/initial_files/{filename}"
