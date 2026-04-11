import os
import uuid
from werkzeug.utils import secure_filename
 
# Allowed image extensions
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif', 'webp'}
 
# Where uploaded files are saved on disk
UPLOAD_FOLDER = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    'static', 'uploads'
)
 
# Default role avatars (fallback when no profile picture uploaded)
DEFAULT_AVATARS = {
    'admin':            'admin.svg',
    'fund_raiser':      'fund_raiser.svg',
    'donee':            'donee.svg',
    'platform_manager': 'platform_manager.svg',
}
 
 
def allowed_file(filename: str) -> bool:
    """Check if file extension is allowed."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
 
 
def save_uploaded_image(file) -> str:
    """
    Yimin's requirement:
    User uploads a file from their computer e.g. 'my photo.jpg'
    We CANNOT use that name — it may clash with other users' files,
    contain spaces/special chars, or expose private info.
 
    Solution:
    1. Generate a random unique name using uuid4()
    2. Keep the original extension (jpg, png, etc.)
    3. Save to backend/app/static/uploads/
    4. Return just the new filename (e.g. 'a1b2c3d4.jpg')
       — NOT the full path, NOT the original name
 
    The full accessible URL is built separately by get_avatar_url()
    so it works on any domain (localhost, Railway, etc.)
    """
    if not file or file.filename == '':
        raise ValueError('No file provided.')
 
    if not allowed_file(file.filename):
        raise ValueError('File type not allowed. Use jpg, jpeg, png, gif, or webp.')
 
    # Get original extension safely
    original_ext = file.filename.rsplit('.', 1)[1].lower()
 
    # Generate a completely unique filename — uuid4 is random and unique
    unique_filename = f"{uuid.uuid4().hex}.{original_ext}"
 
    # Save file to uploads folder
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    save_path = os.path.join(UPLOAD_FOLDER, unique_filename)
    file.save(save_path)
 
    # Return ONLY the filename — not the path, not the original name
    return unique_filename
 
 
def get_avatar_url(role: str, profile_picture: str = None) -> str:
    """
    Build a fully accessible URL for the avatar.
 
    Priority:
    1. If user has uploaded a profile picture → use uploaded image URL
    2. If no upload → use default role avatar URL
 
    Uses request.host_url when inside a request context (real API calls).
    Falls back to a relative path when outside request context (unit tests).
    """
    # Try to get base URL from Flask request context
    # If no request context (e.g. during unit tests), use empty string
    try:
        from flask import request as flask_request
        base_url = flask_request.host_url.rstrip('/')
    except RuntimeError:
        # Outside request context — unit tests
        base_url = ''
 
    if profile_picture:
        return f"{base_url}/static/uploads/{profile_picture}"
    else:
        filename = DEFAULT_AVATARS.get(role, 'default.svg')
        return f"{base_url}/static/avatars/{filename}"
 
 
def delete_old_picture(filename: str) -> None:
    """
    Delete old uploaded picture from disk when user uploads a new one.
    Only deletes from uploads/ — never touches default avatars.
    """
    if not filename:
        return
    path = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.exists(path):
        os.remove(path)