from django.test import TestCase

# Create your tests here.
def soma(a,b):
    return a + b

def test_soma():
    assert soma(1, 2) == 3
    assert soma(-1, 1) == 0