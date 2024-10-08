from .models import CarritoJuego 

def user_context_processor(request):
    print(f'User:  {request.user.username}')
    return {
        'username': request.user.username,
        'is_authenticated': request.user.is_authenticated
    }
# para el examen
# def carrito_context_processor(request):