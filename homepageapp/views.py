from django.shortcuts import render
from django.views.generic import TemplateView
import math
# Create your views here.
class HomePageView(TemplateView):
    template_name = 'home.html'
    def post(self, request, *args, **kwargs):
        expression = request.POST.get('expression')

        # Set epsilon to 0.000001 as in the original code
        epsilon = 0.000001

        # Initialize variables
        a, b, c, k = 0, 0.1, 0, 0

        # Perform the bisection method
        while self.f(expression, a) * self.f(expression, b) > 0:
            a += 0.1
            b = a + 0.1

        while abs(self.f(expression, c)) > epsilon:
            k += 1
            c = a - self.f(expression, a) * ((b - a) / (self.f(expression, b) - self.f(expression, a)))
            if self.f(expression, a) * self.f(expression, c) < 0:
                b = c
            else:
                a = c

        context = {
            'result': c,
        }
        return self.render_to_response(context)

    def f(self, Y, n):
        parsed_expression = self.parse_expression(Y, n)
        result = self.evaluate_expression(parsed_expression)
        return result

    def parse_expression(self, expression, x_value):
        expression = expression.replace('sin(x)', f'math.sin({x_value})')
        expression = expression.replace('exp(x)', f'math.exp({x_value})')
        expression = expression.replace('log10(x)', f'math.log10({x_value})')
        expression = expression.replace('tan(x)', f'math.tan({x_value})')
        expression = expression.replace('x', str(x_value))
        return expression

    def evaluate_expression(self, expression):
        try:
            result = eval(expression)
            return result
        except Exception as e:
            return f"Error: {e}"