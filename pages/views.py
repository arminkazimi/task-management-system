from django.shortcuts import render

def home(request):
    """Render the home page with navigation links based on authentication status."""
    return render(request, 'pages/home.html')
