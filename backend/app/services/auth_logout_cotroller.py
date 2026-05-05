"""
app/services/auth_logout_cotroller.py — Control Layer
======================================================
Sprint 1 — UA-12, FR-07, DN-07, PM-10: Logout

LogoutController — JWT is stateless, no DB operation needed.
"""


class LogoutController:
    """
    Control — LogoutController (UA-12, FR-07, DN-07, PM-10)
    JWT logout is stateless — no DB operation needed.
    Frontend clears token from localStorage.
    """

    @staticmethod
    def logout():
        return True


# Keep old name as alias for backward compatibility
AuthLogoutCotroller = LogoutController