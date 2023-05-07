import uuid


def count_questions_text(count_questions):
    last_digit = count_questions % 10
    if 10 <= count_questions <= 20 or last_digit == 0 or last_digit >= 5:
        return f'о {count_questions} вопросов'
    elif last_digit == 1:
        return f' {count_questions} вопрос'
    return f'о {count_questions} вопроса'


def get_or_set_user_cookie(self, request, dispatch_func, *args, **kwargs):
    self.user_cookie = request.COOKIES.get('user_cookie')
    if not self.user_cookie:
        self.user_cookie = uuid.uuid4().hex
        response = dispatch_func(request, *args, **kwargs)
        response.set_cookie('user_cookie', self.user_cookie)
    else:
        response = dispatch_func(request, *args, **kwargs)
    return response
