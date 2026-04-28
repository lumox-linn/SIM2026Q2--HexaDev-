class AuthLogoutCotroller:
    """
    Control — AuthLogoutCotroller.
    JWT is stateless — no DB operation needed on logout.
    Frontend clears token from localStorage.
    """

    @staticmethod
    def logout():
        """
        JWT logout — nothing to do on backend.
        Frontend handles clearing the token.
        """
        return True