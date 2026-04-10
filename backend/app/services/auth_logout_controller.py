from app.models.user_account import UserAccount
from app.models.user_session import UserSession


class AuthLogoutController:
    """
    Control — AuthLogoutController <controller> from BCE diagram.
    Method: logout(accountId: String)
    Delegates to UserAccount.logout(accountId) per sequence diagram.
    """

    @staticmethod
    def logout(accountId: str) -> None:
        """
        Sequence diagram flow:
          LogoutBoundary → AuthLogoutCotroller.logout(accountId)
                         → UserAccount.logout(accountId)   [expires all sessions]
                         ← return ("login-page")
        """
        if accountId:
            UserAccount.logout(accountId)

    @staticmethod
    def logoutByToken(token: str) -> None:
        """
        Alternative: expire a specific session by token.
        Used when only the token is known (not the accountId).
        """
        if token:
            UserSession.expire(token)
