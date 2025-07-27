from fastapi import HTTPException

# Excepciones base
class BaseAppError(HTTPException):
    """Clase base para todas las excepciones personalizadas"""
    pass

class TodoError(HTTPException):
    """Base exception for todo-related errors"""
    pass

class TodoNotFoundError(TodoError):
    def __init__(self, todo_id=None):
        message = "Todo not found" if todo_id is None else f"Todo with id {todo_id} not found"
        super().__init__(status_code=404, detail=message)

class TodoCreationError(TodoError):
    def __init__(self, error: str):
        super().__init__(status_code=500, detail=f"Failed to create todo: {error}")

class UserError(HTTPException):
    """Base exception for user-related errors"""
    pass

class UserNotFoundError(UserError):
    def __init__(self, user_id=None):
        message = "User not found" if user_id is None else f"User with id {user_id} not found"
        super().__init__(status_code=404, detail=message)

class UserBlockedError(UserError):
    def __init__(self, user_id=None):
        message = "User account is blocked" if user_id is None else f"User account {user_id} is blocked"
        super().__init__(status_code=403, detail=message)

class UserNotActiveError(UserError):
    def __init__(self, user_id=None):
        message = "User account is not active" if user_id is None else f"User account {user_id} is not active"
        super().__init__(status_code=403, detail=message)

class PasswordMismatchError(UserError):
    def __init__(self):
        super().__init__(status_code=400, detail="New passwords do not match")

class InvalidPasswordError(UserError):
    def __init__(self):
        super().__init__(status_code=401, detail="Current password is incorrect")

class AuthenticationError(HTTPException):
    def __init__(self, message: str = "Could not validate user"):
        super().__init__(status_code=401, detail=message)

# ----------------------------
# Excepciones de Libros
# ----------------------------
class BookError(BaseAppError):
    pass

class BookNotFoundError(BookError):
    def __init__(self, book_id=None):
        message = "Book not found" if book_id is None else f"Book with id {book_id} not found"
        super().__init__(status_code=404, detail=message)

class BookExistsError(BookError):
    def __init__(self, isbn=None):
        message = "Book already exists" if isbn is None else f"Book with ISBN {isbn} already exists"
        super().__init__(status_code=400, detail=message)

# ----------------------------
# Excepciones de Copias
# ----------------------------
class CopyError(BaseAppError):
    pass

class CopyNotFoundError(CopyError):
    def __init__(self, copy_id=None):
        message = "Copy not found" if copy_id is None else f"Copy with id {copy_id} not found"
        super().__init__(status_code=404, detail=message)

class CopyNotAvailableError(CopyError):
    def __init__(self, copy_id=None):
        message = "Copy not available" if copy_id is None else f"Copy with id {copy_id} is not available"
        super().__init__(status_code=400, detail=message)

# ----------------------------
# Excepciones de Préstamos
# ----------------------------
class LoanError(BaseAppError):
    pass

class LoanNotFoundError(LoanError):
    def __init__(self, loan_id=None):
        message = "Loan not found" if loan_id is None else f"Loan with id {loan_id} not found"
        super().__init__(status_code=404, detail=message)

class LoanLimitExceededError(LoanError):
    def __init__(self, user_id=None):
        message = "Loan limit exceeded" if user_id is None else f"User {user_id} has reached the loan limit"
        super().__init__(status_code=400, detail=message)

# ----------------------------
# Excepciones de Historial de Préstamos
# ----------------------------
class LoanHistoryError(BaseAppError):
    pass

class LoanHistoryNotFoundError(LoanHistoryError):
    def __init__(self, history_id=None):
        message = "Loan history record not found" if history_id is None else f"Loan history record {history_id} not found"
        super().__init__(status_code=404, detail=message)

class LoanHistoryCreationError(LoanHistoryError):
    def __init__(self, detail: str = "Failed to create loan history record"):
        super().__init__(status_code=500, detail=detail)

class PenaltyError(BaseAppError):
    """Clase base para errores de penalizaciones"""
    pass

class NoActivePenaltyError(PenaltyError):
    def __init__(self, user_id=None):
        message = "No active penalty found" if user_id is None else f"No active penalty found for user {user_id}"
        super().__init__(status_code=404, detail=message)

class PenaltyNotFoundError(PenaltyError):
    def __init__(self, penalty_id=None):
        message = "Penalty not found" if penalty_id is None else f"Penalty with id {penalty_id} not found"
        super().__init__(status_code=404, detail=message)

class PenaltyCreationError(PenaltyError):
    def __init__(self, detail: str = "Failed to create penalty record"):
        super().__init__(status_code=500, detail=detail)

class PenaltyHistoryError(BaseAppError):
    """Clase base para errores de historial de penalizaciones"""
    pass

class PenaltyHistoryNotFoundError(PenaltyHistoryError):
    def __init__(self, history_id=None):
        message = "Penalty history record not found" if history_id is None else f"Penalty history record {history_id} not found"
        super().__init__(status_code=404, detail=message)

class PenaltyHistoryCreationError(PenaltyHistoryError):
    def __init__(self, detail: str = "Failed to create penalty history record"):
        super().__init__(status_code=500, detail=detail)

class RecommendationError(BaseAppError):
    """Clase base para errores de recomendaciones"""
    pass

class RecommendationExistsError(RecommendationError):
    def __init__(self, book_id=None, user_id=None):
        if book_id and user_id:
            message = f"Recommendation already exists for book {book_id} by user {user_id}"
        else:
            message = "Recommendation already exists"
        super().__init__(status_code=400, detail=message)

class RecommendationNotFoundError(RecommendationError):
    def __init__(self, recommendation_id=None):
        message = "Recommendation not found" if recommendation_id is None else f"Recommendation {recommendation_id} not found"
        super().__init__(status_code=404, detail=message)