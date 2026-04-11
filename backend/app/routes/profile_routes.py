from flask import Blueprint, request, jsonify
from app.utils.auth_utils import token_required
from app.utils.avatar_utils import save_uploaded_image, get_avatar_url, delete_old_picture
from app.models.user_account import UserAccount

profile_bp = Blueprint('profile', __name__)


@profile_bp.route('/upload-avatar', methods=['POST'])
@token_required()
def upload_avatar(current_user):
    """
    POST /api/profile/upload-avatar
    Header: Authorization: Bearer <token>
    Body:   multipart/form-data with field 'avatar' (image file)

    What happens (Yimin's requirement):
    1. User picks an image on their computer (any name e.g. 'my photo.jpg')
    2. Backend receives the file
    3. Backend renames it to a unique random name (e.g. 'a1b2c3.jpg')
    4. Backend saves it to backend/app/static/uploads/
    5. Backend stores just the filename in the database
    6. Backend returns the full accessible URL so frontend can display it

    Returns: { avatar_url: "http://localhost:5000/static/uploads/a1b2c3.jpg" }
    """
    if 'avatar' not in request.files:
        return jsonify({'error': 'No file uploaded. Use field name: avatar'}), 400

    file = request.files['avatar']

    try:
        # Delete old picture from disk if user already has one
        old_picture = UserAccount.getProfilePicture(current_user['user_id'])
        if old_picture:
            delete_old_picture(old_picture)

        # Save new picture — returns unique filename like 'abc123.jpg'
        unique_filename = save_uploaded_image(file)

        # Store filename in database (NOT the full path)
        UserAccount.updateProfilePicture(current_user['user_id'], unique_filename)

        # Build the full URL that anyone can access
        avatar_url = get_avatar_url(
            role=current_user['role'],
            profile_picture=unique_filename
        )

        return jsonify({
            'message':    'Profile picture updated successfully.',
            'avatar_url': avatar_url,
        }), 200

    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Upload failed. Please try again.'}), 500
